from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import pandas as pd

# Load your API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EXCEL_PATH = "data/Top_50_S&P_Companies_Data_AI_Networking.xlsx"
OUTPUT_JSON = "data/career_urls.json"

def ask_llm_for_url(company):
    prompt = (
        f"What is the official career page URL of the company '{company}'? "
        "Only return the URL without any extra text or explanation."
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # or "gpt-3.5-turbo" to reduce cost
            messages=[
                {"role": "system", "content": "You are a helpful assistant that returns only URLs."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[✘] LLM failed for {company}: {e}")
        return None

def resolve_all():
    df = pd.read_excel(EXCEL_PATH)
    companies = [name.split(" (")[0].strip() for name in df["Company"].dropna().unique()]
    
    result = {}
    for company in companies:
        print(f"[...] Querying LLM for: {company}")
        url = ask_llm_for_url(company)
        if url and url.startswith("http"):
            print(f"[✔] {company}: {url}")
            result[company] = url
        else:
            print(f"[✘] {company}: Not found")
            result[company] = None

    with open(OUTPUT_JSON, "w") as f:
        json.dump(result, f, indent=2)

if __name__ == "__main__":
    resolve_all()
