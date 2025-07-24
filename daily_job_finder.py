import os
import json
import requests
from datetime import datetime
import google.generativeai as genai
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email_builder import generate_digest

cache_file = 'cache.json'

# Load cache safely
if os.path.exists(cache_file) and os.path.getsize(cache_file) > 0:
    with open(cache_file, 'r') as f:
        cache = json.load(f)
else:
    cache = {"job_ids": []}

# Load config from environment variables
config = {
    "gemini_api_key": os.environ.get("GEMINI_API_KEY"),
    "adzuna": {
        "country": os.environ.get("ADZUNA_COUNTRY", "in"),
        "app_id": os.environ.get("ADZUNA_APP_ID"),
        "app_key": os.environ.get("ADZUNA_APP_KEY"),
        "results_per_page": int(os.environ.get("ADZUNA_RESULTS_PER_PAGE") or 5),
        "search_term": os.environ.get("ADZUNA_SEARCH_TERM", "python developer")
    },
    "email": {
        "subject": os.environ.get("EMAIL_SUBJECT", "Daily Job Digest"),
        "recipient": os.environ.get("EMAIL_RECIPIENT"),
        "smtp_user": os.environ.get("EMAIL_SMTP_USER"),
        "smtp_password": os.environ.get("EMAIL_SMTP_PASSWORD")
    }
}

# Configure Gemini API
genai.configure(api_key=config['gemini_api_key'])
model = genai.GenerativeModel('gemini-1.5-flash')

def fetch_jobs():
    print("Fetching jobs from Adzuna...")
    url = f"https://api.adzuna.com/v1/api/jobs/{config['adzuna']['country']}/search/1"
    params = {
        'app_id': config['adzuna']['app_id'],
        'app_key': config['adzuna']['app_key'],
        'results_per_page': config['adzuna']['results_per_page'],
        'what': config['adzuna']['search_term'],
        'content-type': 'application/json'
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error fetching jobs: {response.status_code} {response.text}")
        return []

    data = response.json()
    jobs = []
    for item in data.get('results', []):
        jobs.append({
            "id": str(item['id']),
            "title": item['title'],
            "company": item['company']['display_name'] if item.get('company') else "Unknown",
            "location": item['location']['display_name'] if item.get('location') else "Unknown",
            "description": item.get('description', ''),
            "url": item['redirect_url'],
        })
    return jobs

def summarize_job(job):
    prompt = (
        f"Summarize this job posting in 2 sentences:\n\n"
        f"Title: {job['title']}\n"
        f"Company: {job['company']}\n"
        f"Description: {job['description']}"
    )
    response = model.generate_content(prompt)
    summary = response.candidates[0].content.parts[0].text
    return summary.strip()

def send_email(html_content, subject, to_email, smtp_user, smtp_password):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = to_email

    part = MIMEText(html_content, "html")
    msg.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)

def main():
    jobs = fetch_jobs()
    new_jobs = [job for job in jobs if job['id'] not in cache['job_ids']]
    if not new_jobs:
        print("No new jobs today.")
        return

    for job in new_jobs:
        job['summary'] = summarize_job(job)

    digest = generate_digest(new_jobs)

    send_email(
        digest,
        config['email']['subject'],
        config['email']['recipient'],
        config['email']['smtp_user'],
        config['email']['smtp_password']
    )

    cache['job_ids'].extend(job['id'] for job in new_jobs)
    with open(cache_file, 'w') as f:
        json.dump(cache, f)

    print("Done!")

if __name__ == "__main__":
    import traceback
    try:
        main()
    except Exception:
        traceback.print_exc()
        exit(1)
