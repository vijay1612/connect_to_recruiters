import requests

# Replace this with your actual Nymeria API Key
API_KEY = "837e1300-bd34-4f66-8a0a-ee6bf1565768"

# Define the company and job title to search for recruiters
company_name = "Amazon"
job_title = "Technical Recruiter"

# Define the API URL
url = f"https://www.nymeria.io/api/v4/person/search?title={'Technical Recruiter'}&company={'Amazon'}"

# Set up the headers with the API key
headers = {
    "X-Api-Key": "837e1300-bd34-4f66-8a0a-ee6bf1565768"
}

# Make the API request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    
    # Extract recruiter emails
    recruiters = []
    for person in data.get("data", []):
        full_name = person.get("full_name", "Unknown")
        emails = person.get("emails", [])
        email_list = [email["address"] for email in emails if email]
        
        recruiters.append({"name": full_name, "emails": email_list})

    # Print the fetched recruiters
    if recruiters:
        print("✅ Recruiters Found:")
        for recruiter in recruiters:
            print(f"Name: {recruiter['name']}")
            print(f"Emails: {', '.join(recruiter['emails'])}")
            print("-" * 40)
    else:
        print("❌ No recruiters found for the given company and job title.")

else:
    print(f"❌ API request failed with status code {response.status_code}: {response.text}")
