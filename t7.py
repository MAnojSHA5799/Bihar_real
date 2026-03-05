# ==========================================
# PATNA SMART INVESTMENT & DEVELOPMENT ANALYZER
# ==========================================

import pandas as pd
from gnews import GNews
import time

# ==========================================
# BASE DATA
# ==========================================

base_data = [
    ["Bihta Airport Patna", "40L", "Commercial Hub, Mall, Hotel, Logistics Park", "45L", "51L", "58L", "75-80L"],
    ["Bhita Chowk Patna", "32L", "High Commercial Growth", "36L", "41L", "46L", "60-65L"],
    ["AIIMS Patna", "32L", "PG, Hostel, Medical Retail Growth", "35L", "39L", "43L", "55-60L"],
    ["IIT Patna", "28L", "Student Housing & Rental Demand", "31L", "34L", "38L", "48-52L"],
    ["Danapur Station Patna", "26L", "Strong Residential + Retail", "29L", "32L", "36L", "46-50L"],
    ["Shivala Golambar Patna", "22L", "Suburban Commercial Zone", "24L", "27L", "30L", "38-42L"],
    ["Phase-1 Pink City Bihta", "18L", "Planned Colony Demand", "20L", "22L", "24L", "30-34L"],
    ["Jaitipur Block B Patna", "17L", "Long-Term Investment Zone", "18.5L", "20L", "22L", "28-30L"],
    ["Goal Township Bihta", "22L", "Gated Society Growth", "24L", "26L", "29L", "36-40L"],
    ["Kanhalu Golambar Patna", "17L", "Mid-Level Growth", "18.5L", "20L", "22L", "28-30L"],
    ["Nandi Gram Bihta", "13L", "Urban Conversion Potential", "14L", "15L", "16.5L", "20-22L"],
    ["Gokul Gram Bihta", "13L", "Low Entry Long-Term ROI", "14L", "15L", "16.5L", "20-22L"],
    ["Woodden World Bihta", "27L", "Resort / Commercial Potential", "30L", "33L", "37L", "48-52L"],
    ["Patna Airport", "70L", "Stable but Slower Growth", "74L", "79L", "84L", "95L-1Cr"]
]

# ==========================================
# GOOGLE NEWS SETUP
# ==========================================

google_news = GNews(language='en', country='IN', max_results=8)

# ==========================================
# KEYWORDS
# ==========================================

development_keywords = [
    "development", "project", "expansion", "construction",
    "infrastructure", "airport", "road", "highway",
    "metro", "industrial", "township"
]

investment_keywords = [
    "investment", "invest", "company", "foreign",
    "mnc", "factory", "plant", "logistics park",
    "industrial park", "signed", "mou", "crore",
    "billion", "deal"
]

# ==========================================
# SMART NEWS FUNCTION
# ==========================================

def get_smart_news(location):
    try:
        query = f"{location} development investment project"
        news = google_news.get_news(query)

        development_news = []
        investment_news = []

        for n in news:
            title_lower = n["title"].lower()

            if any(word in title_lower for word in development_keywords):
                development_news.append(n["title"])

            if any(word in title_lower for word in investment_keywords):
                investment_news.append(n["title"])

        # fallback if empty
        if not development_news and not investment_news:
            fallback = google_news.get_news("Patna industrial investment development")
            for n in fallback:
                title_lower = n["title"].lower()

                if any(word in title_lower for word in development_keywords):
                    development_news.append(n["title"])

                if any(word in title_lower for word in investment_keywords):
                    investment_news.append(n["title"])

        combined = development_news[:2] + investment_news[:2]

        return " | ".join(combined) if combined else "No major development or investment news found"

    except:
        return "News fetch error"

# ==========================================
# MAIN PROCESS
# ==========================================

final_data = []

for row in base_data:
    location = row[0]
    print(f"Fetching smart news for {location}...")
    
    smart_news = get_smart_news(location)
    
    final_data.append([
        location,
        row[1],
        smart_news,
        row[2],
        row[3],
        row[4],
        row[5],
        row[6]
    ])
    
    time.sleep(2)

# ==========================================
# CREATE TABLE
# ==========================================

columns = [
    "Location",
    "Current Avg Rate",
    "Development / Company Investment News",
    "Future Impact",
    "1 Year",
    "2 Year",
    "3 Year",
    "5 Year"
]

df = pd.DataFrame(final_data, columns=columns)

print("\n===== PATNA SMART INVESTMENT TABLE =====\n")
print(df)

# ==========================================
# EXPORT TO EXCEL
# ==========================================

file_name = "Patna_Smart_Investment_Report.xlsx"
df.to_excel(file_name, index=False)

print(f"\nExcel File Saved Successfully: {file_name}")