import json
import os

with open("data/nhs_raw_data.json", "r") as f:
    nhs_data = json.load(f)

with open("data/webmd_raw_data.json", "r") as f:
    webmd_data = json.load(f)

webmd_filtered = [entry for entry in webmd_data if entry["content"] and "POPULAR ON WEBMD" not in entry["content"]]

combined = nhs_data + webmd_filtered

with open("data/combined_data.json", "w") as f:
    json.dump(combined, f, indent=2)

print(f"Total documents: {len(combined)}")