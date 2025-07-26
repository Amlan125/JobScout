# JobScout – AI-Powered Daily Job Digest

JobScout is an AI-powered automation tool that helps you discover new job opportunities effortlessly.
Every day, it automatically fetches fresh job listings from the Adzuna API based on your chosen keywords and location. These listings are then summarized into short, clear highlights using Gemini AI, turning lengthy job descriptions into easy-to-skim insights.

The final result is packaged into a beautifully formatted HTML email digest that lands directly in your inbox each morning — ensuring you never miss a relevant opportunity, without spending hours scrolling through job boards.

JobScout is fully automated using GitHub Actions as a scheduler, written entirely in Python, and designed to be lightweight, extensible, and private (thanks to secure use of repository secrets). Whether you’re actively job hunting or just keeping an eye on the market, JobScout brings the latest opportunities to you — distilled, summarized, and ready to read.

---


## Features
- Fetch jobs daily from Adzuna (free job API)
- Summarize and rank jobs using OpenAI
- Email yourself a daily digest
- Cache to avoid duplicate jobs
- Easy to extend (Slack, Notion, etc.)

## How it works
1. Scheduler triggers script daily (cron / GitHub Actions)
2. Fetch jobs by keywords & location from Adzuna
3. Summarize jobs with OpenAI
4. Generate a Markdown/HTML email
5. Send to your inbox


## Tech Stack
- **Python** (main logic)
- **Google Generative AI (Gemini)** for job summarization
- **Adzuna API** for job listings
- **SMTP** (`smtplib`) for sending emails
- **GitHub Actions** as the scheduler
- **JSON** for caching

## Setup & Installation
```bash
git clone https://github.com/yourusername/daily_job_scout.git
cd daily_job_scout
pip install -r requirements.txt
```

## Set up Secrets in GitHub

Go to **Repository → Settings → Secrets → Actions → New repository secret** and add the following:

| Secret Name                | Example Value / Description                                 |
|---------------------------|-------------------------------------------------------------|
| `ADZUNA_APP_ID`           | *(Your Adzuna application ID)*                              |
| `ADZUNA_APP_KEY`          | *(Your Adzuna application key)*                             |
| `ADZUNA_COUNTRY`          | e.g., `de`                                                  |
| `ADZUNA_SEARCH_TERM`      | e.g., `python developer`                                    |
| `ADZUNA_RESULTS_PER_PAGE` | e.g., `5`                                                    |
| `GEMINI_API_KEY`          | *(Your Gemini AI API key)*                                  |
| `EMAIL_SMTP_USER`         | e.g., `your-email@gmail.com` (the sender’s email address)   |
| `EMAIL_SMTP_PASSWORD`     | *(App Password from your email provider, **not** your main password)* |
| `EMAIL_RECIPIENT`         | e.g., `your-email@gmail.com` (the recipient’s email address) |
| `EMAIL_SUBJECT`           | e.g., `Daily Job Digest`                                    |

---

## Configure the Workflow

The workflow file is located at:

```text
.github/workflows/job.yml
```

It is already configured to run daily at the preferred UTC using a cron schedule.
It can also be manually triggered at any time from the Actions tab in the GitHub repository.


## Author

Built by Amlan (https://github.com/Amlan125)
