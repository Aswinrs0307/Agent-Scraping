# filename: web_scraping.py

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Using Selenium to interact with the webpage
driver = webdriver.Chrome()  # Ensure you have the ChromeDriver installed and in your PATH
driver.get("https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU")

# Wait for the page to load
time.sleep(5)

# Step 4: Perform Search Action
search_term = "BANK OF CYPRUS PUBLIC COMPANY LIMITED"

# Replace <SEARCH_INPUT_ID> with the actual ID or name of the search input field
search_input = driver.find_element(By.ID, '<SEARCH_INPUT_ID>')
search_input.send_keys(search_term)

# Replace <SEARCH_BUTTON_ID> with the actual ID or name of the search button
search_button = driver.find_element(By.ID, '<SEARCH_BUTTON_ID>')
search_button.click()

# Wait for the results to load
time.sleep(5)

# Step 5: Handle Search Results
results_page_html = driver.page_source
results_soup = BeautifulSoup(results_page_html, 'html.parser')

# Step 6: Extract Details
results = results_soup.find_all('div', {'class': 'result'})  # Assuming results are in divs with class 'result'

# Print the results
print("\nSearch Results:")
for result in results:
    print(result.text.strip())

# Close the browser
driver.quit()