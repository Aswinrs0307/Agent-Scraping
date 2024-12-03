# filename: save_results.py
extracted_results = [
    {'Name': 'BLACK JACK SPORTS BETTING', 'Reg. Number': '18831', 'Type': 'Business Name', 'Name Status': 'Current Name', 'Organisation Status': 'Active'}
]

# Save the extracted results to a text file
with open("extracted_results.txt", "w", encoding="utf-8") as file:
    for result in extracted_results:
        file.write(f"Name: {result['Name']}\n")
        file.write(f"Reg. Number: {result['Reg. Number']}\n")
        file.write(f"Type: {result['Type']}\n")
        file.write(f"Name Status: {result['Name Status']}\n")
        file.write(f"Organisation Status: {result['Organisation Status']}\n")
        file.write("\n")  # Add a newline for separation

print("Extracted results saved to extracted_results.txt")