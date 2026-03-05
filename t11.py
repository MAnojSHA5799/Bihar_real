import requests
import math
import json

API_KEY = "e145e0bf1bbcdc1daf0505b5a265f850b80678e2"

class DynamicGeofencingBihar:

    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://google.serper.dev/maps"

    # -------------------------------------------------
    # Fetch Locations
    # -------------------------------------------------
    def get_live_locations(self, city="Patna"):

        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "q": f"car showrooms in {city}, Bihar",
            "gl": "in",
            "hl": "en",
            "num": 20
        }

        response = requests.post(self.url, headers=headers, json=payload)

        if response.status_code != 200:
            print("❌ API ERROR:", response.text)
            return []

        data = response.json()

        # Handle both response types
        places = data.get("places") or data.get("maps") or []

        print(f"\n📡 Total Results Found: {len(places)}\n")

        return places

    # -------------------------------------------------
    # Distance Formula
    # -------------------------------------------------
    def haversine(self, lat1, lon1, lat2, lon2):
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)

        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * \
            math.cos(math.radians(lat2)) * math.sin(dlon/2)**2

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c

    # -------------------------------------------------
    # Print Locations With Coordinates
    # -------------------------------------------------
    def find_sale_hotspots(self, user_lat, user_lon, city="Patna"):

        places = self.get_live_locations(city)

        if not places:
            print("⚠️ No data received from API")
            return

        print("📍 LOCATION LIST WITH COORDINATES")
        print("=" * 100)

        for place in places:

            # Safe name handling
            name = (
                place.get("title") or
                place.get("name") or
                place.get("businessName") or
                "UNKNOWN NAME"
            )

            address = place.get("address", "N/A")
            rating = place.get("rating", "N/A")
            reviews = place.get("reviewsCount", "N/A")

            # Coordinate extraction
            lat = None
            lon = None

            if "gpsCoordinates" in place:
                lat = place["gpsCoordinates"].get("latitude")
                lon = place["gpsCoordinates"].get("longitude")

            elif "latitude" in place and "longitude" in place:
                lat = place.get("latitude")
                lon = place.get("longitude")

            # Convert to float if possible
            if lat and lon:
                try:
                    lat = float(lat)
                    lon = float(lon)
                    distance = round(self.haversine(user_lat, user_lon, lat, lon), 2)
                except:
                    distance = "Invalid coords"
            else:
                distance = "No coords"

            print(f"📍 Name        : {name}")
            print(f"   Address     : {address}")
            print(f"   Rating      : {rating}")
            print(f"   Reviews     : {reviews}")
            print(f"   Latitude    : {lat}")
            print(f"   Longitude   : {lon}")
            print(f"   Distance    : {distance} KM")
            print("-" * 100)


# -------------------------------------------------
# MAIN
# -------------------------------------------------
if __name__ == "__main__":

    print("🚀 Running Bihar Sales Hotspot Tracker...\n")

    tracker = DynamicGeofencingBihar(API_KEY)

    # Bailey Road Patna Coordinates
    user_lat = 25.6105
    user_lon = 85.0841

    tracker.find_sale_hotspots(user_lat, user_lon, "Patna")