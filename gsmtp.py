# gsmtp.py (Production Version)
import smtplib
import ssl
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# --- Configuration for Gmail ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # For SSL

def send_email(sender_email, app_password, recipient, subject, html_body, image_path=None, image_cid=None):
    """
    Sends a real HTML email with an embedded image using Gmail's SMTP server.
    This is the production-ready version.
    """
    print("-" * 50)
    print(f"ATTEMPTING TO SEND REAL EMAIL VIA SMTP")
    print(f"  From: {sender_email}")
    print(f"  To: {recipient}")
    print(f"  Subject: {subject}")
    print("-" * 50)

    # Create the root message and set the headers.
    # 'related' is essential for embedding images.
    msg = MIMEMultipart('related')
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = subject

    # Attach the HTML body of the email.
    msg.attach(MIMEText(html_body, 'html'))

    # Handle the embedded image.
    if image_path and image_cid and os.path.exists(image_path):
        try:
            with open(image_path, 'rb') as img_file:
                # Create the image attachment
                mime_image = MIMEImage(img_file.read())
                
                # Add the Content-ID header. This is the critical part that links
                # the 'cid:companyLogo' in the HTML to this attachment.
                mime_image.add_header('Content-ID', f'<{image_cid}>')
                
                msg.attach(mime_image)
                print(f"  Successfully attached image: {image_path} with CID: {image_cid}")
        except FileNotFoundError:
            print(f"  WARNING: Image file not found at {image_path}. Sending email without image.")
        except Exception as e:
            print(f"  WARNING: Could not attach image. Error: {e}. Sending email without image.")

    # Establish a secure connection with the SMTP server and send the email.
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
            print(f"  SUCCESS: Email sent to {recipient}")
            return True
    except smtplib.SMTPAuthenticationError:
        # This is the most common error: wrong email or app password.
        error_msg = "SMTP Authentication Error: The username or app password you provided is incorrect. Please double-check your config.json."
        print(f"  FAILURE: {error_msg}")
        raise ConnectionRefusedError(error_msg) # Raise a specific error for the log
    except smtplib.SMTPConnectError:
        error_msg = "SMTP Connect Error: Failed to connect to the server. Check your internet connection and firewall settings."
        print(f"  FAILURE: {error_msg}")
        raise ConnectionError(error_msg)
    except Exception as e:
        # Catch any other exceptions during the process.
        error_msg = f"An unexpected error occurred during email sending: {e}"
        print(f"  FAILURE: {error_msg}")
        raise e