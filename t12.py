import requests
import json
import pandas as pd
import time

API_KEY = "e145e0bf1bbcdc1daf0505b5a265f850b80678e2"

class BiharUpcomingEvents:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://google.serper.dev/search"
        self.all_events = []

        self.cities = [
            "Patna",
            "Muzaffarpur",
            "Gaya",
            "Bhagalpur",
            "Darbhanga"
        ]

        self.keywords = [
            "upcoming events 2026",
            "expo 2026",
            "trade fair 2026",
            "exhibition 2026",
            "conference 2026",
            "workshop 2026"
        ]

    def fetch_events(self):
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

        for city in self.cities:
            for keyword in self.keywords:
                query = f"{keyword} in {city}, Bihar"
                print(f"🔍 Searching: {query}")

                payload = json.dumps({"q": query})

                try:
                    response = requests.post(self.url, headers=headers, data=payload)
                    data = response.json()
                    results = data.get("organic", [])

                    for event in results:
                        self.all_events.append({
                            "Event_Name": event.get("title"),
                            "Location": city,
                            "Link": event.get("link")
                        })

                    time.sleep(1)

                except Exception as e:
                    print("❌ Error:", e)

    def save_data(self):
        if self.all_events:
            df = pd.DataFrame(self.all_events)
            df = df.drop_duplicates(subset=["Event_Name"])
            df.to_excel("Bihar_Upcoming_Events_2026.xlsx", index=False)
            print(f"\n✅ Total {len(df)} Events Saved!")
            return df
        else:
            print("❌ No events found")
            return None


if __name__ == "__main__":
    scraper = BiharUpcomingEvents(API_KEY)
    scraper.fetch_events()
    df = scraper.save_data()

    if df is not None:
        print(df.head(10))