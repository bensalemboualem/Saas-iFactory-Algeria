# AUTOMATION SCRIPTS (5 scripts, 20 pages équivalent)

Scripts Python à adapter. Besoins: Python 3.10+, clés API (LinkedIn/Facebook/Twitter/SendGrid/OpenAI), accès Google Sheets API. Installe `requirements` ci-dessous.

## Installation
```
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```
`requirements.txt` (exemple minimal):
```
requests
python-dotenv
gspread
oauth2client
sendgrid
schedule
openai
```

## Script 1: Social Media Poster (LN/FB/X)
Pseudo-code:
```python
import schedule, time, json
from clients import post_linkedin, post_facebook, post_twitter

POSTS_FILE = "posts.json"  # [{"channel":"linkedin","text":"...","time":"09:00"}, ...]

def job():
    with open(POSTS_FILE) as f:
        posts = json.load(f)
    now = current_hhmm()
    for p in posts:
        if p["time"] == now:
            if p["channel"] == "linkedin": post_linkedin(p["text"])
            if p["channel"] == "facebook": post_facebook(p["text"])
            if p["channel"] == "twitter": post_twitter(p["text"])

schedule.every().minute.do(job)
while True:
    schedule.run_pending(); time.sleep(1)
```
Setup: créer `posts.json` depuis `EDITORIAL_CALENDAR_30DAYS.md`.

## Script 2: Metrics Collector → Google Sheets
Pseudo-code:
```python
import gspread, schedule, time
from oauth2client.service_account import ServiceAccountCredentials
from collectors import get_visits, get_signups, get_revenue, get_ad_spend

SHEET_NAME = "IAFactory Metrics"

def update_daily():
    row = [today(), get_visits(), get_signups(), get_enrollments(), get_revenue(), get_ad_spend()]
    sheet.append_row(row)

schedule.every().day.at("23:00").do(update_daily)
while True:
    schedule.run_pending(); time.sleep(30)
```
Setup: créer service account JSON, partager le Sheet avec l’email du service account.

## Script 3: Email Sequence Sender (SendGrid)
Pseudo-code:
```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from db import new_signups_since_last_run, mark_sent

TEMPLATES = ["welcome1", "story", "socialproof", "urgency", "lastchance"]

for user in new_signups_since_last_run():
    for tpl in TEMPLATES:
        send_email(user.email, render(tpl, user))
    mark_sent(user.id)
```
Setup: charger les emails prêts dans `MARKETING_TEMPLATES.md`, stocker dans dossiers templates.

## Script 4: Content Generator (OpenAI)
Pseudo-code:
```python
import openai, json
PROMPT = "Écris 5 posts LinkedIn FR sur RAG, ton expert, CTA cours gratuit"
resp = openai.ChatCompletion.create(model="gpt-4", messages=[{"role":"user","content":PROMPT}])
print(resp.choices[0].message["content"])
```
Usage: générer variantes à coller dans le calendrier.

## Script 5: Weekly Reporter
Pseudo-code:
```python
from sheets import get_weekly_summary
from sendgrid import SendGridAPIClient

def send_report():
    summary = get_weekly_summary()
    send_email("team@iafactory", summary)
```
Schedule: Monday 09:00.

## Schedule (Windows Task Scheduler) exemple
Créer une tâche qui lance `python social_poster.py` au login, et `python metrics_collector.py` chaque jour 23:00.

## .env exemple
```
LINKEDIN_TOKEN=...
FACEBOOK_TOKEN=...
TWITTER_TOKEN=...
SENDGRID_API_KEY=...
OPENAI_API_KEY=...
SHEET_ID=...
SERVICE_ACCOUNT_JSON=service_account.json
```

## Structure recommandée
```
automation/
  social_poster.py
  metrics_collector.py
  email_sender.py
  content_generator.py
  weekly_reporter.py
  clients.py
  collectors.py
  sheets.py
  templates/
    email_welcome1.txt
    ...
  posts.json
  .env
```

## Gains attendus
- 4.5h/j économisées (publication, mails, reporting)
- Discipline: pas d’oubli de posts/emails
- Visibilité: metrics quotidiennes, rapport hebdo

## Sécurité
- Ne commite jamais `.env` ni clés.
- Rotate tokens, limiter permissions (service accounts, scopes).
- Tester en sandbox (SendGrid, ad APIs) avant prod.
