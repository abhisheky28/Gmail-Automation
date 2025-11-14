# main.py
import pandas as pd
import json
import os
import sys
import random
import time
from datetime import datetime
import pytz

# Import content and the mock gsmtp library
import templates
import gsmtp

# --- Configuration ---
CONFIG_FILE = 'config.json'
LOCK_FILE = 'script.lock'
ASSETS_DIR = 'assets'
LOGO_FILE = os.path.join(ASSETS_DIR, 'company_logo.png')

# --- Global variable for log file path to be accessible by the logger function ---
LOG_FILE_PATH = None

# --- Helper Functions ---

def log_action(email, assigned_to, action, sending_account, result, details):
    """Appends a new record to the execution log Excel file."""
    global LOG_FILE_PATH
    if not LOG_FILE_PATH:
        print(f"FATAL: Log file path is not configured. Cannot log action for email: {email}.")
        return
        
    try:
        log_df = pd.DataFrame([{
            'TimestampUTC': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'Email': email,
            'AssignedTo': assigned_to,
            'Action': action,
            'SendingAccount': sending_account,
            'Result': result,
            'Details': str(details) # Ensure details are always a string
        }])
        
        mode = 'a' if os.path.exists(LOG_FILE_PATH) else 'w'
        header = not os.path.exists(LOG_FILE_PATH)
        
        with pd.ExcelWriter(LOG_FILE_PATH, engine='openpyxl', mode=mode, if_sheet_exists='overlay' if mode == 'a' else None) as writer:
            log_df.to_excel(writer, index=False, header=header, sheet_name='Log')

    except PermissionError:
        print(f"FATAL: Could not write to log file {LOG_FILE_PATH}. It is likely open in Excel. Please close it.")
    except Exception as e:
        print(f"FATAL: An unexpected error occurred while writing to the log file {LOG_FILE_PATH}. Error: {e}")

def get_iana_timezone(city_name, mapping):
    """Converts a simple city name to a proper IANA timezone format using the config mapping."""
    return mapping.get(city_name, 'UTC')

def is_business_hours(iana_timezone_str):
    """Checks if the current time in the given timezone is within business hours (Mon-Fri, 9am-5pm)."""
    try:
        target_tz = pytz.timezone(iana_timezone_str)
        now_in_tz = datetime.now(target_tz)
        is_weekday = now_in_tz.weekday() < 5
        is_in_hours = 9 <= now_in_tz.hour < 17
        return is_weekday and is_in_hours
    except pytz.UnknownTimeZoneError:
        log_action(None, None, 'TimezoneCheck', None, 'Failure', f"Invalid IANA timezone in config: {iana_timezone_str}")
        return False

# --- Main Execution Logic ---

def main():
    """The core logic loop of the automation engine."""
    global LOG_FILE_PATH
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        
        contacts_file_path = config['file_paths']['contacts_file']
        LOG_FILE_PATH = config['file_paths']['log_file']
        
        # Read both sheets at once for efficiency and to fail early if one is missing
        excel_data = pd.read_excel(contacts_file_path, sheet_name=['Input', '_AutomationState'])
        input_df = excel_data['Input']
        state_df = excel_data['_AutomationState']

    except FileNotFoundError:
        print(f"FATAL: The config file '{CONFIG_FILE}' or the contacts file could not be found.")
        return
    except json.JSONDecodeError:
        print(f"FATAL: The config file '{CONFIG_FILE}' is malformed. Please check for syntax errors like missing commas.")
        return
    except KeyError:
        print(f"FATAL: 'file_paths' section or a required key is missing in {CONFIG_FILE}. Please add it.")
        return
    except ValueError as e:
        # This often happens if a sheet name is not found
        log_action(None, None, 'Initialization', None, 'Failure', f"Error reading Excel file. A required sheet (e.g., 'Input', '_AutomationState') might be missing. Details: {e}")
        return
    except Exception as e:
        # A catch-all for other unexpected errors during initialization
        log_action(None, None, 'Initialization', None, 'Failure', f"An unexpected error occurred while reading input files: {e}")
        return

    merged_df = pd.merge(input_df, state_df, on='Email', how='left')
    merged_df['Status'] = merged_df['Status'].fillna('NEW')
    merged_df['FollowUpStep'] = merged_df['FollowUpStep'].fillna(0).astype(int)
    
    now_utc = datetime.utcnow()
    
    for index, contact in merged_df.iterrows():
        email = contact['Email']
        assigned_to = contact['AssignedTo']
        
        # Defensive check: Skip rows where essential data is missing to prevent crashes
        if pd.isna(email) or pd.isna(assigned_to):
            continue

        status = contact['Status']
        follow_up_step = contact['FollowUpStep']
        last_contacted_utc_val = contact.get('LastContactedUTC')
        
        if str(status).lower() == 'replied':
            continue

        action_to_take = None
        last_contacted_utc = pd.to_datetime(last_contacted_utc_val) if pd.notna(last_contacted_utc_val) else None

        if status == 'Contacted' and last_contacted_utc:
            days_since_contact = (now_utc - last_contacted_utc).days
            if follow_up_step == 2 and days_since_contact >= 7:
                action_to_take = 'final_follow_up'
            elif follow_up_step == 1 and days_since_contact >= 3:
                action_to_take = 'follow_up_1'
        elif status == 'NEW':
            action_to_take = 'outreach'

        if not action_to_take:
            continue

        contact_timezone_str = get_iana_timezone(contact['Timezone'], config['timezone_mapping'])
        if not is_business_hours(contact_timezone_str):
            log_action(email, assigned_to, action_to_take, None, 'Skipped', f"Outside business hours in {contact['Timezone']} ({contact_timezone_str})")
            continue

        user_config = config['users'].get(assigned_to)
        user_templates = templates.TEMPLATES.get(assigned_to)

        if not user_config or not user_templates:
            log_action(email, assigned_to, action_to_take, None, 'Failure', f"No config or templates found for user '{assigned_to}'")
            continue
        
        # --- CRITICAL ROBUSTNESS CHECK ---
        # Ensure the sending_accounts list is not empty before choosing from it
        if not user_config['sending_accounts']:
            log_action(email, assigned_to, action_to_take, None, 'Failure', f"User '{assigned_to}' has no sending_accounts configured.")
            continue
        sending_account = random.choice(user_config['sending_accounts'])
        
        sig_details = user_config['signature_details']
        signature_html = templates.SIGNATURE_TEMPLATE.replace('{{name}}', sig_details['name']).replace('{{designation}}', sig_details['designation']).replace('{{phone}}', sig_details['phone'])
        
        template_list = user_templates.get(action_to_take, [])
        if not template_list:
            log_action(email, assigned_to, action_to_take, None, 'Failure', f"No templates found for action '{action_to_take}' for user '{assigned_to}'")
            continue
        template = random.choice(template_list)
        
        # Use .get() for custom fields to avoid errors if they are missing
        email_body_html = template['body'].replace('{{FirstName}}', str(contact.get('FirstName', ''))).replace('{{CompanyName}}', str(contact.get('CompanyName', '')))
        final_html = email_body_html + signature_html
        subject = template['subject'].replace('{{CompanyName}}', str(contact.get('CompanyName', '')))

        try:
            gsmtp.send_email(
                sender_email=sending_account['email'],
                app_password=sending_account['app_password'],
                recipient=email,
                subject=subject,
                html_body=final_html,
                image_path=LOGO_FILE,
                image_cid='companyLogo'
            )
            log_action(email, assigned_to, action_to_take, sending_account['email'], 'Success', 'Email sent successfully.')
            merged_df.loc[index, 'Status'] = 'Contacted'
            merged_df.loc[index, 'FollowUpStep'] = follow_up_step + 1
            merged_df.loc[index, 'LastContactedUTC'] = now_utc
            time.sleep(random.uniform(2, 5))
        except Exception as e:
            log_action(email, assigned_to, action_to_take, sending_account['email'], 'Failure', f"Error sending email: {e}")

    final_state_df = merged_df[['Email', 'Status', 'FollowUpStep', 'LastContactedUTC']]
    
    try:
        with pd.ExcelWriter(contacts_file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            final_state_df.to_excel(writer, sheet_name='_AutomationState', index=False)
    except Exception as e:
        log_action(None, None, 'StateUpdate', None, 'Failure', f"Could not write updated state to {contacts_file_path}. Error: {e}")


if __name__ == "__main__":
    if os.path.exists(LOCK_FILE):
        print(f"[{datetime.now()}] Script is already running. Exiting.")
        sys.exit()
    
    try:
        with open(LOCK_FILE, 'w') as f:
            f.write(str(os.getpid()))
        main()
    finally:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
        print(f"[{datetime.now()}] Script finished. Lock released.")