# filename: web_scraping_agent.py

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize the Selenium WebDriver
driver = webdriver.Chrome()

# Open the provided URL
driver.get("https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU")

# Wait for the page to load
time.sleep(5)

# Extract the HTML content of the page
html_content = driver.page_source

# Print the HTML content with proper encoding
print(html_content.encode('utf-8', errors='ignore').decode('utf-8'))

# Close the WebDriver
driver.quit()