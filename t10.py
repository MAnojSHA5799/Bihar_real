import requests
import json
import pandas as pd
import time

# 🛠️ APNI API KEY YAHAN DALAIN
SERPER_API_KEY = "e145e0bf1bbcdc1daf0505b5a265f850b80678e2"

class BiharCarScraperDebug:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://google.serper.dev/maps"
        self.all_dealers = []
        # Chhote districts ko abhi side rakhte hain, pehle Patna/Gaya check karte hain
        self.districts = ["Patna", "Gaya", "Muzaffarpur", "Bhagalpur"]
        self.brands = ["Maruti Suzuki", "Hyundai", "Tata Motors"]

    def fetch(self):
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }

        for city in self.districts:
            for brand in self.brands:
                query = f"{brand} showroom in {city} Bihar"
                print(f"🔍 Searching for: {query}")
                
                payload = json.dumps({"q": query})
                response = requests.post(self.url, headers=headers, data=payload)
                
                # --- DEBUGGING START ---
                if response.status_code != 200:
                    print(f"❌ API Error: Status {response.status_code}. Message: {response.text}")
                    continue
                
                results = response.json()
                # Serper kabhi 'maps' deta hai, kabhi 'places'
                places = results.get('maps') or results.get('places') or []
                
                if not places:
                    # Agar 'maps' nahi hai, toh check karein 'organic' results to nahi aa rahe?
                    print(f"⚠️ No map results for {query}. Checking total keys: {list(results.keys())}")
                else:
                    print(f"✅ Found {len(places)} showrooms!")
                    for p in places:
                        self.all_dealers.append({
                            "Name": p.get("title"),
                            "Address": p.get("address"),
                            "Phone": p.get("phoneNumber", "N/A"),
                            "City": city,
                            "Brand": brand
                        })
                # --- DEBUGGING END ---
                time.sleep(1)

    def save(self):
        if self.all_dealers:
            df = pd.DataFrame(self.all_dealers)
            df.to_excel("Bihar_Showrooms_Debug.xlsx", index=False)
            print(f"\n🎉 Success! {len(df)} entries saved.")
        else:
            print("\n💀 Koi data nahi mila. Check if your API credits are exhausted.")

if __name__ == "__main__":
    if SERPER_API_KEY == "YOUR_SERPER_API_KEY_HERE":
        print("🛑 API Key daalna bhool gaye aap!")
    else:
        scraper = BiharCarScraperDebug(SERPER_API_KEY)
        scraper.fetch()
        scraper.save()