import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

locations = [
    "Bihta Airport Patna",
    "AIIMS Patna",
    "IIT Patna",
    "Danapur Station Patna",
    "Patna Airport"
]

foreign_keywords = [
    "russia","japan","usa","uae","singapore",
    "china","uk","germany","france",
    "fdi","foreign investment",
    "international","kra","agreement"
]

countries = [
    "Russia","Japan","USA","UAE",
    "Singapore","China","UK",
    "Germany","France"
]

def detect_country(text):
    for c in countries:
        if c.lower() in text.lower():
            return c
    return "N/A"

def extract_amount(text):
    match = re.search(r'₹?\s?[\d,]+\s?(crore|billion)?', text.lower())
    return match.group() if match else "N/A"

def search_and_scrape(location):
    
    search_url = f"https://www.bing.com/search?q={location.replace(' ','+') }+foreign+investment+news"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a")
    
    foreign_news = "No international news found"
    country = "N/A"
    amount = "N/A"

    for link in links:
        url = link.get("href")
        
        if url and url.startswith("http"):
            try:
                article = requests.get(url, headers=headers, timeout=5)
                article_soup = BeautifulSoup(article.text, "html.parser")
                text = article_soup.get_text().lower()

                if any(word in text for word in foreign_keywords):
                    foreign_news = link.text.strip()
                    country = detect_country(text)
                    amount = extract_amount(text)
                    break

            except:
                continue

    return foreign_news, country, amount


final_data = []

for loc in locations:
    print(f"Checking {loc}...")
    news, country, amount = search_and_scrape(loc)

    final_data.append([loc, news, country, amount])
    time.sleep(2)

df = pd.DataFrame(final_data, columns=[
    "Location",
    "International / Foreign News",
    "Country Detected",
    "Investment Amount"
])

print("\n===== INTERNATIONAL REPORT =====\n")
print(df)

df.to_excel("Deep_Foreign_Investment_Report.xlsx", index=False)
print("\nExcel Saved: Deep_Foreign_Investment_Report.xlsx")