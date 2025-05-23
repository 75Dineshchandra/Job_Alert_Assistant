# main.py

import time
import json
import pandas as pd
from job_scraper import scrape_linkedin_jobs, scrape_jobs_from_url
from emailer import send_email
print("🔥 Script started")

SEEN_JOBS_FILE = "data/seen_jobs.csv"
CAREER_URLS_FILE = "data/career_urls.json"

def load_seen_jobs():
    try:
        return pd.read_csv(SEEN_JOBS_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["company", "title", "url"])

def save_seen_jobs(df):
    df.to_csv(SEEN_JOBS_FILE, index=False)

def job_exists(seen_df, company, title, url):
    return not seen_df[
        (seen_df["company"] == company) &
        (seen_df["title"] == title) &
        (seen_df["url"] == url)
    ].empty

def run_realtime_agent():
    seen_jobs = load_seen_jobs()

    with open(CAREER_URLS_FILE) as f:
        companies = json.load(f)

    for company, url in companies.items():
        if not url:
            continue

        print(f"[...] Scraping {company} ({url})")
        try:
            if "linkedin.com/jobs/search" in url:
                jobs = scrape_linkedin_jobs(url)
            else:
                jobs = scrape_jobs_from_url(url)
        except Exception as e:
            print(f"[✘] Error scraping {company}: {e}")
            continue

        new_jobs = []

        for job in jobs:
            if not job_exists(seen_jobs, company, job["title"], job["url"]):
                seen_jobs.loc[len(seen_jobs)] = [company, job["title"], job["url"]]
                new_jobs.append(job)

        if new_jobs:
            print(f"[+] New jobs at {company}: {len(new_jobs)}")
            body = "\n".join([f"{j['title']} - {j['url']}" for j in new_jobs])
            send_email(subject=f"New Jobs at {company}", body=body)
        else:
            print(f"[=] No new jobs at {company}")

    save_seen_jobs(seen_jobs)

if __name__ == "__main__":
    print("[✔] Job Alert Agent started. Running every 60 minutes...")
    while True:
        run_realtime_agent()
        time.sleep(3600)
