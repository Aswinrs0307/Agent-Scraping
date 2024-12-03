# filename: save_results_json.py
import json

# Data to be saved
data = [
    {
        "Company Name": "BANK OF CYPRUS PUBLIC COMPANY LIMITED",
        "Registration Number": "165",
        "Type": "Limited Company",
        "Current Name Status": "Active",
        "Last Updated": "26/11/2024"
    }
]

# Save to JSON
with open("search_results.json", "w", encoding='utf-8') as jsonfile:
    json.dump(data, jsonfile, ensure_ascii=False, indent=4)

print("Data saved to search_results.json.")