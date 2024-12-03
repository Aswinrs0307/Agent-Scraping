# filename: get_gold_rate_yahoo_fin.py
import yfinance as yf

# Get the gold price in USD per ounce
gold_data = yf.Ticker("GC=F")
gold_price_usd_per_ounce = gold_data.history(period="1d")['Close'][0]

# Convert the gold price to INR per gram
usd_to_inr = 82.0  # Approximate conversion rate, you can update this with the latest rate
grams_per_ounce = 31.1035
gold_price_inr_per_gram = (gold_price_usd_per_ounce * usd_to_inr) / grams_per_ounce

print(f"Today's gold rate in Tamil Nadu: {gold_price_inr_per_gram:.2f} INR per gram")