# import time
# import pandas as pd
# from pytrends.request import TrendReq

# # ================= CONFIG =================
# KEYWORD = "Digital Transformation."
# COUNTRY = "IN"
# TIMEFRAME = "today 12-m"
# SLEEP = 2
# HOT_THRESHOLD = 70
# GROWING_THRESHOLD = 40
# # ==========================================

# pytrends = TrendReq(hl='en-US', tz=330)

# print(f"\n🔎 Analyzing Market Demand for: {KEYWORD}\n")

# # ---------- FUNCTION: CLASSIFY MARKET ----------
# def classify_market(score):
#     if score >= HOT_THRESHOLD:
#         return "🔥 Hot Market"
#     elif score >= GROWING_THRESHOLD:
#         return "🌱 Growing Market"
#     else:
#         return "❄️ Low Market"

# # ---------- STEP 1: STATE LEVEL ANALYSIS ----------
# print("🌍 Fetching State-wise Demand...\n")

# pytrends.build_payload([KEYWORD], timeframe=TIMEFRAME, geo=COUNTRY)
# time.sleep(SLEEP)

# states_df = pytrends.interest_by_region(resolution='REGION', inc_low_vol=True)

# if states_df.empty:
#     print("No state data found")
# else:
#     states_df = states_df.sort_values(by=KEYWORD, ascending=False).reset_index()
#     states_df["Market Type"] = states_df[KEYWORD].apply(classify_market)

#     print("🏆 TOP BUSINESS STATES:\n")
#     print(states_df.head(10).to_string(index=False))

#     states_df.to_csv("business_opportunity_states.csv", index=False)

# # ---------- STEP 2: CITY LEVEL ANALYSIS ----------
# print("\n🏙️ Fetching City-wise Demand...\n")

# pytrends.build_payload([KEYWORD], timeframe=TIMEFRAME, geo=COUNTRY)
# time.sleep(SLEEP)

# cities_df = pytrends.interest_by_region(resolution='CITY', inc_low_vol=True)

# if cities_df.empty:
#     print("No city data found")
# else:
#     cities_df = cities_df.sort_values(by=KEYWORD, ascending=False).reset_index()
#     cities_df["Market Type"] = cities_df[KEYWORD].apply(classify_market)

#     print("🏆 TOP BUSINESS CITIES:\n")
#     print(cities_df.head(15).to_string(index=False))

#     cities_df.to_csv("business_opportunity_cities.csv", index=False)

# # ---------- STEP 3: BEST TARGET LOCATIONS ----------
# print("\n🚀 BEST LOCATIONS TO TARGET FOR SALES & ADS:\n")

# top_states = states_df[states_df["Market Type"] == "🔥 Hot Market"].head(5)
# top_cities = cities_df[cities_df["Market Type"] == "🔥 Hot Market"].head(5)

# if not top_states.empty:
#     print("🔥 Hot States:")
#     print(top_states[["geoName", KEYWORD]].to_string(index=False))

# if not top_cities.empty:
#     print("\n🔥 Hot Cities:")
#     print(top_cities[["geoName", KEYWORD]].to_string(index=False))

# print("\n✅ Analysis Complete! Files saved for marketing & sales planning.")




import time
import pandas as pd
from pytrends.request import TrendReq

# ==== INPUT (User prompt) ====
search_input = input("Enter search phrase (e.g., 'Show me companies in Bangalore searching for Digital Transformation'): ")

# Extract keyword and target city
# Simple parsing (improve later if needed)
parts = search_input.split(" in ")
if len(parts) > 1:
    raw_keyword = parts[0].replace("Show me companies", "").strip()
    target_city = parts[1].split(" searching")[0].strip()
else:
    raw_keyword = search_input
    target_city = ""

keyword = raw_keyword if raw_keyword else search_input

print(f"\n🔎 Search: '{keyword}' for city: '{target_city}'\n")

pytrends = TrendReq(hl='en-US', tz=330)

# Helper to classify
def classify_score(val):
    if val > 70: return "🔥 High Interest"
    if val > 40: return "🌱 Medium Interest"
    return "❄️ Low Interest"

# ---------- CITY LEVEL TREND ----------
print("🗺️ City Level Interest (All Cities):")

try:
    pytrends.build_payload([keyword], timeframe='today 12-m', geo='IN')
    city_data = pytrends.interest_by_region(resolution='CITY', inc_low_vol=True)

    if city_data.empty:
        print("No city data found for this keyword.")
    else:
        # Sort and annotate
        city_data = city_data.sort_values(by=keyword, ascending=False)
        city_data["Interest Category"] = city_data[keyword].apply(classify_score)

        # Print top 15 cities
        print(city_data.head(15).to_string())

        # If target city exists, print that too
        if target_city.title() in city_data.index:
            print(f"\n📍 Interest in {target_city.title()}:")
            row = city_data.loc[target_city.title()]
            print(f"{target_city.title()}: {row[keyword]} → {row['Interest Category']}")
        else:
            print(f"\n⚠️ No direct city match for: {target_city}")

except Exception as e:
    print("City interest error:", e)

time.sleep(2)

# ---------- STATE LEVEL TREND ----------
print("\n🌍 State Level Interest (All States):")

try:
    pytrends.build_payload([keyword], timeframe='today 12-m', geo='IN')
    state_data = pytrends.interest_by_region(resolution='REGION', inc_low_vol=True)

    if state_data.empty:
        print("No state data found.")
    else:
        state_data = state_data.sort_values(by=keyword, ascending=False)
        state_data["Interest Category"] = state_data[keyword].apply(classify_score)
        print(state_data.head(10).to_string())

except Exception as e:
    print("State interest error:", e)

print("\n✅ Done — Search interest printed.")
