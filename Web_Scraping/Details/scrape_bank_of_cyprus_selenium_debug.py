# filename: scrape_bank_of_cyprus_selenium_debug.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up the Selenium WebDriver (make sure you have the appropriate WebDriver installed, e.g., chromedriver)
driver = webdriver.Chrome()

# Open the website
driver.get("https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU")

# Wait for the page to load completely
time.sleep(10)

try:
    # Print the page source for debugging
    page_source = driver.page_source
    with open('page_source.html', 'w', encoding='utf-8') as file:
        file.write(page_source)
    print("Page source has been saved to 'page_source.html'.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()