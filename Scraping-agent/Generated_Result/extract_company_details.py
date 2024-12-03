# filename: extract_company_details.py
from bs4 import BeautifulSoup

# Update the path to the actual location of company_details.html
file_path = r"C:\Users\aswin.rs\Documents\company_details.html"  # Adjust this path

# Load the company details HTML content from the file
with open(file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Step 7: Extract common details
company_info = {}

# Example extraction (adjust selectors based on actual HTML structure)
company_info['name'] = soup.find(text="Company Name").find_next().text.strip() if soup.find(text="Company Name") else "N/A"
company_info['registration_number'] = soup.find(text="Registration Number").find_next().text.strip() if soup.find(text="Registration Number") else "N/A"
company_info['address'] = soup.find(text="Address").find_next().text.strip() if soup.find(text="Address") else "N/A"
company_info['contact'] = soup.find(text="Contact").find_next().text.strip() if soup.find(text="Contact") else "N/A"

# Print the extracted company information
print("Extracted Company Information:")
for key, value in company_info.items():
    print(f"{key}: {value}")