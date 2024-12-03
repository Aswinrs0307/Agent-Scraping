# 1. pip install selenium
#    pip install beautifulsoup4

# 2. **Download the appropriate WebDriver** for your browser (e.g., ChromeDriver for Google Chrome) and ensure it is in your system's PATH.

# 3. **Write the Python script**:

# ```python
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup

# # Set up the WebDriver
# driver = webdriver.Chrome()  # or use the appropriate WebDriver for your browser
# driver.get("https://efiling.drcor.mcit.gov.cy/")

# # Select language as "English"
# english_button = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'English')]"))
# )
# english_button.click()

# # Navigate to the search tab
# search_tab = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Search')]"))
# )
# search_tab.click()

# # Choose "with all these words"
# search_criteria = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "//select[@name='criteria']/option[text()='with all these words']"))
# )
# search_criteria.click()

# # Type "cedar rose" in the Name field
# name_field = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.NAME, "name"))
# )
# name_field.send_keys("cedar rose")

# # Click the "Go" button
# go_button = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "//input[@value='Go']"))
# )
# go_button.click()

# # Wait for the table to load and extract the data
# table = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.XPATH, "//table[@class='results']"))
# )

# # Parse the table with BeautifulSoup
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# table = soup.find('table', {'class': 'results'})

# # Extract the required data
# data = []
# for row in table.find_all('tr')[1:]:  # Skip the header row
#     cols = row.find_all('td')
#     data.append({
#         "Name": cols[0].text.strip(),
#         "Reg. Number": cols[1].text.strip(),
#         "Type": cols[2].text.strip(),
#         "Name Status": cols[3].text.strip(),
#         "Organisation Status": cols[4].text.strip(),
#     })

# # Close the WebDriver
# driver.quit()

# # Print the extracted data
# for entry in data:
#     print(entry)
# ```

# This script will open the specified URL, change the language to English, navigate to the search tab, perform the search with the criteria provided, and extract the required data from the resulting table.

# Please note that web scraping should be done in compliance with the website's terms of service and robots.txt file. Always ensure you have permission to scrape the data from the website.
