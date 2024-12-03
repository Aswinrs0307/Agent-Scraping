# filename: follow_links_selenium.py
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize the WebDriver (make sure to have the appropriate driver installed)
driver = webdriver.Chrome()  # Adjust if using a different browser

try:
    # Load the search results HTML content from the file
    driver.get("file:///path/to/search_results.html")  # Adjust the path to your local file

    # Step 6.1: Locate the relevant link associated with the extracted result
    # Assuming the relevant link is in the same row as the found text
    results = driver.find_elements(By.TAG_NAME, "td")  # Get all table cells

    # Step 6.2: Check for links in the same row as the company name
    for td in results:
        if "BANK OF CYPRUS PUBLIC COMPANY LIMITED" in td.text:
            # Find the link in the same row
            link = td.find_element(By.TAG_NAME, "a")
            if link:
                detail_url = link.get_attribute("href")
                print(f"Found link to details: {detail_url}")

                # Fetch the details from the link
                driver.get(detail_url)
                time.sleep(5)  # Wait for the page to load

                # Save the details to a file
                detail_html = driver.page_source
                with open("company_details.html", "w", encoding="utf-8") as detail_file:
                    detail_file.write(detail_html)
                print("Company details successfully written to company_details.html")
                break  # Exit after finding the first relevant link

finally:
    driver.quit()