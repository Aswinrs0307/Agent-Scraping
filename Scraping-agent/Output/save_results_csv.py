# filename: save_results_csv.py
import csv

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

# Save to CSV
with open("search_results.csv", "w", newline='', encoding='utf-8') as csvfile:
    fieldnames = data[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for entry in data:
        writer.writerow(entry)

print("Data saved to search_results.csv.")