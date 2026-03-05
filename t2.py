import re
import time
from collections import Counter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googleapiclient.discovery import build

# =====================================
# CONFIGURATION
# =====================================
YOUTUBE_API_KEY = "AIzaSyDbbn1H1GcuMKXMhhRl-wnld7KOz_JLTl4"   # <-- Apna new key yaha daalein

# Multiple cities added here
cities = [
    "Bhita Bihar",
    "Bihta Bihar",
   
]

# =====================================
# KEYWORD GROUPS
# =====================================
PRICE_WORDS = ["price", "rate", "cost", "mahanga", "sasta"]
FRAUD_WORDS = ["fraud", "scam", "dhokha", "fake", "dispute"]
REGISTRY_WORDS = ["registry", "registration", "paper", "document"]
DEVELOPMENT_WORDS = ["road", "highway", "school", "hospital", "metro", "development"]
DEMAND_WORDS = ["buy", "sale", "investment", "future", "growth"]

# =====================================
# TEXT CLEANING
# =====================================
def clean_text(text):
    text = re.sub(r'[^a-zA-Z\u0900-\u097F\s]', '', text)
    return text.lower()

# =====================================
# YOUTUBE SETUP
# =====================================
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
analyzer = SentimentIntensityAnalyzer()

# =====================================
# FETCH COMMENTS
# =====================================
def get_comments(query):
    comments = []

    try:
        search_response = youtube.search().list(
            q=query,
            part="id",
            maxResults=3,
            type="video"
        ).execute()
    except:
        return comments

    for item in search_response.get("items", []):
        video_id = item["id"]["videoId"]

        try:
            comment_response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=50,
                textFormat="plainText"
            ).execute()

            for c in comment_response.get("items", []):
                text = c["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                comments.append(text)

        except:
            continue

    return comments

# =====================================
# INTERPRETATION ENGINE
# =====================================
def dynamic_explanation(city, keyword_counter, positive_pct, negative_pct):

    print("\n" + "="*90)
    print(f"Detailed Sentiment Interpretation for {city}\n")

    price_mentions = sum(keyword_counter[w] for w in PRICE_WORDS)
    growth_mentions = sum(keyword_counter[w] for w in DEMAND_WORDS)
    dev_mentions = sum(keyword_counter[w] for w in DEVELOPMENT_WORDS)
    registry_mentions = sum(keyword_counter[w] for w in REGISTRY_WORDS)
    fraud_mentions = sum(keyword_counter[w] for w in FRAUD_WORDS)

    if price_mentions > 0:
        print("Positive Outlook on Land Value")
        print(f"{price_mentions} comments discussed pricing or affordability.\n")
        print("Buyers are assessing whether current rates are reasonable")
        print("and if appreciation potential exists.\n")

    if growth_mentions > 0:
        print("2️⃣ Growth Expectation")
        print(f"{growth_mentions} comments referenced investment or growth.\n")
        print("Indicates long-term strategic positioning.\n")

    if dev_mentions > 0:
        print("3️⃣ Future Development Belief")
        print(f"{dev_mentions} comments mentioned infrastructure or development.\n")
        print("Urban expansion expectations influencing demand.\n")

    if registry_mentions > 0:
        print("4️⃣ Active Buying Intent")
        print(f"{registry_mentions} comments discussed registry or paperwork.\n")
        print("Shows serious purchase consideration.\n")

    if fraud_mentions > 0:
        print("⚠ Fraud / Risk Concern")
        print(f"{fraud_mentions} comments mentioned fraud or disputes.\n")
        print("Indicates verification behavior before investment.\n")

    print("Overall Interpretation:\n")

    if positive_pct > 60 and fraud_mentions == 0:
        print("Market appears confidence-driven and opportunity-focused.\n")
    elif fraud_mentions > 0 and negative_pct > 30:
        print("Market shows cautious optimism with visible risk awareness.\n")
    else:
        print("Market sentiment is mixed with both opportunity and caution.\n")

# =====================================
# MAIN LOOP (MULTI-CITY)
# =====================================
for city in cities:

    print("\n" + "#"*100)
    print(f"Analyzing: {city}")
    print("#"*100 + "\n")

    search_query = f"{city} land plot review"
    comments = get_comments(search_query)

    if not comments:
        print("No comments found.\n")
        continue

    pos = neg = neu = 0
    keyword_counter = Counter()

    print("🗣 COMMENTS:\n")

    for c in comments:
        print("•", c)
        cleaned = clean_text(c)
        score = analyzer.polarity_scores(cleaned)["compound"]

        if score >= 0.05:
            pos += 1
        elif score <= -0.05:
            neg += 1
        else:
            neu += 1

        for word in PRICE_WORDS + FRAUD_WORDS + REGISTRY_WORDS + DEVELOPMENT_WORDS + DEMAND_WORDS:
            if word in cleaned:
                keyword_counter[word] += 1

    total = len(comments)
    positive_pct = (pos / total) * 100
    negative_pct = (neg / total) * 100
    neutral_pct = (neu / total) * 100

    print("\n📊 SENTIMENT SUMMARY")
    print(f"Total Comments: {total}")
    print(f"Positive: {round(positive_pct,2)}%")
    print(f"Negative: {round(negative_pct,2)}%")
    print(f"Neutral : {round(neutral_pct,2)}%")

    dynamic_explanation(city, keyword_counter, positive_pct, negative_pct)

    time.sleep(1)

print("\n✅ ALL CITY ANALYSIS COMPLETE")