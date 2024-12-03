from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up Selenium WebDriver (ensure the path to chromedriver is correct)
driver = webdriver.Chrome()

# Open the target page
driver.get("https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchResults.aspx?name=BLACK%20JACK%20SPORTS%20BETTING&number=%25&searchtype=optStartMatch&index=1&tname=%25&sc=0")

# Wait for the page to load completely
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Select')]")))

# Find the 'Select' link
select_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Select')]")

# Use JavaScript to click the link if normal click isn't working
driver.execute_script("arguments[0].click();", select_link)

# Wait for the page to load after clicking
# Use WebDriverWait to ensure that new content is loaded after the click
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'new_content')]")))

# Now that the page is loaded, you can proceed to scrape or interact with other elements
# For example, let's print the title of the page after the click
print("Page title after click:", driver.title)

# Close the browser after scraping
driver.quit()
