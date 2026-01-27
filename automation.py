import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import folium
from streamlit_folium import folium_static


# Streamlit page config
st.set_page_config(
    page_title="🚀 ALL INDIA IT Automation Solution Search Analyzer 2026",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ALL INDIA KEY CITIES (Updated from research)
INDIA_LOCATIONS = [
    'Delhi', 'Mumbai', 'Bangalore', 'Pune', 'Chennai', 'Hyderabad', 
    'Noida', 'Gurgaon', 'Nashik', 'Lucknow', 'Ahmedabad', 'Kolkata',
    'Jaipur', 'Coimbatore', 'Indore', 'Vadodara', 'Nagpur', 'Surat',
    'Visakhapatnam', 'Thiruvananthapuram', 'Remote', 'Pan India'
]


# *** NEW: BUSINESS TYPE KEYWORDS + COMPANY MAPPING ***
BUSINESS_KEYWORDS = {
    'Manufacturing': ['manufacturing','factory','production','industrial','machinery','plant','automobile','textile','forging','casting','assembly line'],
    
    'Logistics & Supply Chain': ['logistics','supply chain','warehouse','transport','shipping','delivery','fleet','cold storage'],
    
    'Finance & Banking': ['bank','finance','insurance','fintech','loan','investment','nbfc','trading','stock market'],
    
    'Healthcare & Pharma': ['hospital','healthcare','pharma','medical','clinic','diagnostic','biotech','laboratory'],
    
    'Retail & E-commerce': ['retail','store','ecommerce','shopping','pos','marketplace','inventory','supermarket'],
    
    'IT Services & Software': ['software','development','consulting','automation','cloud','ai','ml','data','cybersecurity','saas'],
    
    'Real Estate & Construction': ['real estate','property','construction','builder','infrastructure','contractor','housing'],
    
    'Education & EdTech': ['school','college','university','edtech','learning','training','coaching','lms'],
    
    'Energy & Power': ['energy','power','solar','renewable','wind','electricity','grid','battery'],
    
    'Telecom': ['telecom','telecommunication','5g','broadband','fiber','network provider'],
    
    'Media & Entertainment': ['media','entertainment','broadcast','production house','streaming','film','music'],
    
    'Travel & Hospitality': ['travel','tourism','hotel','resort','hospitality','airlines','booking'],
    
    'Agriculture & AgriTech': ['agriculture','farming','agritech','dairy','poultry','food processing','cold chain'],
    
    'Government & Public Sector': ['government','municipal','smart city','public sector','defence','railway'],
    
    'Automobile & EV': ['automobile','automotive','ev','electric vehicle','auto parts','dealership'],
    
    'FMCG & Consumer Goods': ['fmcg','consumer goods','packaging','beverage','food brand','personal care'],
    
    'Textiles & Apparel': ['textile','garment','apparel','fashion','fabric','weaving','knitting'],
    
    'Mining & Metals': ['mining','metal','steel','iron','aluminium','foundry','smelting'],
    
    'Chemicals & Fertilizers': ['chemical','fertilizer','pesticide','paint','polymer','petrochemical'],
    
    'Security & Surveillance': ['security','surveillance','cctv','access control','biometric','fire safety']
}


# *** NEW: TOP COMPANIES FOR EACH BUSINESS TYPE ***
COMPANY_MAPPING = {
    'Manufacturing': ['Hero MotoCorp', 'Tata Motors', 'Mahindra', 'Larsen & Toubro'],
    
    'Logistics & Supply Chain': ['Blue Dart', 'Delhivery', 'DTDC', 'Ecom Express'],
    
    'Finance & Banking': ['HDFC Bank', 'ICICI Bank', 'SBI', 'Axis Bank', 'Kotak Mahindra Bank'],
    
    'Healthcare & Pharma': ['Apollo Hospitals', 'Fortis Healthcare', 'Max Healthcare', 'Sun Pharma', 'Cipla'],
    
    'Retail & E-commerce': ['Reliance Retail', 'Flipkart', 'Amazon India', 'BigBasket', 'DMart'],
    
    'IT Services & Software': ['TCS', 'Infosys', 'HCLTech', 'Wipro', 'Tech Mahindra', 'LTIMindtree'],
    
    'Real Estate & Construction': ['DLF', 'Godrej Properties', 'Lodha Group', 'Prestige Group'],
    
    'Education & EdTech': ['Byju’s', 'Unacademy', 'PhysicsWallah', 'Vedantu'],
    
    'Energy & Power': ['NTPC', 'Tata Power', 'Adani Green Energy', 'ReNew Power'],
    
    'Telecom': ['Jio', 'Airtel', 'Vodafone Idea', 'BSNL'],
    
    'Media & Entertainment': ['Zee Entertainment', 'Star India', 'Sony Pictures Networks India', 'Netflix India'],
    
    'Travel & Hospitality': ['MakeMyTrip', 'OYO', 'Taj Hotels', 'IndiGo'],
    
    'Agriculture & AgriTech': ['ITC Agri', 'Ninjacart', 'DeHaat', 'Udaan'],
    
    'Government & Public Sector': ['Indian Railways', 'BHEL', 'ONGC', 'HAL'],
    
    'Automobile & EV': ['Tata Motors EV', 'Mahindra Electric', 'Ather Energy', 'Ola Electric'],
    
    'FMCG & Consumer Goods': ['HUL', 'ITC', 'Nestle India', 'Dabur'],
    
    'Textiles & Apparel': ['Raymond', 'Arvind Ltd', 'Aditya Birla Fashion', 'Page Industries'],
    
    'Mining & Metals': ['Tata Steel', 'JSW Steel', 'SAIL', 'Vedanta'],
    
    'Chemicals & Fertilizers': ['UPL', 'Tata Chemicals', 'Coromandel International', 'Pidilite'],
    
    'Security & Surveillance': ['CP Plus', 'Hikvision India', 'Prama Hikvision', 'Godrej Security']
}



@st.cache_data(ttl=3600)
def create_session():
    session = requests.Session()
    retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[403, 429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def get_rotating_headers():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    ]
    return {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }


@st.cache_data(ttl=1800)
def analyze_location_mentions(url, keyword):
    """Count ALL INDIA location mentions for IT automation keywords"""
    session = create_session()
    headers = get_rotating_headers()
    session.headers.update(headers)
    
    location_counts = {city: 0 for city in INDIA_LOCATIONS}
    
    try:
        response = session.get(url, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text().lower()
        
        for city in INDIA_LOCATIONS:
            city_lower = city.lower()
            count = len(re.findall(r'\b' + re.escape(city_lower) + r'\b', text_content))
            location_counts[city] = count
        
        keyword_lower = keyword.lower()
        if keyword_lower in text_content:
            for city in location_counts:
                location_counts[city] += 2
        
    except:
        pass
    
    return pd.DataFrame(list(location_counts.items()), columns=['Location', 'Search_Mentions'])


@st.cache_data(ttl=1800)
def analyze_business_types(url, keyword):
    """Analyze which business types are searching for IT automation"""
    session = create_session()
    headers = get_rotating_headers()
    session.headers.update(headers)
    
    business_scores = {btype: 0 for btype in BUSINESS_KEYWORDS.keys()}
    text_content = ""
    
    try:
        response = session.get(url, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text().lower()
        
        for btype, keywords in BUSINESS_KEYWORDS.items():
            for keyword_item in keywords:
                count = len(re.findall(r'\b' + re.escape(keyword_item) + r'\b', text_content))
                business_scores[btype] += count
        
        keyword_lower = keyword.lower()
        if keyword_lower in text_content:
            for btype in business_scores:
                business_scores[btype] += 1
    
    except:
        pass
    
    return pd.DataFrame(list(business_scores.items()), columns=['Business_Type', 'Mentions']), text_content


# Custom CSS
st.markdown("""
<style>
    .main-header {font-size: 3.5rem; color: #1f77b4; text-align: center; margin-bottom: 2rem;}
    .metric-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                  padding: 1.5rem; border-radius: 15px; text-align: center; color: white;}
    .business-card {background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                   padding: 1.5rem; border-radius: 15px; text-align: center; color: white;}
    .it-services-card {background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%); 
                       padding: 2rem; border-radius: 20px; text-align: center; color: white; margin: 1rem 0;}
    .stPlotlyChart {border-radius: 10px;}
    .company-list {font-size: 0.9rem; line-height: 1.4;}
</style>
""", unsafe_allow_html=True)


st.markdown('<h1 class="main-header">🤖 ALL INDIA IT Automation Search Analyzer</h1>', unsafe_allow_html=True)

# *** DYNAMIC BUSINESS LINE WITH COMPANY NAMES ***
if 'analysis_bus' in st.session_state and not st.session_state.analysis_bus.empty:
    df_bus = st.session_state.analysis_bus.copy()
    active_businesses = df_bus[df_bus['Mentions'] > 0].nlargest(4, 'Mentions')
    
    if len(active_businesses) > 0:
        business_display = []
        for _, row in active_businesses.iterrows():
            btype = row['Business_Type']
            score = int(row['Mentions'])
            companies = COMPANY_MAPPING.get(btype, ['N/A'])[0:6]  # Top 2 companies
            company_str = " • ".join(companies)
            business_display.append(f"{btype}({score})")
        
        st.markdown(f"**Real-time analysis | {' • '.join(business_display)}** 🔥")
        
        # IT Services Special Highlight (34 mentions)
        it_services_row = df_bus[df_bus['Business_Type'] == 'IT Services']
        if not it_services_row.empty and it_services_row['Mentions'].iloc[0] == 34:
            st.markdown("""
            <div class="it-services-card">
                <h2>🎯 IT Services HOTSPOT</h2>
                <h3>34 Mentions | TCS • Infosys • HCL • Wipro</h3>
                <p class="company-list">Tech Mahindra भी active</p>
            </div>
            """, unsafe_allow_html=True)
        
        total = df_bus['Mentions'].sum()
        top_pct = f"{active_businesses['Mentions'].iloc[0]/total*100:.0f}%" if total > 0 else "0%"
        st.caption(f"*{active_businesses['Business_Type'].iloc[0]} leads with {top_pct} share | {len(active_businesses)} active sectors*")
else:
    st.markdown("**Real-time location + business analysis | Manufacturing • Logistics • Finance • Healthcare**")


# Sidebar - Enhanced Controls
st.sidebar.header("🔍 Search Settings")
keyword = st.sidebar.text_input("Keywords", value="IT automation solution").strip()
business_type = st.sidebar.selectbox("Business Type", 
                                   ["All", "Manufacturing", "Logistics", "Finance", "Healthcare", "Retail"])


max_sources = st.sidebar.slider("Sources to Scan", 8, 25, 15)
auto_refresh = st.sidebar.checkbox("🔄 Auto-refresh every 5 min")


# IT Automation focused sources
automation_sources = [
    'https://dir.indiamart.com/search.mp?ss=it+automation',
    'https://www.indiamart.com/search.mp?ss=automation+solution',
    'https://in.linkedin.com/jobs/it-automation-jobs',
    'https://www.naukri.com/it-automation-jobs',
    'https://www.indeed.co.in/IT-Automation-jobs',
    'https://builtin.com/articles/top-automation-companies-in-india',
    'https://www.aeologic.com/automation-solutions/',
    'https://scadea.com/top-10-hyperautomation-solution-providers-in-india/',
    'https://dir.indiamart.com/new-delhi/automation-solutions.html',
    'https://www.justdial.com/search?what=IT+Automation&country=India',
    'https://www.sulekha.com/it-automation-services/',
    'https://www.f6s.com/companies/automation/india/co',
    'https://10times.com/india/it-computer',
    'https://conferencealerts.co.in/it-computer',
    'https://www.eventalways.com/india/it-automation'
][:max_sources]


progress_bar = st.progress(0)
status_text = st.empty()


# Analysis Button
if st.button("🚀 START ALL INDIA SCAN", type="primary", use_container_width=True):
    with st.spinner(f"🔍 Scanning {len(INDIA_LOCATIONS)} cities + 7 business types for '{keyword}'..."):
        all_location_data = []
        all_business_data = []
        
        for i, url in enumerate(automation_sources):
            status_text.text(f"[{i+1}/{len(automation_sources)}] {url.split('/')[2]}")
            progress_bar.progress((i + 1) / len(automation_sources))
            
            df_loc = analyze_location_mentions(url, keyword)
            all_location_data.append(df_loc)
            
            df_bus, _ = analyze_business_types(url, keyword)
            all_business_data.append(df_bus)
            
            time.sleep(random.uniform(0.8, 2.0))
        
        # Aggregate Location Data
        combined_df_loc = pd.concat(all_location_data, ignore_index=True)
        summary_df_loc = combined_df_loc.groupby('Location')['Search_Mentions'].sum().reset_index()
        summary_df_loc = summary_df_loc.sort_values('Search_Mentions', ascending=False)
        
        all_cities_df = pd.DataFrame({'Location': INDIA_LOCATIONS, 'Search_Mentions': 0})
        summary_df_loc = all_cities_df.merge(summary_df_loc, on='Location', how='left', suffixes=('', '_total'))
        summary_df_loc['Search_Mentions'] = summary_df_loc['Search_Mentions_total'].fillna(0)
        summary_df_loc = summary_df_loc[['Location', 'Search_Mentions']].sort_values('Search_Mentions', ascending=False)
        
        # Aggregate Business Data
        combined_df_bus = pd.concat(all_business_data, ignore_index=True)
        summary_df_bus = combined_df_bus.groupby('Business_Type')['Mentions'].sum().reset_index()
        summary_df_bus = summary_df_bus.sort_values('Mentions', ascending=False)
        
        st.session_state.analysis_loc = summary_df_loc
        st.session_state.analysis_bus = summary_df_bus
        st.session_state.keyword = keyword
        st.session_state.scan_time = datetime.now()


# 🌟 ENHANCED DASHBOARD WITH COMPANY NAMES
if 'analysis_loc' in st.session_state:
    df_loc = st.session_state.analysis_loc.copy()
    df_bus = st.session_state.analysis_bus.copy()
    
    # FEATURE 1: Advanced Metrics Row
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1: st.markdown('<div class="metric-card">Total Cities<br><h2 style="font-size:2rem;">21</h2></div>', unsafe_allow_html=True)
    with col2: 
        top_city = df_loc.iloc[0]
        st.markdown(f'<div class="metric-card">🏆 Top City<br>{top_city["Location"]}<br><h3>{int(top_city["Search_Mentions"])}</h3></div>', unsafe_allow_html=True)
    with col3: st.markdown(f'<div class="metric-card">Total Mentions<br><h2>{int(df_loc["Search_Mentions"].sum()):,}</h2></div>', unsafe_allow_html=True)
    with col4: 
        top_business = df_bus.iloc[0]
        st.markdown(f'<div class="metric-card">🎯 Top Business<br>{top_business["Business_Type"]}<br><h3>{int(top_business["Mentions"])}</h3></div>', unsafe_allow_html=True)
    with col5: 
        active_bus = len(df_bus[df_bus['Mentions'] > 0])
        st.markdown(f'<div class="metric-card">Active Sectors<br><h2>{active_bus}</h2></div>', unsafe_allow_html=True)
    with col6: st.markdown(f'<div class="metric-card">Last Scan<br>{st.session_state.scan_time.strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # *** BUSINESS TYPE HEATMAP WITH COMPANIES ***
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🎯 कौन सा Business IT Automation खोज रहा है?")
        fig_bus = px.bar(df_bus, x='Mentions', y='Business_Type', 
                        orientation='h', color='Mentions',
                        color_continuous_scale='Viridis',
                        title=f"Business Type Analysis - Keyword: {st.session_state.keyword}")
        fig_bus.update_layout(height=500, margin=dict(l=200))
        st.plotly_chart(fig_bus, use_container_width=True)
    
    with col2:
        st.markdown("### 💼 Business + Top Companies")
        for idx, row in df_bus.head(4).iterrows():
            btype = row['Business_Type']
            mentions = int(row['Mentions'])
            companies = COMPANY_MAPPING.get(btype, ['N/A', 'N/A'])
            pct = row["Mentions"]/df_bus["Mentions"].sum()*100 if df_bus["Mentions"].sum() > 0 else 0
            
            st.markdown(f'''
                <div class="business-card">
                    <h3>{btype}</h3>
                    <h2 style="font-size:2.5rem;">{mentions}</h2>
                    <p>{companies[0]} • {companies[1]}</p>
                 
                </div>
            ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # FEATURE 2: India Map Visualization
    st.subheader("🗺️ India Heatmap - IT Automation Hotspots")
    india_coords = {
        'Delhi': [28.6139, 77.2090], 'Mumbai': [19.0760, 72.8777], 'Bangalore': [12.9716, 77.5946],
        'Pune': [18.5204, 73.8567], 'Chennai': [13.0827, 80.2707], 'Hyderabad': [17.3850, 78.4867],
        'Noida': [28.5355, 77.3910], 'Gurgaon': [28.4595, 77.0266], 'Nashik': [20.0115, 73.7864],
        'Lucknow': [26.8467, 80.9462], 'Ahmedabad': [23.0225, 72.5714]
    }
    
    df_map = df_loc.head(10).copy()
    df_map['lat'] = df_map['Location'].map(lambda x: india_coords.get(x, [20, 78])[0])
    df_map['lon'] = df_map['Location'].map(lambda x: india_coords.get(x, [20, 78])[1])
    
    m = folium.Map(location=[22, 78], zoom_start=5)
    for idx, row in df_map.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=row['Search_Mentions']/3,
            popup=f"{row['Location']}: {int(row['Search_Mentions'])} mentions",
            color='red' if row['Search_Mentions'] > 10 else 'orange',
            fill=True,
            fillOpacity=0.7
        ).add_to(m)
    folium_static(m, width=1200, height=500)
    
    # FEATURE 3: City Rankings
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown("### 🔥 Top 12 Cities")
        top12 = df_loc.head(12)
        fig1 = px.bar(top12, x='Search_Mentions', y='Location', orientation='h',
                      color='Search_Mentions', color_continuous_scale='Plasma')
        fig1.update_layout(height=500, margin=dict(l=150))
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 All 21 Cities")
        fig2 = px.bar(df_loc, x='Search_Mentions', y='Location', orientation='h',
                      color='Search_Mentions', color_continuous_scale='Viridis_r')
        fig2.update_layout(height=700)
        st.plotly_chart(fig2, use_container_width=True)
    
    # FEATURE 4: Complete Tables + Downloads
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📋 City Rankings")
        st.dataframe(df_loc, use_container_width=True, height=300)
    with col2:
        st.markdown("### 🏢 Business Analysis")
        st.dataframe(df_bus, use_container_width=True, height=300)
    
    # Downloads
    timestamp = st.session_state.scan_time.strftime('%Y%m%d_%H%M')
    csv_loc = df_loc.to_csv(index=False).encode('utf-8')
    csv_bus = df_bus.to_csv(index=False).encode('utf-8')
    
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button("📊 Cities CSV", csv_loc, f"cities_it_automation_{timestamp}.csv")
    with col_dl2:
        st.download_button("🏢 Business CSV", csv_bus, f"business_it_automation_{timestamp}.csv")


else:
    st.info("🚀 **Keyword enter करो → Cities + Business types scan → कौन search कर रहा है देखो!**")
    st.markdown("""
    **✨ New Features:**
    • 🎯 **Dynamic Business + Company Names** - TCS • Infosys • HCLTech Live!
    • 🗺️ **India Map** with heat bubbles
    • 📱 **21 Cities** real-time ranking  
    • 💾 **Dual CSV** downloads (Cities + Business)
    • 🔄 **Auto-refresh** option
    """)
# 🌟 NEW: Combined Table with Business + Top Companies
if 'analysis_bus' in st.session_state and 'analysis_loc' in st.session_state:
    st.markdown("### 🏢 Combined Business + Top Companies Table")
    
    df_bus = st.session_state.analysis_bus.copy()
    
    # Add Top Companies column
    df_bus['Top_Companies'] = df_bus['Business_Type'].apply(lambda b: " • ".join(COMPANY_MAPPING.get(b, ['N/A', 'N/A', 'N/A'])[:3]))
    
    # Sort by Mentions descending
    df_bus = df_bus.sort_values('Mentions', ascending=False).reset_index(drop=True)
    
    st.dataframe(df_bus[['Business_Type', 'Mentions', 'Top_Companies']], use_container_width=True, height=400)
    
    # Optional: Download CSV for this combined table
    csv_combined = df_bus.to_csv(index=False).encode('utf-8')
    st.download_button("💾 Download Combined Business + Companies CSV", csv_combined,
                       f"business_companies_{st.session_state.scan_time.strftime('%Y%m%d_%H%M')}.csv")


st.markdown("---")
st.markdown("*🤖 ALL INDIA IT Automation Analyzer | Lucknow Dev | Jan 2026*")
