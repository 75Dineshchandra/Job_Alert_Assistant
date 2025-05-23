# 📱 Real-Time Job Alert Assistant

This Python-based job alert agent scrapes filtered LinkedIn job search URLs, detects new postings in real-time, and **sends email alerts** only for unseen jobs.
It ensures **no duplicates are emailed**, even if LinkedIn adds tracking parameters to job URLs.

---

## 🚀 Features

* 🔍 Scrapes filtered LinkedIn search result pages
* 🔁 Auto-paginates (up to 20 pages or until empty)
* 🧠 Removes tracking parameters (e.g. `refId`, `trackingId`) from URLs
* ✅ Detects only *unseen* job postings
* 📬 Sends email alerts for new jobs only
* 📁 Tracks previously seen jobs in `seen_jobs.csv`

---

## 🗂️ Folder Structure

```
job_alert_agent/
├── config/
│   └── email_config.yaml         # Email credentials (sender, receiver, app password)
├── data/
│   ├── career_urls.json          # List of job board URLs per company
│   └── seen_jobs.csv             # Job history to prevent duplicate alerts
├── src/
│   ├── main.py                   # Main loop: scrape, deduplicate, send email
│   ├── job_scraper.py            # Scraper logic for LinkedIn (can add more)
│   └── emailer.py                # Email logic (SMTP with TLS)
└── requirements.txt              # Required Python packages
```

---

## ⚙️ Setup Instructions

### 1. 📅 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. ✍️ Add LinkedIn URL to `career_urls.json`

```json
{
  "LinkedIn": "https://www.linkedin.com/jobs/search/?keywords=data+analyst&location=United+States"
}
```

Use any valid filtered search URL from LinkedIn.

### 3. 📧 Configure Email in `config/email_config.yaml`

```yaml
sender_email: your_email@gmail.com
sender_pass: YOUR_APP_PASSWORD
receiver_email: destination_email@gmail.com
```

Use a [Gmail App Password](https://support.google.com/accounts/answer/185833) (not your login password).

---

## ▶️ Run the Agent

```bash
python src/main.py
```

It will run continuously, scraping every 60 minutes.

---

## 📧 How Deduplication Works

The agent:

* Strips tracking parameters from LinkedIn URLs using:

```python
url.split("?")[0]
```

* Stores only normalized job title and base URL
* Checks if each job is already stored before sending email

So jobs like:

```
https://linkedin.com/jobs/view/xyz?refId=abc&trackingId=123
https://linkedin.com/jobs/view/xyz?refId=zzz&trackingId=999
```

…are treated as the **same job**.

---

## 📧 Sample Email

```
Subject: New Jobs at LinkedIn

Data Analyst - https://linkedin.com/jobs/view/4220713516
Machine Learning Intern - https://linkedin.com/jobs/view/4220718794
```

---

## 🔁 Extend to More Sites

You can add more keys to `career_urls.json` and implement scrapers in `job_scraper.py`:

```json
{
  "LinkedIn": "https://...",
  "Amazon": "https://...",
  "Meta": "https://..."
}
```

---

## ✅ Dependencies

```
pandas
requests
beautifulsoup4
pyyaml
```

---

## 🤛 Maintainer

**Dinesh Chandra Gaddam**
📧 [dineshchandragaddam2002@gmail.com](mailto:dineshchandragaddam2002@gmail.com)
🔗 [LinkedIn](https://www.linkedin.com/in/dineshchandra-gaddam002/)

---

> This tool ensures you never miss a relevant job posting — and never get duplicate alerts again.
