# filename: gold_rate_chennai.py

import requests
from bs4 import BeautifulSoup

def get_gold_rate():
    url = "https://www.goldratetoday.com/gold-rate-in-chennai/"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        gold_rate_section = soup.find('div', class_='gold-rate-today')
        if gold_rate_section:
            gold_rate = gold_rate_section.find('span', class_='gold-rate').text.strip()
            return gold_rate
        else:
            return "Gold rate section not found"
    else:
        return "Failed to retrieve data"

if __name__ == "__main__":
    gold_rate = get_gold_rate()
    print(f"Today's gold rate in Chennai: {gold_rate}")