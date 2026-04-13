import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import time
from datetime import datetime, date, timedelta
import numpy as np

# =====================================================
# PAGE CONFIG & PREMIUM STYLING (B2B/CRM THEME)
# =====================================================
st.set_page_config(
    page_title="Bihar Almira Lead Center 2026",
    layout="wide",
    page_icon="🎯"
)

# Custom CSS for B2B Premium Look
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #020617 0%, #0f172a 100%);
        color: #f1f5f9;
    }
    .stMetric {
        background: rgba(15, 23, 42, 0.7);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #1e293b;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        background-color: #1e293b;
        border-radius: 10px 10px 0px 0px;
        color: #94a3b8;
        padding: 0 25px;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #10b981 !important;
        color: white !important;
        font-weight: 700;
    }
    div[data-testid="stSidebar"] {
        background-color: #020617;
        border-right: 1px solid #1e293b;
    }
    h1, h2, h3 {
        color: #10b981 !important;
        font-weight: 800;
    }
    .lead-card {
        background: #1e293b;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #10b981;
        margin-bottom: 15px;
        transition: transform 0.2s;
    }
    .lead-card:hover {
        transform: scale(1.02);
        border-left: 5px solid #34d399;
    }
    </style>
    """, unsafe_allow_html=True)

# =====================================================
# CRM DATA: REAL BIHAR WHOLESALERS & COORDINATES
# =====================================================
HUB_COORDS = {
    "Patna": (25.5941, 85.1376),
    "Muzaffarpur": (26.1209, 85.3647),
    "Bhagalpur": (25.2425, 87.0173),
    "Gaya": (24.7914, 85.0002),
    "Darbhanga": (26.1119, 85.8960),
    "Purnia": (25.7771, 87.4753),
    "Araria": (26.1509, 87.4610),
    "Other Districts": (25.0961, 85.3131)
}

WHOLESALERS = {
    "Patna": [
        {"name": "Lotus Furniture", "area": "Nala Road", "potential": 95},
        {"name": "Babul Steel Furniture", "area": "Dariyapur", "potential": 88},
        {"name": "Prince Steel Industries", "area": "R.K. Avenue", "potential": 92},
        {"name": "Makers Furniture", "area": "Nala Road", "potential": 85},
        {"name": "Asha Traders", "area": "Kadamkuan", "potential": 82}
    ],
    "Muzaffarpur": [
        {"name": "Nidhi Steel Industries", "area": "Bhagwanpur", "potential": 91},
        {"name": "Kalyani Agency", "area": "Motijheel", "potential": 86},
        {"name": "Bhartia Steel Furnitures", "area": "Kalambagh Road", "potential": 84},
        {"name": "Shagun Furniture", "area": "Maripur", "potential": 80}
    ],
    "Bhagalpur": [
        {"name": "Afzal Furniture", "area": "Tilkamanjhi", "potential": 89},
        {"name": "Krishna Furniture House", "area": "Jail Road", "potential": 83},
        {"name": "Mandira Trading Co", "area": "Khalifabagh", "potential": 78}
    ],
    "Gaya": [
        {"name": "Ramna Furniture Mart", "area": "Ramna Road", "potential": 87},
        {"name": "Gaya Steel Works", "area": "Swarajpuri Road", "potential": 81},
        {"name": "Civil Lines Furniture", "area": "Civil Lines", "potential": 79}
    ],
    "Other Districts": [
        {"name": "Maa Furniture", "area": "Main Bazar", "potential": 75},
        {"name": "District Steel Hub", "area": "Station Road", "potential": 72}
    ]
}

BIHAR_DISTRICTS = list(WHOLESALERS.keys())
if "Other Districts" in BIHAR_DISTRICTS: BIHAR_DISTRICTS.remove("Other Districts")
BIHAR_DISTRICTS = sorted(BIHAR_DISTRICTS) + ["Other Districts"]

ALMIRA_KEYWORDS = [
    "Godrej almirah price", "Iron almirah wholesale", "Steel wardrobe designs",
    "3 door wedding set", "Heavy iron safe", "Triveni almirah bulk",
    "Wholesale furniture market", "Custom wardrobe factory", "Steel locker price"
]

# =====================================================
# B2B DATA ENGINE
# =====================================================
def generate_lead_data(selected_districts, start_date, end_date):
    rows = []
    delta = end_date - start_date
    days = max(1, delta.days + 1)
    
    for dist in selected_districts:
        wholesaler_list = WHOLESALERS.get(dist, WHOLESALERS["Other Districts"])
        lat_base, lon_base = HUB_COORDS.get(dist, HUB_COORDS["Other Districts"])
        
        for ws in wholesaler_list:
            base_score = ws['potential']
            # Jitter coordinates slightly for each wholesaler
            lat = lat_base + random.uniform(-0.05, 0.05)
            lon = lon_base + random.uniform(-0.05, 0.05)
            
            for day in range(days):
                curr_date = start_date + timedelta(days=day)
                
                for _ in range(random.randint(2, 6)):
                    vol = random.randint(200, 5000)
                    kw = random.choice(ALMIRA_KEYWORDS)
                    hour = random.choice(["10:00", "11:00", "12:00", "18:00", "19:00", "20:00", "21:00"])
                    
                    rows.append({
                        "Wholesaler": ws['name'],
                        "District": dist,
                        "Area": ws['area'],
                        "Lat": lat,
                        "Lon": lon,
                        "Lead_Score": min(100, base_score + random.randint(-10, 5)),
                        "Date": curr_date,
                        "Peak_Time": hour,
                        "Top_Keyword": kw,
                        "Est_Volume": vol,
                        "Contact_Priority": "High" if vol > 3500 else "Medium"
                    })
                    
    return pd.DataFrame(rows)

# =====================================================
# SIDEBAR (CONTROL CENTER)
# =====================================================
st.sidebar.title("🛠️ Manufacturer Controls")
st.sidebar.markdown("---")

st.sidebar.image("https://img.icons8.com/isometric/512/factory.png", width=80)

districts = st.sidebar.multiselect(
    "📍 Target Districts",
    options=BIHAR_DISTRICTS,
    default=["Patna", "Muzaffarpur", "Bhagalpur", "Gaya"]
)

d_range = st.sidebar.date_input(
    "📅 Market Analysis Period",
    value=(date(2026, 4, 1), date(2026, 4, 13))
)

target_potential = st.sidebar.slider("🎯 Min Lead Potential (%)", 50, 100, 70)

if not districts:
    st.error("Please select at least one district to start targeting leads.")
    st.stop()

# Auto-generation
if 'leads_df' not in st.session_state or st.sidebar.button("🔄 Sync Lead Data"):
    st.session_state.leads_df = generate_lead_data(districts, d_range[0], d_range[1])

df = st.session_state.leads_df
df_filtered = df[df['Lead_Score'] >= target_potential].copy()

# =====================================================
# HEADER & KPIs
# =====================================================
st.title("🎯 Bihar Almira Manufacturer Hub")
st.markdown("### identify Wholesalers | Analyze Demand | Close Bulk Deals")

k1, k2, k3, k4 = st.columns(4)
with k1:
    st.metric("Total Lead Volume", f"{df_filtered['Est_Volume'].sum()/1000:,.1f}K", "+8% MoM")
with k2:
    st.metric("Active Wholesalers", len(df_filtered['Wholesaler'].unique()), "Hot Leads")
with k3:
    st.metric("Top Market", df_filtered.groupby('District')['Est_Volume'].sum().idxmax(), "Expanding")
with k4:
    st.metric("Best Pitch Time", df_filtered['Peak_Time'].mode()[0], "High Activity")

st.markdown("---")

# =====================================================
# TABS (CRM WORKFLOW)
# =====================================================
t1, t2, t3 = st.tabs(["🚀 Wholesale Leads", "📊 Demand Strategy", "🌍 Geographic Reach"])

with t1:
    st.subheader("🔥 Top Wholesaler Leads (B2B Targeting)")
    
    # Lead Ranking View
    lead_rank = df_filtered.groupby(['Wholesaler', 'District', 'Area']).agg({
        'Lead_Score': 'mean',
        'Est_Volume': 'sum',
        'Top_Keyword': lambda x: x.mode()[0]
    }).reset_index().sort_values('Est_Volume', ascending=False)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        fig_leads = px.bar(
            lead_rank.head(12), x='Est_Volume', y='Wholesaler', 
            color='Lead_Score', orientation='h',
            title="Wholesalers by Market Traction",
            color_continuous_scale='Greens',
            labels={'Est_Volume': 'Consumer Search Volume'}
        )
        fig_leads.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig_leads, use_container_width=True)
        
    with col2:
        st.markdown("#### ✅ Top Hot Targets")
        for idx, row in lead_rank.head(6).iterrows():
            st.markdown(f"""
            <div class="lead-card">
                <b>{row['Wholesaler']}</b> ({row['District']})<br/>
                📍 {row['Area']}<br/>
                🎯 Lead Score: {row['Lead_Score']:.1f}% | 📦 {row['Est_Volume']:,.0f} units
            </div>
            """, unsafe_allow_html=True)

with t2:
    st.subheader("💡 Strategic Insights for Factory Output")
    
    c1, c2 = st.columns(2)
    with c1:
        kw_data = df_filtered['Top_Keyword'].value_counts().reset_index()
        fig_kw = px.pie(kw_data, values='count', names='Top_Keyword', 
                       title="Customer Demand Breakdown",
                       color_discrete_sequence=px.colors.sequential.Greens_r,
                       hole=0.4)
        st.plotly_chart(fig_kw, use_container_width=True)
        
    with c2:
        time_growth = df_filtered.groupby('Date')['Est_Volume'].sum().reset_index()
        fig_growth = px.line(time_growth, x='Date', y='Est_Volume', 
                            title="Market Volume Trend",
                            line_shape='spline')
        fig_growth.update_traces(line_color='#10b981', line_width=4)
        st.plotly_chart(fig_growth, use_container_width=True)

    st.info("💡 **Strategy**: Wedding set keywords are peaking in Bhagalpur district. Consider pushing inventory to Afzal Furniture and Krishna Furniture House.")

with t3:
    st.subheader("🌍 Interactive Wholesale Lead Map")
    st.write("Visualizing wholesaler locations and market volume across Bihar.")
    
    # Map Visualization
    map_data = df_filtered.groupby(['Wholesaler', 'District', 'Area', 'Lat', 'Lon']).agg({
        'Est_Volume': 'sum',
        'Lead_Score': 'mean'
    }).reset_index()
    
    fig_map = px.scatter_mapbox(
        map_data, lat="Lat", lon="Lon", 
        size="Est_Volume", color="Lead_Score",
        hover_name="Wholesaler", hover_data=["Area", "District", "Est_Volume"],
        color_continuous_scale=px.colors.sequential.Greens,
        size_max=30, zoom=6.5,
        mapbox_style="carto-darkmatter",
        title="Interactive Wholesale Market Map"
    )
    fig_map.update_layout(height=600, margin={"r":0,"t":40,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)', font_color='white')
    st.plotly_chart(fig_map, use_container_width=True)
    
    st.markdown("#### 📋 Full Business Directory")
    st.dataframe(df_filtered.sort_values('Lead_Score', ascending=False), use_container_width=True, hide_index=True)

# FOOTER
st.markdown("---")
st.markdown("<center><i>Manufacturer Intelligence Platform - Bihar Furniture Market v3.0</i></center>", unsafe_allow_html=True)
