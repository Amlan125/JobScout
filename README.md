# 🧠 Daily AI-Powered Job Scout

Automatically find new jobs every day, summarize them with AI, and get a clean email digest.

## ✨ Features
- Fetch jobs daily from Adzuna (free job API)
- Summarize and rank jobs using OpenAI
- Email yourself a daily digest
- Cache to avoid duplicate jobs
- Easy to extend (Slack, Notion, etc.)

## ⚙️ How it works
1. Scheduler triggers script daily (cron / GitHub Actions)
2. Fetch jobs by keywords & location from Adzuna
3. Summarize jobs with OpenAI
4. Generate a Markdown/HTML email
5. Send to your inbox

## 🛠️ Tech Stack
- Python
- requests (HTTP)
- openai (AI summarization)
- smtplib / yagmail (email)
- pyyaml (config)
- JSON (cache)

## 📦 Install
```bash
git clone https://github.com/yourusername/daily_job_scout.git
cd daily_job_scout
pip install -r requirements.txt
