import requests
import pandas as pd
import time

# -----------------------------
# Overpass API Servers (Backup)
# -----------------------------
OVERPASS_SERVERS = [
    "https://overpass-api.de/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
]

# -----------------------------
# Bihar Government + Bank + Expanded Govt Offices
# -----------------------------
query = """
[out:json][timeout:300];

area["name"="Bihar"]["boundary"="administrative"]["admin_level"="4"]->.state;

(
  /* Banks */
  node(area.state)["amenity"="bank"];
  way(area.state)["amenity"="bank"];
  relation(area.state)["amenity"="bank"];

  /* General Government Offices */
  node(area.state)["office"="government"];
  way(area.state)["office"="government"];
  relation(area.state)["office"="government"];

  node(area.state)["government"="*"];
  way(area.state)["government"="*"];

  /* Agriculture Department */
  node(area.state)["office"="agricultural"];
  way(area.state)["office"="agricultural"];

  node(area.state)["government"="agriculture"];
  way(area.state)["government"="agriculture"];

  /* JEEViKA (BRLPS) */
  node(area.state)["name"~"JEEViKA|BRLPS", i];
  way(area.state)["name"~"JEEViKA|BRLPS", i];

  /* Court */
  node(area.state)["amenity"="courthouse"];
  way(area.state)["amenity"="courthouse"];

  /* Post Office */
  node(area.state)["amenity"="post_office"];
  way(area.state)["amenity"="post_office"];

  /* Town Hall / Municipality */
  node(area.state)["amenity"="townhall"];
  way(area.state)["amenity"="townhall"];

  /* Panchayat Office */
  node(area.state)["office"="panchayat"];
  way(area.state)["office"="panchayat"];

  /* Electricity / Power */
  node(area.state)["power"="substation"];
  way(area.state)["power"="substation"];

  /* Water Works */
  node(area.state)["man_made"="water_works"];
  way(area.state)["man_made"="water_works"];

  /* Transport Office */
  node(area.state)["amenity"="vehicle_inspection"];
  way(area.state)["amenity"="vehicle_inspection"];

  /* Forest Department */
  node(area.state)["office"="forestry"];
  way(area.state)["office"="forestry"];

  /* ============================= */
  /* 🚗 CAR SHOWROOMS ADDED */
  /* ============================= */

  node(area.state)["shop"="car"];
  way(area.state)["shop"="car"];
  relation(area.state)["shop"="car"];

  node(area.state)["shop"="car_repair"];
  way(area.state)["shop"="car_repair"];
);

out center;
"""

# -----------------------------
# Fetch Data
# -----------------------------
response = None
for server in OVERPASS_SERVERS:
    try:
        print("Connecting to:", server)
        response = requests.post(server, data={"data": query}, timeout=300)
        if response.status_code == 200:
            print("✅ Connected Successfully")
            break
    except Exception as e:
        print("❌ Server Failed:", e)

if not response:
    print("❌ All servers failed")
    exit()

data = response.json()
places = []

# -----------------------------
# Extract Data
# -----------------------------
for element in data.get("elements", []):
    tags = element.get("tags", {})

    name = tags.get("name", "N/A")

    place_type = (
        tags.get("amenity")
        or tags.get("office")
        or tags.get("government")
        or tags.get("power")
        or tags.get("man_made")
        or "N/A"
    )

    lat = element.get("lat") or element.get("center", {}).get("lat")
    lon = element.get("lon") or element.get("center", {}).get("lon")

    places.append({
        "Name": name,
        "Type": place_type,
        "Latitude": lat,
        "Longitude": lon
    })

df = pd.DataFrame(places)
df.drop_duplicates(subset=["Name", "Latitude", "Longitude"], inplace=True)

print("Total Raw Records:", len(df))

# -----------------------------
# Reverse Geocoding
# -----------------------------
def get_location_name(lat, lon):
    try:
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            "lat": lat,
            "lon": lon,
            "format": "json"
        }
        headers = {"User-Agent": "bihar-gov-script"}

        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()

        address = data.get("address", {})
        return (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or address.get("district")
            or "N/A"
        )
    except:
        return "N/A"

print("Adding Location Names...")

locations = []
for index, row in df.iterrows():
    location = get_location_name(row["Latitude"], row["Longitude"])
    locations.append(location)
    time.sleep(1)

df["Location"] = locations

# -----------------------------
# Save to Excel
# -----------------------------
file_name = "bihar_all_government_expanded.xlsx"
df.to_excel(file_name, index=False)

print("\n✅ FINAL DATA SAVED:", file_name)
print("Total Final Records:", len(df))
print(df.head(20))