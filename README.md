# Daily Secretary

A personal AI-style secretary that emails you a daily journal every morning at
**07:00 Paris time** with:

- Today's weather (Paris)
- Top news headlines from the last 24 hours
- Your Google Calendar events for today
- Five rotating programs (summer schools, sponsored events, insight days) in
  finance, astronomy and coding/tech
- Topic-based alerts: anything relevant to a Grade-12 student in France
  (Parcoursup, scholarships, French baccalauréat news, etc.)

Designed to run for free on **GitHub Actions** — no server needed.

---

## How it works

```
GitHub Actions (cron, 5am + 6am UTC)
         │
         ▼
   main.py  ──►  modules/weather.py     (Open-Meteo, no key)
              │ modules/news.py         (NewsAPI + Google News RSS)
              │ modules/calendar_module.py  (Google Calendar OAuth)
              │ modules/programs.py     (curated rotating list)
              │ modules/alerts.py       (Google News keyword feeds)
              ▼
         modules/emailer.py (Gmail SMTP)
              │
              ▼
        leoshancx@gmail.com
```

A small "gate" step inside the workflow only sends when the **Paris local hour
is 7**, so DST is handled automatically.

---

## Setup (one time, ~30 minutes)

### 1. Clone this folder into a GitHub repo

```bash
gh repo create daily-secretary --private --source=. --push
# or: create a new empty repo on github.com and push manually.
```

### 2. Get a NewsAPI key (free)

- Visit https://newsapi.org/register and copy your API key.

### 3. Create a Gmail App Password

- Open https://myaccount.google.com/apppasswords (you must have 2FA enabled).
- Create a password for "Mail" / "Other (Daily Secretary)".
- Copy the 16-character password — you won't see it again.

### 4. Authorize Google Calendar (run locally, once)

```bash
pip install -r requirements.txt
```

- Go to https://console.cloud.google.com/
- Create a new project (e.g. "Daily Secretary").
- Under **APIs & Services → Library**, enable **Google Calendar API**.
- Under **OAuth consent screen**: type = External; add yourself as a test user.
- Under **Credentials**: create an **OAuth client ID** of type
  **Desktop app**. Download the JSON file as `credentials.json` into this
  folder.
- Run:

  ```bash
  python setup_google_auth.py
  ```

- A browser will open; sign in as `leoshancx@gmail.com` and click **Allow**.
- A file `token.json` will be created. Open it and copy its entire content
  (one long JSON line).

### 5. Add GitHub secrets

In your repo: **Settings → Secrets and variables → Actions → New repository secret**

| Name                  | Value                                 |
|-----------------------|---------------------------------------|
| `GMAIL_ADDRESS`       | `leoshancx@gmail.com`                 |
| `GMAIL_APP_PASSWORD`  | the 16-char app password              |
| `RECIPIENT_EMAIL`     | `leoshancx@gmail.com`                 |
| `NEWSAPI_KEY`         | your NewsAPI key                      |
| `GOOGLE_TOKEN_JSON`   | the full content of `token.json`      |

### 6. Test it

Go to **Actions → Daily Secretary → Run workflow** to fire a manual run.

> Note: a manual run still passes through the "Paris hour == 7" gate. To test
> at any hour, temporarily comment out that gate in `.github/workflows/daily.yml`
> or run locally with `python main.py --dry-run`.

---

## Running locally

```bash
cp .env.example .env
# fill in your secrets in .env
pip install -r requirements.txt

python main.py --dry-run   # writes journal_preview.html, sends nothing
python main.py             # sends the email
```

---

## Customizing

| What you want to change                  | Where                                   |
|------------------------------------------|-----------------------------------------|
| City / coordinates / timezone            | `.env` and the workflow's `env:` block  |
| News topics & languages                  | `modules/news.py` → `GENERAL_TOPICS`    |
| Personal alert keywords                  | `modules/alerts.py` → `ALERT_TOPICS`    |
| List of programs / summer schools        | `modules/programs.py` → `PROGRAMS`      |
| Email template & section order           | `main.py` → `build_journal_html()`      |
| Send time                                | `.github/workflows/daily.yml` cron      |

---

## Cost

Everything runs on free tiers:

- **GitHub Actions**: 2,000 free min/month (this uses ~2 min/day = ~60/month).
- **NewsAPI**: 100 requests/day free, this uses ~4.
- **Open-Meteo**: completely free, no key.
- **Google Calendar API**: free for personal use.
- **Gmail SMTP**: free.

No paid services required.

---

## Troubleshooting

- *No emails arriving*: check Spam, and check the **Actions** tab for failed
  runs.
- *Calendar error: "Token has been expired or revoked"*: rerun
  `setup_google_auth.py` locally and update the `GOOGLE_TOKEN_JSON` secret.
- *News list empty*: NewsAPI free tier denies requests from cloud IPs in some
  regions — the code automatically falls back to Google News RSS in that case.

---

## File map

```
daily-secretary/
├── .github/workflows/daily.yml   # cron + GitHub Actions job
├── modules/
│   ├── weather.py
│   ├── news.py
│   ├── calendar_module.py
│   ├── programs.py
│   ├── alerts.py
│   └── emailer.py
├── main.py                       # orchestrator
├── setup_google_auth.py          # one-time OAuth flow
├── requirements.txt
├── .env.example
└── README.md
```
