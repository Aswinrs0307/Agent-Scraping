# filename: fetch_article.py
import requests
from bs4 import BeautifulSoup

# Fetch the content of the article
url = "https://benjaminspall.com/input-output/"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the main content of the article
article_content = soup.find('article').get_text()

# Save the content to a file to avoid encoding issues
with open("article_content.txt", "w", encoding="utf-8") as file:
    file.write(article_content)

print("Article content has been saved to 'article_content.txt'")