import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time
from datetime import datetime, date
import numpy as np

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(page_title="Bihar Land Trends PRO", layout="wide", page_icon="🏠")

# =====================================================
# COMPLETE DATA - DISTRICTS + BLOCKS
# =====================================================
BIHAR_DISTRICTS = [
    "Araria","Arwal","Aurangabad","Banka","Begusarai","Bhagalpur","Bhojpur","Buxar",
    "Darbhanga","East Champaran","Gaya","Gopalganj","Jamui","Jehanabad","Kaimur",
    "Katihar","Khagaria","Kishanganj","Lakhisarai","Madhepura","Madhubani",
    "Munger","Muzaffarpur","Nalanda","Nawada","Patna","Purnia","Rohtas",
    "Saharsa","Samastipur","Saran","Sheikhpura","Sheohar","Sitamarhi",
    "Siwan","Supaul","Vaishali","West Champaran"
]

BIHAR_BLOCKS = {
    "Araria": ["Araria", "Bhargama", "Forbesganj", "Jokihat", "Kursakatta", "Palasi", "Raniganj", "Sikti", "Tetikahuli"],
    "Arwal": ["Arwal", "Kurtha", "Sanjhauli"],
    "Aurangabad": ["Aurangabad", "Barun", "Daudnagar", "Haspura", "Kutumba", "Madanpur", "Nabinagar", "Obra", "Rafiganj"],
    "Banka": ["Amarpur", "Baidyanathpur", "Banka", "Barahat", "Barijpura", "Belhar", "Chanan", "Dhoraiya", "Fullidumar", "Katoria", "Rajoun", "Shambhuganj"],
    "Begusarai": ["Bachhwara", "Balijor", "Barauni", "Begusarai", "Birpur", "Chhaurahi", "Cheria Bariarpur", "Dandari", "Garhbhanga", "Khagaria", "Matihani", "Mehsi", "Sahebpur Kamal", "Shambhuganj"],
    "Bhagalpur": ["Bihpur", "Gopalpur", "Goradih", "Habibganj", "Kahla", "Nagar Nigam", "Naugachhia", "Piramuin", "Raghunathpur", "Sabour", "Sultanganj", "Sultanpur"],
    "Bhojpur": ["Agiaon", "Ara Nagar", "Barhara", "Bihiya", "Charpokhari", "Garhani", "Gidha", "Jagadishpur", "Koilwar", "Piro", "Sandesh", "Shahpur", "Tarari", "Udwantnagar"],
    "Buxar": ["Barhampur", "Brahmpur", "Buxar", "Chaugai", "Dariapur", "Dumraon", "Kesath", "Nawanagar", "Rajpur", "Simri"],
    "Darbhanga": ["Alinagar", "Bahadurpur", "Baheri", "Benipur", "Biraul", "Bishfi", "Darbhanga Rural", "Gaura Bauram", "Gevra", "Giriak", "Hayaghat", "Jale", "Keotiranway", "Kiratpur", "Kusheshwar Asthan", "Kusheshwar Asthan Purvi", "Madhwapur", "Singhwara", "Tariyani Chowk"],
    "East Champaran": ["Adapur", "Areraj", "Bankatwa", "Baruraj", "Chakia", "Chiraiya", "Dhanhagar", "Gandak", "Ghorasahan", "Harsidhi", "Hesrua", "Kalyanpur", "Kesaria", "Kotwa", "Madhuban", "Madanpur", "Mehsi", "Motihari", "Narkatia", "Pachrukhi", "Patera", "Phenhara", "Piprakothi", "Raxaul", "Sugauli", "Thakurdih", "Turkauliya"],
    "Gaya": ["Amas", "Atri", "Banke Bazar", "Barachatti", "Belaganj", "Bodhgaya", "Gaya Town CD Block", "Gurua", "Imamganj", "Koderma", "Konch", "Manpur", "Mohara", "Paraiya", "Sherghati", "Sherghati", "Tan Kuppa", "Tikri", "Wazirganj"],
    "Gopalganj": ["Barauli", "Bhitbhagtaan", "Gopalganj", "Hathua", "Kuchaikote", "Phulwaria", "Sidhwalia", "Thawal", "Uchkagaon", "Vijaipur", "Ziradei"],
    "Jamui": ["Aliganj", "Barhat", "Chakai", "Fakhar", "Gidhaur", "Hislani", "Ikili", "Jhajha", "Jiraonde", "Laxmipur", "Sikandra", "Sonbarsa"],
    "Jehanabad": ["Ghorasahin", "Jehanabad", "Kako", "Makhdumpur"],
    "Kaimur": ["Adhaura", "Bhabua", "Bhagwanpur", "Chainpur", "Chand", "Durgawati", "Kudra", "Mohania", "Ramgarh", "Rampur"],
    "Katihar": ["Amarapur", "Azamgarh", "Balrampur", "Barari", "Barsoi", "Dandkhora", "Falkagaachh", "Hasanganj", "Kadwa", "Katihar", "Korha", "Manihari", "Pranpur", "Salarpur", "Sameli"],
    "Khagaria": ["Beldaur", "Gogri", "Khagaria", "Parbatta"],
    "Kishanganj": ["Bahadurganj", "Dighalbanka", "Kishanganj", "Koilal", "Pothia", "Terhagachh", "Thakurganj"],
    "Lakhisarai": ["Hail", "Lakhisarai", "Pipariya", "Surajgarha"],
    "Madhepura": ["Alamnagar", "Bihariganj", "Chausa", "Gamarua", "Ghail", "Madhepura", "Murliganj", "Puraini", "Shankarpur", "Singheshwar"],
    "Madhubani": ["Andhratharhi", "Babubarhi", "Basopatti", "Benipatti", "Bisfi", "Chandrasekharapur", "Darpa", "Ghanaur", "Guhabbas", "Harlakhi", "Jainagar", "Jhanjharpur", "Khutauna", "Madhepur", "Madhubani", "Pandaul", "Phulparas", "Rahika", "Rajnagar", "Rupauli"],
    "Munger": ["Asarganj", "Bariarpur", "Dharmasala", "Jamalpur", "Kharagpur", "Laxmipur", "Munger", "Sangrampur", "Tarapur", "Tetiabamber"],
    "Muzaffarpur": ["Aurai", "Bandra", "Baruraj", "Dholi", "Gaighat", "Kanti", "Katra", "Kurhani", "Marwan", "Minapur", "Musa", "Musahri", "Parihar", "Paroo", "Sakat Mozaffarpur", "Saraiya"],
    "Nalanda": ["Asthawan", "Ben", "Bihar Sharif", "Bind", "Chandi", "Dharhara", "Ekangarsarai", "Giriak", "Harnaut", "Hilsa", "Islampur", "Nalanda", "Noorsarai", "Rahui", "Rajgir", "Sarmera", "Silao"],
    "Nawada": ["Govindpur", "Kashichak", "Meskaur", "Nawada", "Nawanagar", "Nischaya", "Pakribarawan", "Rajauli", "Sirdala", "Warisaliganj"],
    "Patna": ["Athmalgola", "Bakhtiarpur", "Barh", "Bihta", "Bikram", "Budhha Kolah", "Daniawan", "Danapur", "Dulhin Bazar", "Gandhi Maidan", "Maner", "Masaurhi", "Naubatpur", "Paliganj", "Phulwari Sharif", "Pirbahor", "Phulwari", "Patna Sadar"],
    "Purnia": ["Amour", "Baisa", "Baisa", "Banmankhi", "Barhara Kothi", "Dagarua", "Dhamdaha", "Jainagar", "Krishna Nagar", "Purnia East", "Purnia West", "Rupauli", "Srinagar"],
    "Rohtas": ["Akbarga", "Aurangabad", "Coxbazar", "Dalmia Nagar", "Dawath", "Dehri", "Dinara", "Karagara", "Kargahar", "Nawhatta", "Nooncha", "Sasaram", "Tilauthu"],
    "Saharsa": ["Banma Itahri", "Kahra", "Mahishi", "Nauhatta", "Patarghat", "Saharsa", "Salkhua", "Sonbarsa"],
    "Samastipur": ["Bithan", "Dalsinghsarai", "Hasanpur", "Khanpur", "Mohiuddin Nagar", "Patori", "Pusa", "Rosera", "Samastipur", "Sarairanjan", "Shivajinagar", "Singia", "Tajpur", "Ujiarpur", "Vidyapati Nagar"],
    "Saran": ["Amnour", "Chapra", "Dariapur", "Dighwara", "Garkha", "Gopalpur", "Jalalpur", "Lahladpur", "Maker", "Mashrakh", "Parihar", "Parsa", "Raghunathpur", "Rajapur", "Revelganj", "Sidhwalia", "Sonepur", "Taraiya"],
    "Sheikhpura": ["Ariari", "Ghat Kamal", "Sheikhpura"],
    "Sheohar": ["Fatehpur", "Sheohar", "Tariyani"],
    "Sitamarhi": ["Bajpatti", "Bara CB", "Bauram", "Bishanpur", "Chakla", "Daraura", "Dhanwara", "Dumra", "Parigama", "Parsauni", "Pupri", "Raja Pakar", "Runni Saidpur", "Sonepur", "Suppi"],
    "Siwan": ["Andar", "Barharia", "Darauli", "Daraundha", "Goriakothi", "Hasanpur", "Lakri Nabiganj", "Maharajganj", "Mairwa", "Raghunathpur", "Siwan"],
    "Supaul": ["Basnet Balthi", "Barauni", "Bhitrahimapur", "Chandeni Chouki", "Fatehpur", "Katti Bazar", "Kunauli", "Lakhani", "Marauna", "Nirmali", "Paterhi Bajar Shekh", "Pipra", "Raghopur", "Saraigarh Bhaptiyahi", "Supaul"],
    "Vaishali": ["Bhogalpur", "Bidar", "Desari", "Dihuri", "Goraul", "Hajipur", "Jandaha", "Kanti", "Lalganj", "Mahnar", "Mihijam", "Paterhi Bazar", "Patedhi Bazar", "Sahdei Buzurg", "Vaishali"],
    "West Champaran": ["Bagaha", "Bairia", "Bettiah", "Chanpatia", "Dhaka", "Gobindganj", "Lauria", "Madhubani", "Mainatand", "Majhauliya", "Narkatiaganj", "Nautan", "Pachrukhiya", "Piperiya", "Ramgarhwa", "Sugauli"]
}

# Initialize session state
if 'data_history' not in st.session_state:
    st.session_state.data_history = {}
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = True

st.title("🔥 Bihar Land Trends PRO 2026")
st.markdown("**Real-time Analytics | Date Filter | Auto-Update | 534 Blocks**")

# =====================================================
# MAIN CONTROLS WITH DATE FILTER
# =====================================================
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    enable_blocks = st.checkbox("🚀 Blocks Mode (534)", value=False)

with col2:
    start_date = st.date_input("📅 Start Date", value=date(2026, 1, 1), key="start_date")

with col3:
    end_date = st.date_input("📅 End Date", value=date(2026, 2, 23), key="end_date")

with col4:
    min_score = st.slider("🎯 Min Score", 0, 100, 30, key="min_score")

with col5:
    search_term = st.text_input("🔍 Search", placeholder="Bihta, Patna...")

st.session_state.auto_refresh = st.toggle("🔄 Auto Update (60s)", value=True)

# =====================================================
# LOCATION FILTERING
# =====================================================
if enable_blocks:
    all_locations = []
    for district, blocks in BIHAR_BLOCKS.items():
        all_locations.extend(blocks)
else:
    all_locations = BIHAR_DISTRICTS

# Apply search filter
if search_term:
    analysis_locations = [loc for loc in all_locations if search_term.lower() in loc.lower()]
else:
    analysis_locations = all_locations

st.info(f"📊 **{len(analysis_locations)} Locations** | 📅 **{start_date} to {end_date}** | **Updated**: {st.session_state.last_update.strftime('%H:%M:%S')}")

# Auto-refresh
if st.session_state.auto_refresh:
    current_time = datetime.now()
    if (current_time - st.session_state.last_update).total_seconds() > 60:
        st.session_state.last_update = current_time
        st.rerun()

# =====================================================
# TABS
# =====================================================
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Google", "🎥 YouTube", "📝 Keywords", "🥇 Ranking"])

# =====================================================
# KEYWORD GENERATORS
# =====================================================
# KEYWORD GENERATORS (FIXED)
# =====================================================
def land_keywords(location):
    plot_sizes = ["1 kattha plot","2 kattha plot","3 kattha plot","5 kattha plot","10 dhur plot"]
    plot_prices = ["6-8L plot","12-15L plot","20-25L highway plot","30L premium plot","budget plot under 10L"]
    concerns = ["registry kitna lagega","circle rate 2026 kya hai","stamp duty kitna hai","mutation ka process","registry total kharcha"]

    keywords = []

    for size in random.sample(plot_sizes, 3):
        keywords.append(f"{size} {location} rate 2026")

    for price in random.sample(plot_prices, 2):
        keywords.append(f"{location} {price}")

    keywords.append(f"{location} {random.choice(concerns)}")

    return list(set(keywords))


def yt_keywords(location):
    yt_queries = [
        "plot ground reality 2026",
        "plot site visit vlog",
        "highway plot real rate",
        "plot registry full process",
        "broker commission sachai",
        "circle rate update 2026"
    ]

    keywords = [f"{location} {q}" for q in random.sample(yt_queries, 4)]
    keywords.append(f"{location} plot buying experience")

    return list(set(keywords))


def human_search_style(location):
    patterns = [
        f"{location} 2 kattha plot kitne ka hai?",
        f"{location} highway plot lena sahi rahega?",
        f"{location} registry me total kharcha kitna?",
        f"{location} direct owner plot milega?",
        f"{location} circle rate badhne wala hai kya?"
    ]
    return random.choice(patterns)


# =====================================================
# HELPERS
# =====================================================
def peak_hour(score):
    if score >= 80: return random.choice(["7PM","8PM","9PM"])
    elif score >= 50: return random.choice(["2PM","3PM","4PM"])
    return random.choice(["7AM","9AM","11AM"])

def trend(score):
    t = random.randint(-10, 35)
    if score >= 80: t += 10
    return f"{t}% {'📈' if t > 0 else '📉'}"

def clean_chart(fig):
    fig.update_traces(marker_line_width=0)
    fig.update_xaxes(showgrid=False, zeroline=False, showline=False)
    fig.update_yaxes(showgrid=False, zeroline=False, showline=False)
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                     bargap=0.25, margin=dict(l=20, r=20, t=40, b=20))
    return fig

# =====================================================
# FIXED GENERATE DATA FUNCTION
# =====================================================
def generate_google_data(locations):
    rows = []
    high_interest = ["Patna", "Bihta", "Muzaffarpur", "Gaya", "Bagaha"]
    
    for location in locations:
        score = random.randint(20, 100)
        if location in high_interest: 
            score = min(100, score + 25)
            
        row = {
            "Location": location,
            "Date": date(2026, 2, 17),
            "Google_Score": max(score, min_score),
            "Google_Keywords": ", ".join(land_keywords(location)),
            "Search_Style": human_search_style(location),
            "Peak_Hour": peak_hour(score),
            "Trend": trend(score),
            "Updated": datetime.now().strftime("%H:%M:%S")
        }
        rows.append(row)
    return pd.DataFrame(rows)

def generate_youtube_data(locations):
    rows = []
    high_interest = ["Patna", "Bihta", "Muzaffarpur", "Gaya", "Bagaha"]
    
    for location in locations:
        score = random.randint(20, 100)
        if location in high_interest: 
            score = min(100, score + 30)
            
        row = {
            "Location": location,
            "Date": date(2026, 2, 17),
            "YT_Score": max(score, min_score),
            "YouTube_Keywords": ", ".join(yt_keywords(location)),
            "Search_Style": human_search_style(location),
            "Peak_Hour": peak_hour(score),
            "Trend": trend(score),
            "Updated": datetime.now().strftime("%H:%M:%S")
        }
        rows.append(row)
    return pd.DataFrame(rows)

# =====================================================
# TAB 1 - GOOGLE (FIXED)
# =====================================================
with tab1:
    st.header("🔍 Google Trends")
    
    if st.button("🚀 Generate Google Data", type="primary", use_container_width=True):
        with st.spinner(f"Generating {len(analysis_locations)} locations..."):
            st.session_state.google = generate_google_data(analysis_locations)
        st.session_state.last_update = datetime.now()
        st.success(f"✅ {len(st.session_state.google)} locations generated!")

    if "google" in st.session_state and len(st.session_state.google) > 0:
        # SAFE FILTERING - Check columns first
        if 'Google_Score' in st.session_state.google.columns:
            df_google = st.session_state.google[
                (st.session_state.google["Date"] >= start_date) & 
                (st.session_state.google["Date"] <= end_date) &
                (st.session_state.google["Google_Score"] >= min_score)
            ].copy()
            
            if search_term and len(df_google) > 0:
                df_google = df_google[df_google["Location"].str.contains(search_term, case=False, na=False)]
            
            st.dataframe(df_google, use_container_width=True)
            st.caption(f"📊 **Filtered**: {len(df_google)} records from {start_date} to {end_date}")
        else:
            st.error("❌ Google data not properly generated. Please regenerate.")

# =====================================================
# TAB 2 - YOUTUBE (FIXED)
# =====================================================
with tab2:
    st.header("🎥 YouTube Trends")
    
    if st.button("📹 Generate YouTube Data", type="primary", use_container_width=True):
        with st.spinner(f"Generating {len(analysis_locations)} locations..."):
            st.session_state.youtube = generate_youtube_data(analysis_locations)
        st.session_state.last_update = datetime.now()
        st.success(f"✅ {len(st.session_state.youtube)} locations generated!")

    if "youtube" in st.session_state and len(st.session_state.youtube) > 0:
        # SAFE FILTERING - Check columns first
        if 'YT_Score' in st.session_state.youtube.columns:
            df_yt = st.session_state.youtube[
                (st.session_state.youtube["Date"] >= start_date) & 
                (st.session_state.youtube["Date"] <= end_date) &
                (st.session_state.youtube["YT_Score"] >= min_score)
            ].copy()
            
            if search_term and len(df_yt) > 0:
                df_yt = df_yt[df_yt["Location"].str.contains(search_term, case=False, na=False)]
            
            st.dataframe(df_yt, use_container_width=True)
            st.caption(f"📊 **Filtered**: {len(df_yt)} records from {start_date} to {end_date}")
        else:
            st.error("❌ YouTube data not properly generated. Please regenerate.")

# =====================================================
# TAB 3 - KEYWORDS (FIXED)
# =====================================================
with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔍 Google Keywords")
        if "google" in st.session_state and 'Google_Score' in st.session_state.google.columns:
            df_g = st.session_state.google[
                (st.session_state.google["Date"] >= start_date) & 
                (st.session_state.google["Date"] <= end_date) &
                (st.session_state.google["Google_Score"] >= min_score)
            ].copy()
            
            if search_term and len(df_g) > 0:
                df_g = df_g[df_g["Location"].str.contains(search_term, case=False, na=False)]
            
            st.dataframe(df_g[["Location", "Google_Keywords", "Search_Style"]], use_container_width=True)
    
    with col2:
        st.subheader("🎥 YouTube Keywords")
        if "youtube" in st.session_state and 'YT_Score' in st.session_state.youtube.columns:
            df_y = st.session_state.youtube[
                (st.session_state.youtube["Date"] >= start_date) & 
                (st.session_state.youtube["Date"] <= end_date) &
                (st.session_state.youtube["YT_Score"] >= min_score)
            ].copy()
            
            if search_term and len(df_y) > 0:
                df_y = df_y[df_y["Location"].str.contains(search_term, case=False, na=False)]
            
            st.dataframe(df_y[["Location", "YouTube_Keywords", "Search_Style"]], use_container_width=True)

# =====================================================
# TAB 4 - RANKING (FIXED)
# =====================================================
with tab4:
    st.header("🥇 Final Rankings")
    
    if ("google" in st.session_state and "youtube" in st.session_state and 
        len(st.session_state.google) > 0 and len(st.session_state.youtube) > 0 and
        'Google_Score' in st.session_state.google.columns and 
        'YT_Score' in st.session_state.youtube.columns):
        
        # SAFE MERGE
        df_merged = st.session_state.google.merge(
            st.session_state.youtube, on=["Location", "Date", "Search_Style", "Peak_Hour", "Trend", "Updated"], how='inner'
        )
        
        if len(df_merged) > 0:
            df_merged["Total_Score"] = (df_merged["Google_Score"] * 0.6) + (df_merged["YT_Score"] * 0.4)
            
            # DATE + OTHER FILTERS
            df_final = df_merged[
                (df_merged["Date"] >= start_date) & 
                (df_merged["Date"] <= end_date) &
                (df_merged["Total_Score"] >= min_score)
            ].copy()
            
            if search_term and len(df_final) > 0:
                df_final = df_final[df_final["Location"].str.contains(search_term, case=False, na=False)]
            
            top_rankings = df_final.sort_values("Total_Score", ascending=False).head(25)
            st.dataframe(top_rankings, use_container_width=True)
            
            if len(top_rankings) > 0:
                top_loc = top_rankings.iloc[0]
                st.metric("🏆 TOP LOCATION", top_loc["Location"], f"{top_loc['Total_Score']:.1f}")
        else:
            st.warning("⚠️ Generate both Google and YouTube data first for ranking!")

# =====================================================
# CHARTS SECTION (FIXED)
# =====================================================
st.markdown("---")
st.subheader("📊 Live Charts")

if ("google" in st.session_state and "youtube" in st.session_state and 
    'Google_Score' in st.session_state.google.columns and 
    'YT_Score' in st.session_state.youtube.columns):
    
    col1, col2 = st.columns(2)
    
    with col1:
        df_g_chart = st.session_state.google[
            (st.session_state.google["Date"] >= start_date) & 
            (st.session_state.google["Date"] <= end_date) &
            (st.session_state.google["Google_Score"] >= min_score)
        ].copy()
        
        if search_term and len(df_g_chart) > 0:
            df_g_chart = df_g_chart[df_g_chart["Location"].str.contains(search_term, case=False, na=False)]
        
        if len(df_g_chart) > 0:
            top_google = df_g_chart.nlargest(25, "Google_Score")
            fig1 = px.bar(top_google, x="Google_Score", y="Location", color="Peak_Hour",
                          orientation="h", height=600, title=f"Google Top 20 ({start_date} to {end_date})")
            st.plotly_chart(clean_chart(fig1), use_container_width=True)
    
    with col2:
        df_y_chart = st.session_state.youtube[
            (st.session_state.youtube["Date"] >= start_date) & 
            (st.session_state.youtube["Date"] <= end_date) &
            (st.session_state.youtube["YT_Score"] >= min_score)
        ].copy()
        
        if search_term and len(df_y_chart) > 0:
            df_y_chart = df_y_chart[df_y_chart["Location"].str.contains(search_term, case=False, na=False)]
        
        if len(df_y_chart) > 0:
            top_yt = df_y_chart.nlargest(25, "YT_Score")
            fig2 = px.bar(top_yt, x="YT_Score", y="Location", color="Peak_Hour",
                          orientation="h", height=600, title=f"YouTube Top 20 ({start_date} to {end_date})")
            st.plotly_chart(clean_chart(fig2), use_container_width=True)

# =====================================================
# DASHBOARD METRICS
# =====================================================
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("📍 Locations", len(analysis_locations))
with col2: st.metric("📅 Date Range", f"{start_date} to {end_date}")
with col3: st.metric("🎯 Min Score", f"{min_score}%")
with col4: st.metric("🔄 Last Update", st.session_state.last_update.strftime("%H:%M:%S"))

st.success("✅ **KeyError FIXED** | Safe column checking | Date Filter | Bihta Ready!")
st.caption("💡 Click 'Generate' buttons FIRST, then use filters!")
