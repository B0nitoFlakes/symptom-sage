import json
import os

def chunk_document(entry):
    chunk_text = f"""
Symptom: {entry['symptom']}
Possible Condition: {entry['possible_condition']}
Description: {entry['description']}
Advice: {entry['advice']}
When to See Doctor: {entry['when_to_see_doctor']}
    """.strip()

    return {
        "text": chunk_text,
        "metadata": {
            "symptom": entry["symptom"],
            "possible_condition": entry["possible_condition"],
            "source": entry["source"],
            "url": entry["url"]
        }
    }

def chunk_all(input_path, output_path):
    with open(input_path, "r") as f:
        data = json.load(f)
    
    chunks = [chunk_document(entry) for entry in data]

    with open(output_path, "w") as f:
        json.dump(chunks, f, indent=2)

    print(f"Total chunks created: {len(chunks)}")
    return chunks

if__name__ = "__main__"

chunk_all(
    input_path="data/generated_pairs.json",
    output_path="data/chunks.json"
)