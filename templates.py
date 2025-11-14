# templates.py

# Master HTML signature template.
# It uses placeholders {{...}} for data and a CID reference for the embedded logo.
SIGNATURE_TEMPLATE = """
<br><br>
<table style="width: 400px; font-family: Arial, sans-serif; font-size: 12px;">
    <tr>
        <td style="width: 80px; vertical-align: top;">
            <img src="assets\Company_logo.png" alt="Company Logo">
        </td>
        <td style="vertical-align: top;">
            <p style="margin: 0; font-weight: bold; color: #2c3e50;">{{name}}</p>
            <p style="margin: 2px 0; color: #34495e;">{{designation}}</p>
            <p style="margin: 2px 0; color: #34495e;">{{phone}}</p>
        </td>
    </tr>
</table>
"""

# --- CORRECTED STRUCTURE ---
# Each step is now a LIST of template dictionaries, allowing for random selection.
TEMPLATES = {
    "Abhishek": {
        "outreach": [
            {
                "subject": "Exploring a partnership with {{CompanyName}}",
                "body": """
                <p>Hi {{FirstName}},</p>
                <p>In the BFSI, every sale starts with trust — that happens when you engage with the right customer at precisely the right moment.</p>
                <p>At Infidigit, we have helped brands like yours cut through the noise and connect meaningfully with their audience. From increasing product visibility to driving high-intent traffic, our digital approach is built for measurable, revenue-focused impact.</p>
                <p>Leading brands like Kotak Life, SBI Life, Razorpay, HDFC Life have partnered with us for years — and continue to place their trust in our work.  "For a leading BFSI client, we have obtained more than 100 percent growth in leads." </p>
                <p> Let’s explore how we can do the same for your brand. You can pick a time and we’ll take it from there.: Booking Calendar</p>
                <p>Best regards,</p>
                """
            },
            {
                "subject": "Quick question for {{CompanyName}}",
                "body": """
                <p>Hi {{FirstName}},</p>
                <p>In the BFSI, every sale starts with trust — that happens when you engage with the right customer at precisely the right moment.</p>
                <p>At Infidigit, we have helped brands like yours cut through the noise and connect meaningfully with their audience. From increasing product visibility to driving high-intent traffic, our digital approach is built for measurable, revenue-focused impact.</p>
                <p>Leading brands like Kotak Life, SBI Life, Razorpay, HDFC Life have partnered with us for years — and continue to place their trust in our work.  "For a leading BFSI client, we have obtained more than 100 percent growth in leads." </p>
                <p> Let’s explore how we can do the same for your brand. You can pick a time and we’ll take it from there.: Booking Calendar</p>
                <p>Best regards,</p>
                """
            }
        ],
        "follow_up_1": [
            {
                "subject": "Re: Exploring a partnership with {{CompanyName}}",
                "body": """
                <p>Hi {{FirstName}},</p>
                <p>Just wanted to follow up on my previous email. We are confident we can bring significant value to {{CompanyName}}.</p>
                <p>Are you the right person to discuss this with? If not, could you please point me in the right direction?</p>
                <p>Thanks,</p>
                """
            },
            {
                "subject": "Following up",
                "body": """
                <p>Hello {{FirstName}},</p>
                <p>I'm just checking in on my email below. If you have a moment, I'd love to hear your thoughts.</p>
                <p>Best,</p>
                """
            }
        ],
        "final_follow_up": [
            {
                "subject": "Re: Exploring a partnership with {{CompanyName}}",
                "body": """
                <p>Hi {{FirstName}},</p>
                <p>I haven't heard back from you, so I'll assume now isn't the right time. Please feel free to reach out if things change in the future.</p>
                <p>Wishing you and {{CompanyName}} all the best.</p>
                <p>Sincerely,</p>
                """
            },
            {
                "subject": "Closing the loop",
                "body": """
                <p>Hello {{FirstName}},</p>
                <p>I'm writing to you one last time. I understand you're busy, so I won't reach out again on this topic.</p>
                <p>If you ever need assistance with your business goals, please don't hesitate to get in touch.</p>
                <p>All the best,</p>
                """
            }
        ]
    },




    "Abhi": {
        # NOTE: These are placeholders. Please edit them to be unique for Abhi.
        "outreach": [
            {
                "subject": "A question for {{CompanyName}}",
                "body": """
                <p>Hi {{FirstName}},</p>
                <p>In the BFSI, every sale starts with trust — that happens when you engage with the right customer at precisely the right moment.</p>
                <p>At Infidigit, we have helped brands like yours cut through the noise and connect meaningfully with their audience. From increasing product visibility to driving high-intent traffic, our digital approach is built for measurable, revenue-focused impact.</p>
                <p>Leading brands like Kotak Life, SBI Life, Razorpay, HDFC Life have partnered with us for years — and continue to place their trust in our work.  "For a leading BFSI client, we have obtained more than 100 percent growth in leads." </p>
                <p> Let’s explore how we can do the same for your brand. You can pick a time and we’ll take it from there.: Booking Calendar</p>
                <p>Best regards,</p>
                """
            }
        ],
        "follow_up_1": [
            {
                "subject": "Re: A question for {{CompanyName}}",
                "body": """
                <p>Hi {{FirstName}},</p>
                <p>Just checking in on my previous email. If you have a moment, I'd love to hear your thoughts.</p>
                <p>Thanks,</p>
                """
            }
        ],
        "final_follow_up": [
            {
                "subject": "Re: A question for {{CompanyName}}",
                "body": """
                <p>Hi {{FirstName}},</p>
                <p>I'll assume now isn't the best time to connect. I won't reach out again, but please feel free to get in touch if your priorities change.</p>
                <p>All the best,</p>
                """
            }
        ]
    }
}