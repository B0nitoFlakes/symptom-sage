import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

with open("data/cleaned_data.json", "r") as f:
    data = json.load(f)

def generate_pairs(entry):
    prompt = f"""
You are a medical knowledge extractor. Based on the following medical content about {entry['symptom']}, 
generate 5 structured JSON entries.

CRITICAL RULES - YOU MUST FOLLOW THESE EXACTLY:
1. Every entry MUST have EXACTLY these 7 keys, nothing more, nothing less:
   - "symptom"
   - "possible_condition"
   - "description"
   - "advice" (NOT "advise", NOT "advices", NOT "advice_given" - ONLY "advice")
   - "when_to_see_doctor"
   - "source"
   - "url"

2. The key "advice" must be spelled exactly as: a-d-v-i-c-e
3. NEVER use "advise" - this is WRONG and will break the system
4. Return ONLY a JSON array of 5 entries. No explanation, no markdown, no backticks.

Each entry must follow this exact format:
{{
  "symptom": "{entry['symptom']}",
  "possible_condition": "name of condition",
  "description": "brief description of the condition and how it relates to the symptom",
  "advice": "what the person should do",
  "when_to_see_doctor": "specific warning signs that require medical attention",
  "source": "{entry['source']}",
  "url": "{entry['url']}"
}}

Medical content:
{entry['content'][:3000]}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user", "content":prompt}],
        temperature=0.3
    )

    text = response.choices[0].message.content.strip()
    return json.loads(text)

all_pairs = []
for entry in data:
    print(f"Generating pairs for {entry['symptom']} from {entry['source']}...")
    try:
        pairs = generate_pairs(entry)
        all_pairs.extend(pairs)
    except Exception as e:
        print(f"Error for {entry['symptom']} from {entry['source']}: {e}")

with open("data/generated_pairs.json", "w") as f:
    json.dump(all_pairs, f, indent=2)

print(f"Total pairs generated: {len(all_pairs)}")
print("Saved to data/generated_pairs.json")

