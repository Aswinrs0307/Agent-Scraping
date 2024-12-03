# filename: print_html_content.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize the WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU")

# Wait for the page to load completely
time.sleep(10)

# Get the HTML content of the page
html_content = driver.page_source

# Save the HTML content to a file
with open("page_content.html", "w", encoding="utf-8") as file:
    file.write(html_content)

# Close the browser
driver.quit()