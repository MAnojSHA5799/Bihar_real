import pandas as pd
from serpapi import GoogleSearch
import time

# -------------------------------
# Replace with your SerpAPI Key
# -------------------------------
SERPAPI_KEY = "YOUR_SERPAPI_KEY"

# -------------------------------
# Input Data
# -------------------------------
data = [
    {
        "Project Name": "A M PINNACLE",
        "Registration No": "BRERAP00427-9/155/R-1663/2024",
        "Promoter Name": "R.D.ECO DEVELOPERS PVT. LTD.",
        "Address": "",
        "Date": "04 Apr 2024"
    },
    {
        "Project Name": "A ONE HERITAGE",
        "Registration No": "BRERAP00923-1/607/R-783/2019",
        "Promoter Name": "A ONE BUILDERS DEVELOPERS",
        "Address": "NOSHA, PHULWARI SHARIF, Block- Phulwari Sarif Mauja - नोहसा District - PatnaPlot No -437",
        "Date": "17 Oct 2019"
    },
    {
        "Project Name": "A.R GREEN CITY",
        "Registration No": "BRERAP14746-5/100/R-1767/2024",
        "Promoter Name": "PARI CONSTRUCTION AND DEVELOPER",
        "Address": "",
        "Date": "09 Oct 2024"
    }
]

# -------------------------------
# Function to search Google using SerpAPI
# -------------------------------
def get_google_reviews(promoter):

    params = {
        "engine": "google_search",
        "q": promoter,
        "api_key": SERPAPI_KEY,
        "gl": "in",
        "hl": "en",
        "num": "10"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    snippets = []

    # Organic snippets
    if "organic_results" in results:
        for r in results["organic_results"]:
            if "snippet" in r:
                snippets.append(r["snippet"])

    # Related questions
    if "related_questions" in results:
        for q in results["related_questions"]:
            if "snippet" in q:
                snippets.append(q["snippet"])

    # Topbox (possible reviews)
    if "topbox" in results and "reviews" in results["topbox"]:
        for rev in results["topbox"]["reviews"]:
            if "snippet" in rev:
                snippets.append(rev["snippet"])

    return snippets


# -------------------------------
# Main
# -------------------------------

all_reviews = []

for item in data:
    promoter = item["Promoter Name"]
    print(f"Searching for: {promoter}")

    try:
        comments = get_google_reviews(promoter)
    except Exception as e:
        print("Error:", e)
        comments = []

    for comment in comments:
        all_reviews.append({
            "Promoter Name": promoter,
            "Comment": comment
        })

    time.sleep(2)

# Convert to DataFrame
df = pd.DataFrame(all_reviews)

# Save to CSV
df.to_csv("promoter_google_reviews.csv", index=False)

print("Saved reviews to promoter_google_reviews.csv")