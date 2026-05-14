import requests
from bs4 import BeautifulSoup
import json
import time
import os

urls = [
    {"source": "WebMD", "symptom": "headache", "url": "https://www.webmd.com/migraines-headaches/migraines-headaches-basics"},
    {"source": "WebMD", "symptom": "fever", "url": "https://www.webmd.com/covid/what-is-a-fever"},
    {"source": "WebMD", "symptom": "cough", "url": "https://www.webmd.com/cold-and-flu/overview"},
    {"source": "WebMD", "symptom": "fatigue", "url": "https://www.webmd.com/women/features/chronic-fatigue-tired-feeling-tired"},
    {"source": "WebMD", "symptom": "nausea", "url": "https://www.webmd.com/digestive-disorders/digestive-diseases-nausea-vomiting"},
    {"source": "WebMD", "symptom": "stomach pain", "url": "https://www.webmd.com/pain-management/abdominal-pain-causes-treatments"},
    {"source": "WebMD", "symptom": "sore throat", "url": "https://www.webmd.com/cold-and-flu/understanding-sore-throat-basics"},
    {"source": "WebMD", "symptom": "dizziness", "url": "https://www.webmd.com/brain/dizziness-vertigo"},
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

def scrape_page(entry):
    session = requests.Session()
    session.headers.update(headers)
    response = session.get(entry["url"], timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    content = soup.find("main")
    text = content.get_text(separator="\n", strip=True) if content else ""

    return {
        "symptom": entry["symptom"],
        "source": entry["source"],
        "url": entry["url"],
        "content": text
    }

results = []
for entry in urls:
    print(f"Scraping {entry['symptom']} from {entry['source']}...")
    data = scrape_page(entry)
    results.append(data)
    time.sleep(2)

os.makedirs("data", exist_ok=True)
with open("data/webmd_raw_data.json", "w") as f:
    json.dump(results, f, indent=2)

print("Done! Saved to data/webmd_raw_data.json")