import requests
import smtplib
import os
from email.message import EmailMessage

# ✅ Replace with your Nymeria API Key
API_KEY = "837e1300-bd34-4f66-8a0a-ee6bf1565768"

# ✅ List of companies to search for recruiters
companies = ["Amazon", "Salesforce", "Walmart"]
job_title = "Technical Recruiter"

# ✅ Your email credentials (for sending emails)
SENDER_EMAIL = "vijayreddymopuru@gmail.com"
SENDER_PASSWORD = "VIjaymuni55@"

# ✅ Path to your resume (update with the actual file path)
RESUME_PATH = "/Users/vijju/Desktop/projects/Nymeria/Vijay_Reddy_docx.docx"

# ✅ Define the email subject and message
SUBJECT = "Seeking Data Scientist Opportunities – Resume Attached"
MESSAGE = """
Dear {name},

I hope you're doing well. I came across your profile and wanted to reach out regarding Data Scientist opportunities at {company}. 

I have 10+ years of experience in Data Engineering and Business Intelligence, with expertise in AWS, Databricks, SQL, and Machine Learning. I am interested in contributing my skills to {company} and would love to discuss any available opportunities.

Attached is my resume for your reference. Looking forward to connecting.

Best Regards,  
Vijay Muni  
(Your LinkedIn Profile Here)
"""

# Function to fetch recruiters' emails
def fetch_recruiters(company):
    url = f"https://www.nymeria.io/api/v4/person/search?title={job_title}&company={company}"
    headers = {"X-Api-Key": "837e1300-bd34-4f66-8a0a-ee6bf1565768"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        recruiters = []
        for person in data.get("data", []):
            full_name = person.get("full_name", "Recruiter")
            emails = person.get("emails", [])
            email_list = [email["address"] for email in emails if email]
            
            if email_list:
                recruiters.append({"name": full_name, "emails": email_list, "company": company})
        return recruiters
    else:
        print(f"❌ API request failed for {company} - Status Code: {response.status_code}")
        return []

# Function to send email
def send_email(recruiter_name, recruiter_email, company):
    msg = EmailMessage()
    msg["From"] = SENDER_EMAIL
    msg["To"] = recruiter_email
    msg["Subject"] = SUBJECT
    msg.set_content(MESSAGE.format(name=recruiter_name, company=company))

    # Attach Resume
    with open("/Users/vijju/Desktop/projects/Nymeria/Vijay_Reddy_docx.docx", "rb") as resume_file:
        msg.add_attachment(resume_file.read(), maintype="application", subtype="pdf", filename=os.path.basename(RESUME_PATH))

    # Send Email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print(f"✅ Email sent to {recruiter_name} ({recruiter_email}) at {company}")
    except Exception as e:
        print(f"❌ Failed to send email to {recruiter_email} - Error: {e}")

# Main Script Execution
if __name__ == "__main__":
    for company in companies:
        recruiters = fetch_recruiters(company)
        for recruiter in recruiters:
            for email in recruiter["emails"]:
                send_email(recruiter["name"], email, recruiter["company"])
