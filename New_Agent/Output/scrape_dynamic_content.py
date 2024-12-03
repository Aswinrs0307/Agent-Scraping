# filename: scrape_dynamic_content.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

# Step 1: Set up the Selenium WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Step 2: Open the webpage
url = "https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU"
driver.get(url)

# Wait for a few seconds to ensure the page loads completely
time.sleep(5)

# Take a screenshot to see the loaded page
driver.save_screenshot('screenshot.png')

# Save the page source to an HTML file for further analysis
with open('page_source.html', 'w', encoding='utf-8') as file:
    file.write(driver.page_source)

# Close the browser
driver.quit()

print("Screenshot saved as 'screenshot.png' and page source saved as 'page_source.html'.")