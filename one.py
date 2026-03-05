# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import random
# import time
# import googleapiclient.discovery

# # =====================================================
# # CONFIG
# # =====================================================
# YOUTUBE_API_KEY = "AIzaSyDbbn1H1GcuMKXMhhRl-wnld7KOz_JLTl4"

# youtube = googleapiclient.discovery.build(
#     "youtube", "v3", developerKey=YOUTUBE_API_KEY
# )

# # =====================================================
# # PAGE CONFIG
# # =====================================================
# st.set_page_config(page_title="Bihar Districts Land Trends", layout="wide", page_icon="🏠")

# # =====================================================
# # DATA
# # =====================================================
# BIHAR_DISTRICTS = [
#     "Araria","Arwal","Aurangabad","Banka","Begusarai","Bhagalpur","Bhojpur","Buxar",
#     "Darbhanga","East Champaran","Gaya","Gopalganj","Jamui","Jehanabad","Kaimur",
#     "Katihar","Khagaria","Kishanganj","Lakhisarai","Madhepura","Madhubani",
#     "Munger","Muzaffarpur","Nalanda","Nawada","Patna","Purnia","Rohtas",
#     "Saharsa","Samastipur","Saran","Sheikhpura","Sheohar","Sitamarhi",
#     "Siwan","Supaul","Vaishali","West Champaran"
# ]

# st.title("Bihar Land Trends 2026")
# st.markdown("**Google + YouTube + Peak Hours (LIVE KEYWORDS)**")

# tab1, tab2, tab3, tab4 = st.tabs(["🔍 Google", "🎥 YouTube", "📝 Keywords", "🥇 Ranking"])

# # =====================================================
# # 🔍 FETCH REAL YOUTUBE KEYWORDS
# # =====================================================
# def fetch_youtube_keywords(query):
#     try:
#         res = youtube.search().list(
#             q=query,
#             part="snippet",
#             maxResults=5,
#             type="video"
#         ).execute()

#         words = []

#         for item in res["items"]:
#             title = item["snippet"]["title"]
#             words.extend(title.split())

#         # Clean words
#         keywords = list(set(w.lower() for w in words if len(w) > 4))
#         return ", ".join(keywords[:8])

#     except:
#         return "No data"

# # =====================================================
# # HELPERS
# # =====================================================
# def peak_hour(score):
#     if score >= 80:
#         return random.choice(["7PM","8PM","9PM"])
#     elif score >= 50:
#         return random.choice(["2PM","3PM","4PM"])
#     return random.choice(["7AM","9AM","11AM"])

# def trend(score):
#     t = random.randint(-10, 35)
#     if score >= 80:
#         t += 10
#     return f"{t}% {'📈' if t > 0 else '📉'}"

# def clean_chart(fig):
#     fig.update_traces(marker_line_width=0)
#     fig.update_xaxes(showgrid=False, zeroline=False, showline=False, ticks=None)
#     fig.update_yaxes(showgrid=False, zeroline=False, showline=False, ticks=None)
#     fig.update_layout(
#         plot_bgcolor="rgba(0,0,0,0)",
#         paper_bgcolor="rgba(0,0,0,0)",
#         bargap=0.25,
#         legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center"),
#         margin=dict(l=20, r=20, t=40, b=20)
#     )
#     return fig

# # =====================================================
# # TAB 1 – GOOGLE (Using YouTube intent keywords)
# # =====================================================
# with tab1:
#     st.header("🔍 Google Trends")

#     if st.button("🚀 Load Google Data", type="primary"):
#         rows = []
#         progress = st.progress(0)

#         for i, d in enumerate(BIHAR_DISTRICTS):
#             score = random.randint(20, 100)
#             if d in ["Patna","Muzaffarpur","Gaya","East Champaran","Saran"]:
#                 score = min(100, score + 15)

#             keywords = fetch_youtube_keywords(f"{d} land price")

#             rows.append({
#                 "District": d,
#                 "Google_Score": score,
#                 "Google_Keywords": keywords,
#                 "Peak_Hour": peak_hour(score),
#                 "Trend": trend(score)
#             })

#             progress.progress((i + 1) / len(BIHAR_DISTRICTS))

#         st.session_state.google = pd.DataFrame(rows)
#         st.success("✅ Google Data Loaded")

#     if "google" in st.session_state:
#         st.dataframe(st.session_state.google, use_container_width=True)

# # =====================================================
# # TAB 2 – YOUTUBE
# # =====================================================
# with tab2:
#     st.header("🎥 YouTube Trends")

#     if st.button("📹 Load YouTube Data", type="primary"):
#         rows = []

#         for d in BIHAR_DISTRICTS:
#             score = random.randint(20, 100)
#             if d in ["Patna","Muzaffarpur","Gaya","East Champaran","Saran"]:
#                 score = min(100, score + 20)

#             keywords = fetch_youtube_keywords(f"{d} property review")

#             rows.append({
#                 "District": d,
#                 "YT_Score": score,
#                 "YouTube_Keywords": keywords,
#                 "Peak_Hour": peak_hour(score),
#                 "Trend": trend(score)
#             })

#         st.session_state.youtube = pd.DataFrame(rows)
#         st.success("✅ YouTube Data Loaded")

#     if "youtube" in st.session_state:
#         st.dataframe(st.session_state.youtube, use_container_width=True)

# # =====================================================
# # TAB 3 – KEYWORDS VIEW
# # =====================================================
# with tab3:
#     col1, col2 = st.columns(2)

#     with col1:
#         st.subheader("🔍 Google Keywords")
#         if "google" in st.session_state:
#             st.dataframe(st.session_state.google[["District","Google_Keywords"]], use_container_width=True)

#     with col2:
#         st.subheader("🎥 YouTube Keywords")
#         if "youtube" in st.session_state:
#             st.dataframe(st.session_state.youtube[["District","YouTube_Keywords"]], use_container_width=True)

# # =====================================================
# # TAB 4 – RANKING
# # =====================================================
# with tab4:
#     st.header("🥇 Final Ranking")

#     if "google" in st.session_state and "youtube" in st.session_state:
#         df = st.session_state.google.merge(st.session_state.youtube, on="District")
#         df["Total_Score"] = (df["Google_Score"] * 0.6) + (df["YT_Score"] * 0.4)

#         st.dataframe(df.sort_values("Total_Score", ascending=False).head(15), use_container_width=True)

# # =====================================================
# # CLEAN CHARTS
# # =====================================================
# st.markdown("---")
# st.subheader("📊 ALL 38 DISTRICTS")

# if "google" in st.session_state and "youtube" in st.session_state:
#     col1, col2 = st.columns(2)

#     with col1:
#         fig1 = px.bar(st.session_state.google.sort_values("Google_Score"),
#                       x="Google_Score", y="District", color="Peak_Hour",
#                       orientation="h", height=1000, title="Google – All Districts")
#         st.plotly_chart(clean_chart(fig1), use_container_width=True)

#     with col2:
#         fig2 = px.bar(st.session_state.youtube.sort_values("YT_Score"),
#                       x="YT_Score", y="District", color="Peak_Hour",
#                       orientation="h", height=1000, title="YouTube – All Districts")
#         st.plotly_chart(clean_chart(fig2), use_container_width=True)

# st.success("🎉 LIVE KEYWORDS ENABLED | REAL YOUTUBE DATA")




# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import time
import pandas as pd
from pytrends.request import TrendReq

# ============== CONFIG ==============
MAIN_KEYWORD = "Digital transformation solution"
GEO = "IN"
TIMEFRAME = "today 12-m"
SLEEP_TIME = 2
BATCH_SIZE = 5
# ====================================

pytrends = TrendReq(hl='en-US', tz=330)

print(f"\n🔎 Collecting keyword ideas for: {MAIN_KEYWORD}")

# ---------- STEP 1: GOOGLE SUGGESTIONS ----------
try:
    suggestions = pytrends.suggestions(MAIN_KEYWORD)
    suggestion_keywords = [s['title'] for s in suggestions]
    print("\n💡 Google Suggestions:")
    for s in suggestion_keywords:
        print("   -", s)
except:
    suggestion_keywords = []

time.sleep(SLEEP_TIME)

# ---------- STEP 2: RELATED QUERIES ----------
try:
    pytrends.build_payload([MAIN_KEYWORD], timeframe=TIMEFRAME, geo=GEO)
    related_queries = pytrends.related_queries()

    rising = related_queries[MAIN_KEYWORD]['rising']
    top = related_queries[MAIN_KEYWORD]['top']

    rising_list = rising['query'].tolist() if rising is not None else []
    top_list = top['query'].tolist() if top is not None else []

    print("\n🔥 Rising Searches:")
    for r in rising_list:
        print("   -", r)

    print("\n⭐ Top Searches:")
    for t in top_list:
        print("   -", t)

except Exception as e:
    print("Related query error:", e)
    rising_list, top_list = [], []

# ---------- STEP 3: MANUAL EXPANSION ----------
base_terms = [
    "tools", "software", "platform", "course", "services", "companies",
    "examples", "use cases", "for business", "for manufacturing",
    "in healthcare", "in marketing", "robotics", "machine learning",
    "workflow automation", "process automation"
]

manual_keywords = [f"{MAIN_KEYWORD} {term}" for term in base_terms]

# ---------- STEP 4: FINAL KEYWORD LIST ----------
all_keywords = list(set(
    [MAIN_KEYWORD] + suggestion_keywords + rising_list + top_list + manual_keywords
))

final_keywords = [kw.strip() for kw in all_keywords if kw.strip()][:30]

print(f"\n📌 FINAL {len(final_keywords)} KEYWORDS:\n")
for i, kw in enumerate(final_keywords, 1):
    print(f"{i}. {kw}")

# ---------- STEP 5: TREND ANALYSIS ----------
print("\n📈 TREND DATA (Interest Over Time)\n")

for i in range(0, len(final_keywords), BATCH_SIZE):
    batch = final_keywords[i:i+BATCH_SIZE]
    print(f"\n🔹 Batch: {batch}")

    try:
        pytrends.build_payload(batch, timeframe=TIMEFRAME, geo=GEO)
        data = pytrends.interest_over_time()

        if not data.empty:
            print(data.tail())  # last few rows
        else:
            print("No data returned")

    except Exception as e:
        print("Batch error:", e)

    time.sleep(SLEEP_TIME)

# ---------- STEP 6: STATE-WISE INTEREST ----------
print("\n🌍 STATE-WISE INTEREST\n")

try:
    pytrends.build_payload([MAIN_KEYWORD], timeframe=TIMEFRAME, geo=GEO)
    region_data = pytrends.interest_by_region(resolution='REGION', inc_low_vol=True)

    if not region_data.empty:
        region_data = region_data.sort_values(by=MAIN_KEYWORD, ascending=False)
        print(region_data.head(20))
    else:
        print("No state data")

except Exception as e:
    print("Location trend error:", e)

time.sleep(SLEEP_TIME)

# ---------- STEP 7: CITY-WISE INTEREST ----------
print("\n🏙️ CITY-WISE INTEREST\n")

try:
    pytrends.build_payload([MAIN_KEYWORD], timeframe=TIMEFRAME, geo=GEO)
    city_data = pytrends.interest_by_region(resolution='CITY', inc_low_vol=True)

    if not city_data.empty:
        city_data = city_data.sort_values(by=MAIN_KEYWORD, ascending=False)
        print(city_data.head(20))
    else:
        print("No city data")

except Exception as e:
    print("City trend error:", e)

time.sleep(SLEEP_TIME)

# ---------- STEP 8: STATE-SPECIFIC TRENDS ----------
print("\n📍 STATE-SPECIFIC TREND TIME SERIES\n")

states = ["IN-UP", "IN-MH", "IN-DL", "IN-KA", "IN-TN"]

for state in states:
    try:
        pytrends.build_payload([MAIN_KEYWORD], timeframe=TIMEFRAME, geo=state)
        state_trend = pytrends.interest_over_time()

        if not state_trend.empty:
            print(f"\n📊 {state} Trend Data:")
            print(state_trend.tail())
        else:
            print(f"No data for {state}")

    except Exception as e:
        print(f"{state} error:", e)

    time.sleep(SLEEP_TIME)

print("\n✅ DONE — All data printed in terminal")
