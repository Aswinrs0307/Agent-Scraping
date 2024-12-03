# filename: test_scrape_bank_of_cyprus.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def log(message):
    print(f"[LOG] {message}")

try:
    # Set up headless Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")

    # Step 1: Load the web page using Selenium
    url = "https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU"
    driver = webdriver.Chrome(options=chrome_options)  # Ensure you have the ChromeDriver installed and in your PATH
    driver.get(url)
    log("Web page loaded successfully.")

    # Wait for the page to be fully loaded
    WebDriverWait(driver, 10).until(lambda d: d.execute_script('return document.readyState') == 'complete')
    log("Page fully loaded.")

    # Capture and save the HTML content to a file
    page_source = driver.page_source
    with open("page_source.html", "w", encoding="utf-8") as file:
        file.write(page_source)
    log("HTML content saved to page_source.html")

    # Extract the page source and parse it with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Step 2: Extract the IDs, names, and class names of the text fields for searching input
    input_fields = soup.find_all('input', {'type': 'text'})
    for field in input_fields:
        log(f"ID: {field.get('id')}, Name: {field.get('name')}, Class: {field.get('class')}")

    # Step 3: Identify and click the search button using Selenium
    # Find the search input field and enter the company name
    try:
        search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_txtName')))
        search_input.send_keys("BANK OF CYPRUS PUBLIC COMPANY LIMITED")
        log("Search input field located and company name entered.")
    except Exception as e:
        log(f"Error locating search input field: {e}")
        driver.save_screenshot("error_screenshot.png")
        log("Screenshot saved as error_screenshot.png")
        driver.quit()
        exit(1)

    # Find the search button and click it
    try:
        search_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_btnSearch')))
        search_button.click()
        log("Search button located and clicked.")
    except Exception as e:
        log(f"Error locating search button: {e}")
        driver.save_screenshot("error_screenshot.png")
        log("Screenshot saved as error_screenshot.png")
        driver.quit()
        exit(1)

    driver.quit()
except Exception as e:
    log(f"An error occurred: {e}")
    driver.save_screenshot("error_screenshot.png")
    log("Screenshot saved as error_screenshot.png")