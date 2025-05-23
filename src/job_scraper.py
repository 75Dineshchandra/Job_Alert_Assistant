# job_scraper.py
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_linkedin_jobs(base_url):
    print("[~] Scraping LinkedIn with dynamic pagination...")
    jobs = []

    for page in range(0, 20):  # Try up to 20 pages
        paged_url = base_url + f"&start={page * 25}"
        print(f"    → Page {page+1}: {paged_url}")
        res = requests.get(paged_url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")

        listings = soup.find_all("a", {"data-tracking-control-name": "public_jobs_jserp-result_search-card"})

        if not listings:
            print(f"    → No jobs found on page {page+1}. Stopping.")
            break

        for link in listings:
            title = link.get_text(strip=True)
            href = link['href']
            jobs.append({
                "title": title,
                "url": href,
                "location": "N/A"
            })

    return jobs

def scrape_jobs_from_url(url):
    print(f"[~] Generic scrape: {url}")
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        links = soup.find_all("a", href=True)

        jobs = []
        for link in links:
            title = link.get_text(strip=True)
            href = link["href"]

            if title and ("job" in href.lower() or "careers" in href.lower()):
                jobs.append({
                    "title": title,
                    "url": href if href.startswith("http") else url.rstrip("/") + "/" + href,
                    "location": "N/A"
                })
        return jobs
    except Exception as e:
        print(f"[✘] Failed to scrape {url}: {e}")
        return []
