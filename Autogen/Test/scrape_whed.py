# filename: scrape_whed.py

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Open the main page
    driver.get("https://whed.net/home.php#:~:text=World%20Higher%20Education%20Database%20(WHED)%20Portal")

    # Find and click the "List of IAU Members Organizations" link
    link = driver.find_element(By.LINK_TEXT, "List of IAU Members Organizations")
    link.click()

    # Wait for the new page to load
    time.sleep(5)

    # Find the search input field and enter "medical"
    search_input = driver.find_element(By.NAME, "search")
    search_input.send_keys("medical")
    search_input.send_keys(Keys.RETURN)

    # Wait for the search results to load
    time.sleep(5)

    # Retrieve the first result from the search results
    first_result = driver.find_element(By.CSS_SELECTOR, ".result-item")
    first_result_text = first_result.text

    # Save the retrieved information into a text file
    with open("search_result.txt", "w") as file:
        file.write(first_result_text)

    print("Search result has been saved to search_result.txt")

finally:
    # Close the WebDriver
    driver.quit()