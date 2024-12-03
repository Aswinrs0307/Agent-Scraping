# filename: fetch_article.py
import requests
from bs4 import BeautifulSoup

# URL of the article
url = "https://benjaminspall.com/input-output/"

# Fetch the content of the webpage
response = requests.get(url)
web_content = response.content

# Parse the content using BeautifulSoup
soup = BeautifulSoup(web_content, 'html.parser')

# Extract the main content of the article
article_content = soup.find('article')
if article_content:
    text = article_content.get_text()
    # Save the content to a file
    with open("article_content.txt", "w", encoding="utf-8") as file:
        file.write(text)
    print("Article content has been saved to 'article_content.txt'.")
else:
    print("Article content not found.")