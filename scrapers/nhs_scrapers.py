import requests
from bs4 import BeautifulSoup
import json
import time

urls = [
    {"source": "NHS", "symptom": "headache", "url": "https://www.nhs.uk/conditions/headaches/"},
    {"source": "NHS", "symptom": "cough", "url": "https://www.nhs.uk/conditions/cough/"},
    {"source": "NHS", "symptom": "fever", "url": "https://www.nhs.uk/symptoms/fever-in-adults/"},
    {"source": "NHS", "symptom": "fatigue", "url": "https://www.nhs.uk/symptoms/tiredness-and-fatigue/"},
    {"source": "NHS", "symptom": "nausea", "url": "https://www.nhs.uk/symptoms/feeling-sick-nausea/"},
    {"source": "NHS", "symptom": "stomach pain", "url": "https://www.nhs.uk/conditions/stomach-ache/"},
    {"source": "NHS", "symptom": "sore throat", "url": "https://www.nhs.uk/conditions/sore-throat/"},
    {"source": "NHS", "symptom": "dizziness", "url": "https://www.nhs.uk/conditions/dizziness/"},
]

def scrape_page(entry):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}
    response = requests.get(entry["url"], headers=headers)
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
    time.sleep(1)

with open("data/nhs_raw_data.json", "w") as f:
    json.dump(results, f, indent=2)

print("Done! Saved to data/nhs_raw_data.json")