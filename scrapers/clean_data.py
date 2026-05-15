import json
import re
import os

with open("data/combined_data.json", "r") as f:
    data = json.load(f)

def clean_text(text):
    # Remove excessive newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Remove weird encoded characters
    text = text.replace('\u00c2', '').replace('\u00a0', ' ')
    # Remove extra whitespace
    text = re.sub(r' {2,}', ' ', text)
    # Strip leading/trailing whitespace
    text = text.strip()
    return text

cleaned = []
for entry in data:
    cleaned.append({
        "symptom": entry["symptom"],
        "source": entry["source"],
        "url": entry["url"],
        "content": clean_text(entry["content"])
    })

os.makedirs("data", exist_ok=True)
with open("data/cleaned_data.json", "w") as f:
    json.dump(cleaned, f, indent=2)

print(f"Cleaned {len(cleaned)} documents saved to data/cleaned_data.json")