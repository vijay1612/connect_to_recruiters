import streamlit as st
import requests
import smtplib
import os
from email.message import EmailMessage

# Set Streamlit Page Config
st.set_page_config(page_title="Recruiter Outreach", page_icon="📧", layout="wide")

# API Key (Replace with your actual Nymeria API Key)
API_KEY = "your_api_key_here"

# Email Credentials (Replace with your details)
SENDER_EMAIL = "your_email"
SENDER_PASSWORD = "pass"  # Please check your email settings before.

# Resume Path (Update with your actual resume path)
RESUME_PATH = "Path to your resume"

# Streamlit UI
st.title("📧 Automated Recruiter Outreach")
st.markdown("### Find recruiter emails and send your resume in one click!")

# User Input: Job Title and Company Names
job_title = st.text_input("Enter Job Title", value="Data Scientist Recruiter")
companies = st.text_area("Enter Company Names (one per line)", "Amazon\nSalesforce\nWalmart")

# Button to Fetch Recruiters
if st.button("Find Recruiters"):
    companies_list = companies.split("\n")

    st.subheader("🔍 Searching for Recruiters...")
    
    def fetch_recruiters(company):
        url = f"https://www.nymeria.io/api/v4/person/search?title={job_title}&company={company.strip()}"
        headers = {"X-Api-Key": "Api"}
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
            st.error(f"❌ API request failed for {company} - Status Code: {response.status_code}")
            return []

    all_recruiters = []
    for company in companies_list:
        recruiters = fetch_recruiters(company)
        all_recruiters.extend(recruiters)

    if all_recruiters:
        st.success(f"✅ Found {len(all_recruiters)} recruiters!")
        
        # Show Recruiters in a Table
        st.write("### Recruiter Details")
        recruiter_data = []
        for recruiter in all_recruiters:
            for email in recruiter["emails"]:
                recruiter_data.append([recruiter["name"], recruiter["company"], email])
        st.table(recruiter_data)

        # Button to Send Emails
        if st.button("Send Emails to Recruiters"):
            st.subheader("📤 Sending Emails...")
            
            def send_email(recruiter_name, recruiter_email, company):
                msg = EmailMessage()
                msg["From"] = SENDER_EMAIL
                msg["To"] = recruiter_email
                msg["Subject"] = "Seeking Data Scientist Opportunities – Resume Attached"
                msg.set_content(f"Dear {recruiter_name},\n\n"
                                f"I hope you're doing well. I am reaching out regarding Data Scientist opportunities at {company}.\n"
                                "I have 10+ years of experience in Data Engineering, BI, SQL, and Machine Learning.\n"
                                "Attached is my resume for your reference. Looking forward to connecting.\n\n"
                                "Best Regards,\nVijay Muni\n(Your LinkedIn Profile Here)")

                # Attach Resume
                with open(RESUME_PATH, "rb") as resume_file:
                    msg.add_attachment(resume_file.read(), maintype="application", subtype="pdf", filename=os.path.basename(RESUME_PATH))

                # Send Email
                try:
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                        server.login(SENDER_EMAIL, SENDER_PASSWORD)
                        server.send_message(msg)
                    st.success(f"✅ Email sent to {recruiter_name} ({recruiter_email}) at {company}")
                except Exception as e:
                    st.error(f"❌ Failed to send email to {recruiter_email} - Error: {e}")

            for recruiter in all_recruiters:
                for email in recruiter["emails"]:
                    send_email(recruiter["name"], email, recruiter["company"])

    else:
        st.warning("⚠️ No recruiters found. Try different companies or job titles.")

