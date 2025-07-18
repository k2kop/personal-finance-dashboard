import requests
from bs4 import BeautifulSoup
import json
import os

CACHE_FILE = "data/exchange_rates.json"

def scrape_exchange_rate(base="USD", target="NGN"):
    base = base.upper()
    target = target.upper()
    url = f"https://wise.com/gb/currency-converter/{base}-to-{target}-rate"

    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        rate_span = soup.find("h3", {"data-testid": "exchange-rate"})
        if not rate_span:
            raise ValueError("Could not find exchange rate")

        rate_text = rate_span.text.split(" = ")[1].split(" ")[0].replace(",", "")
        rate = float(rate_text)
        save_rate_to_cache(base, target, rate)
        return rate

    except Exception as e:
        print(f"Error scraping {base} to {target}: {e}")
        return load_rate_from_cache(base, target)

def save_rate_to_cache(base, target, rate):
    os.makedirs("data", exist_ok=True)
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            try:
                cache = json.load(f)
            except:
                cache = {}
    cache[f"{base}_{target}"] = rate
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)

def load_rate_from_cache(base, target):
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            try:
                cache = json.load(f)
                return cache.get(f"{base}_{target}", 1.0)
            except:
                return 1.0
    return 1.0
