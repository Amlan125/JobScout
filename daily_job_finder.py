import requests
import yaml
import json
import os
from datetime import datetime
import google.generativeai as genai
from email_builder import generate_digest

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Load cache safely
cache_file = 'cache.json'

if os.path.exists(cache_file) and os.path.getsize(cache_file) > 0:
    with open(cache_file, 'r') as f:
        cache = json.load(f)
else:
    cache = {"job_ids": []}

# Load config
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Configure Gemini API
genai.configure(api_key=config['gemini']['api_key'])
model = genai.GenerativeModel('gemini-1.5-flash')  # or 'gemini-1.5-pro'

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

    # Using Gmail SMTP server as example; adjust if different
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
    main()
