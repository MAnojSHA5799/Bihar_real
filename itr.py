import requests
import pandas as pd
import time
import random
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np
import warnings
import openpyxl  # Excel formatting ke liye

# ==============================================
# FONT WARNING FIX - TOP OF FILE
# ==============================================
plt.rcParams['font.family'] = ['DejaVu Sans', 'Arial', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
warnings.filterwarnings("ignore", category=FutureWarning)

BASE_URL = "https://suggestqueries.google.com/complete/search"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print(f"🚀 COMPLETE ITR FORM ANALYSIS Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
overall_start = time.time()

# ==============================================
# IMPROVED ITR FORM CATEGORIES + KEYWORD MAPPING
# ==============================================
itr_categories = {
    'ITR1_SAHAAJ': {
        'keywords': ['itr 1', 'itr1', 'sahaj', 'sahaj itr', 'salary itr', 'salaried itr', 'simple itr', 'easy itr', 'employee itr', 'itr1 form'],
        'who': 'Salaried <= Rs50L, 1 House Property, Agriculture <= Rs5K',
        'percentage': '65%'
    },
    'ITR2_COMPLEX': {
        'keywords': ['itr 2', 'itr2', 'itr2 form', 'capital gain itr', 'capital gains', 'house property itr', 'multiple house', 'foreign income itr', 'foreign income', 'director itr'],
        'who': 'Salaried > Rs50L, Capital Gains, Multiple Properties, Foreign Income',
        'percentage': '20%'
    },
    'ITR3_BUSINESS': {
        'keywords': ['itr 3', 'itr3', 'itr3 form', 'business itr', 'proprietor itr', 'professional itr', 'audit itr', 'firm itr', 'business income'],
        'who': 'Proprietors, Professionals, Partnership (Audited Books)',
        'percentage': '10%'
    },
    'ITR4_SUGAM': {
        'keywords': ['itr 4', 'itr4', 'sugam', 'sugam itr', 'presumptive itr', 'small business itr', 'freelancer itr', '44ad', '44ada'],
        'who': 'Small Business <= Rs2Cr turnover, Freelancers (44AD/44ADA)',
        'percentage': '5%'
    }
}

service_categories = {
    'ONLINE_PORTAL': ['online', 'website', 'app', 'portal', 'digital', 'e filing', 'efiling', 'cleartax', 'tax2win', 'efile'],
    'CA_CONSULTANT': ['ca ', 'chartered accountant', 'consultant', 'expert', 'professional', 'advisor', 'accountant', 'ca near'],
    'FORMS_DOCS': ['form 16', 'form16', 'form 1', 'form 2', 'form 3', 'form 4', 'documents', 'annexure'],
    'DEADLINE_PANIC': ['last date', 'due date', 'deadline', '31 july', '31st july', 'urgent', 'aaj', 'late fee'],
    'REFUND_TRACK': ['refund', 'refund status', 'track refund', 'my refund', 'refund check'],
    'HINDI_QUERIES': ['kaise', 'कैसे', 'भरे', 'भरें', 'करें', 'क्या', 'है', 'file kaise']
}

time_categories = {
    'MORNING_PEAK': ['morning', '9am', '10am', 'early', 'सुबह'],
    'EVENING_PEAK': ['evening', '7pm', '8pm', 'late', 'रात'],
    'DEADLINE_PANIC': ['last day', 'last hour', 'urgent', 'aaj', 'आज'],
    'WEEKEND_PEAK': ['saturday', 'sunday', 'weekend'],
    'NIGHT_OWL': ['midnight', '12am', '1am']
}

cities = [
    "delhi","mumbai","bangalore","bengaluru","hyderabad","chennai","kolkata","pune","ahmedabad",
    "jaipur","lucknow","bhopal","patna","ranchi","raipur","chandigarh","dehradun","kanpur","noida",
    "gurgaon","surat","indore","vadodara","coimbatore","visakhapatnam","nagpur"
]

all_keywords = set()
section_times = {}

def get_suggestions(query):
    """Get Google autocomplete suggestions with better error handling"""
    params = {
        "client": "firefox", 
        "q": query,
        "hl": "en-IN"  # India specific
    }
    try:
        response = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data[1] if len(data) > 1 else []
        else:
            print(f"⚠ HTTP {response.status_code}: {query[:30]}...")
            return []
    except Exception as e:
        print(f"❌ Error {query[:25]}...: {str(e)[:40]}")
        return []

def improved_detection(keyword):
    """IMPROVED Detection Logic - Priority + Exact Matching"""
    kw_lower = keyword.lower().strip()
    
    # 1. EXACT ITR FORM MATCHING (Highest Priority)
    itr_keywords_all = []
    for form_code, form_data in itr_categories.items():
        itr_keywords_all.extend(form_data['keywords'])
    
    for form_code, form_data in itr_categories.items():
        for kw in form_data['keywords']:
            if kw in kw_lower:  # Exact substring match
                return form_code, itr_categories[form_code]['who']
    
    # 2. Time Categories
    for tcat, twords in time_categories.items():
        if any(word in kw_lower for word in twords):
            return f"TIME_{tcat}", f"Peak Time: {tcat.replace('_', ' ').title()}"
    
    # 3. Service Categories
    for scat, swords in service_categories.items():
        if any(word in kw_lower for word in swords):
            return scat, f"Service: {scat.replace('_', ' ').title()}"
    
    return 'GENERAL', 'Generic ITR Query'

def time_track(func_name):
    """Execution time tracking decorator"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            section_times[func_name] = f"{elapsed:.1f}s"
            print(f"✅ {func_name}: {elapsed:.1f}s")
            return result
        return wrapper
    return decorator

# ==============================================
# 1. ENHANCED ITR FORM COLLECTION
# ==============================================
@time_track("ITR Forms Collection")
def collect_itr_forms():
    itr_queries = []
    for form_code, form_data in itr_categories.items():
        for kw in form_data['keywords']:
            itr_queries.extend([
                f"{kw} kaise bhare",
                f"{kw} online", 
                f"{kw} help",
                f"file {kw}",
                f"{kw} form",
                f"how to {kw}"
            ])
    # Limit to avoid blocking
    for query in itr_queries[:80]:
        suggestions = get_suggestions(query)
        for s in suggestions:
            if s and len(s) > 3:  # Filter short/noisy suggestions
                all_keywords.add(s.lower())
        time.sleep(random.uniform(0.8, 1.5))

collect_itr_forms()

# ==============================================
# 2. CITY + ITR FORM COMBINATIONS
# ==============================================
@time_track("City + ITR Forms")
def collect_city_forms():
    for city in cities[:20]:  # Top 20 cities first
        form_queries = [
            f"itr 1 {city}",
            f"itr 2 {city}", 
            f"itr 3 {city}",
            f"itr 4 {city}",
            f"itr filing {city}",
            f"{city} itr"
        ]
        for query in form_queries:
            suggestions = get_suggestions(query)
            for s in suggestions:
                if s and len(s) > 3:
                    all_keywords.add(s.lower())
            time.sleep(random.uniform(0.6, 1.2))

collect_city_forms()

# ==============================================
# 3. BASELINE + SERVICE KEYWORDS
# ==============================================
@time_track("Baseline Keywords")
def collect_baseline():
    seed_keywords = [
        "itr filing", "income tax return", "file itr", "itr kaise bhare",
        "tax return", "itr form", "income tax filing"
    ]
    for keyword in seed_keywords:
        # A-Z expansion
        for letter in "abcdefghijklmnopqrstuvwxyz":
            query = f"{keyword} {letter}"
            suggestions = get_suggestions(query)
            for s in suggestions:
                if s and len(s) > 3:
                    all_keywords.add(s.lower())
            time.sleep(random.uniform(0.5, 1.0))

collect_baseline()

print(f"\n⏱️ TOTAL COLLECTION COMPLETE: {time.time() - overall_start:.1f}s")
print(f"📊 Total Unique Keywords: {len(all_keywords):,}")

# ==============================================
# MAIN ANALYSIS DATAFRAME
# ==============================================
print("🔍 PROCESSING KEYWORDS...")
df = pd.DataFrame(list(all_keywords), columns=["Keyword"]).sort_values('Keyword').reset_index(drop=True)

# Apply IMPROVED detection
df[['ITR_Form_Code', 'ITR_Form_Description']] = df['Keyword'].apply(
    lambda x: pd.Series(improved_detection(x))
)

df['Collect_DateTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Location Detection (Optimized)
print("📍 DETECTING LOCATIONS...")
df['Detected_Location'] = None
location_hits = 0
for i, keyword in enumerate(df["Keyword"]):
    kw_lower = keyword.lower()
    for city in cities:
        if city.lower() in kw_lower and len(city) > 3:
            df.loc[i, 'Detected_Location'] = city.title()
            location_hits += 1
            break

print(f"📍 Locations matched: {location_hits}/{len(df)} ({location_hits/len(df)*100:.1f}%)")

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# ==============================================
# SAVE CORE FILES
# ==============================================
df.to_csv(f"itr_complete_analysis_{timestamp}.csv", index=False, encoding='utf-8')
print(f"✅ Saved: itr_complete_analysis_{timestamp}.csv")

# ==============================================
# MASTER SUMMARY TABLE (IMPROVED)
# ==============================================
print("\n" + "="*120)
print("📊 COMPLETE MASTER SUMMARY TABLE")
print("="*120)

# Create master dataframe
master_df = df.groupby(['ITR_Form_Code', 'Detected_Location']).size().reset_index(name='Keyword_Volume')

# Enhanced descriptions
itr_desc_map = {
    'ITR1_SAHAAJ': 'ITR-1 Sahaj (Salaried <= Rs50L, 1 House)',
    'ITR2_COMPLEX': 'ITR-2 (Capital Gains, Multiple Properties)',
    'ITR3_BUSINESS': 'ITR-3 (Business, Professionals, Audit)',
    'ITR4_SUGAM': 'ITR-4 Sugam (Small Business, Freelancers)',
    'CA_CONSULTANT': 'CA Services Demand',
    'ONLINE_PORTAL': 'Online Tools (ClearTax, eFiling)',
    'DEADLINE_PANIC': 'Urgent/Deadline Queries',
    'REFUND_TRACK': 'Refund Status Queries',
    'FORMS_DOCS': 'Forms & Documents',
    'GENERAL': 'Generic ITR Queries'
}

master_df['ITR_Description'] = master_df['ITR_Form_Code'].map(itr_desc_map).fillna('Other')
master_df['Market_Share_%'] = (master_df['Keyword_Volume'] / len(df) * 100).round(2)
master_df['Rank'] = master_df['Keyword_Volume'].rank(ascending=False, method='dense').astype(int)

# Sort properly
master_table_final = master_df.sort_values(['Keyword_Volume', 'Detected_Location'], ascending=[False, True]).reset_index(drop=True)

# Display TOP 25
print("\n🎯 TOP 25 RESULTS:")
print("-" * 140)
display_cols = ['Rank', 'ITR_Form_Code', 'ITR_Description', 'Detected_Location', 'Keyword_Volume', 'Market_Share_%']
print(master_table_final[display_cols].head(25).to_string(index=False, max_colwidth=35))

# GRAND TOTALS
total_keywords = len(df)
total_cities = df['Detected_Location'].nunique() - 1 if df['Detected_Location'].nunique() > 1 else 0
total_forms = df['ITR_Form_Code'].nunique()

grand_totals_row = pd.DataFrame({
    'Rank': ['TOTAL'],
    'ITR_Form_Code': [f'{total_keywords:,}'],
    'ITR_Description': ['Keywords'],
    'Detected_Location': [f'{total_cities} Cities'],
    'Keyword_Volume': [f'{total_forms} Categories'],
    'Market_Share_%': ['100.0%']
})

print("\n" + "="*140)
print("🏆 GRAND TOTALS:")
print("-" * 140)
print(pd.concat([master_table_final[display_cols].head(5), grand_totals_row], ignore_index=True).to_string(index=False, max_colwidth=35))

# Save Master Files
master_filename = f"itr_master_table_{timestamp}.csv"
master_table_final.to_csv(master_filename, index=False, encoding='utf-8')
print(f"\n✅ MASTER TABLE: {master_filename} ({len(master_table_final)} rows)")

# Excel export
try:
    master_table_final[display_cols].to_excel(f"itr_master_excel_{timestamp}.xlsx", index=False)
    print(f"✅ EXCEL: itr_master_excel_{timestamp}.xlsx")
except:
    print("⚠ Excel export skipped (openpyxl not installed)")

# ==============================================
# SUMMARY STATISTICS
# ==============================================
summary = df['ITR_Form_Code'].value_counts().reset_index()
summary.columns = ['ITR_Form', 'Keyword_Count']
summary['Market_Share'] = (summary['Keyword_Count'] / len(df) * 100).round(1)
summary.to_csv(f"itr_summary_{timestamp}.csv", index=False)

print(f"\n📈 ITR FORM BREAKDOWN:")
print(summary.head(10).round(1).to_string(index=False))

print(f"\n🎉 ANALYSIS COMPLETE: {time.time()-overall_start:.1f}s")
print(f"📁 Files Generated: 5 CSV/Excel files")
print(f"🔥 Total Keywords Collected: {len(df):,}")














# import requests
# import pandas as pd
# import time
# import matplotlib.pyplot as plt
# import seaborn as sns

# BASE_URL = "https://suggestqueries.google.com/complete/search"
# HEADERS = {"User-Agent": "Mozilla/5.0"}

# seed_keywords = [
#     "itr filing",
#     "income tax return",
#     "file itr",
#     "itr kaise bhare",
#     "itr last date",
#     "itr refund",
#     "itr form",
# ]

# cities = [
#     "delhi", "mumbai", "bangalore", "hyderabad",
#     "pune", "chennai", "kolkata", "ahmedabad",
#     "jaipur", "lucknow"
# ]

# all_keywords = set()

# def get_suggestions(query):
#     params = {"client": "firefox", "q": query}
#     try:
#         response = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=5)
#         return response.json()[1]
#     except:
#         return []

# print("🔍 Collecting keyword suggestions...")

# # A-Z expansion
# for keyword in seed_keywords:
#     for char in "abcdefghijklmnopqrstuvwxyz":
#         query = f"{keyword} {char}"
#         suggestions = get_suggestions(query)
#         for s in suggestions:
#             all_keywords.add(s.lower())
#         time.sleep(0.4)

# # City based
# print("📍 Collecting city intent searches...")
# for city in cities:
#     query = f"itr filing in {city}"
#     suggestions = get_suggestions(query)
#     for s in suggestions:
#         all_keywords.add(s.lower())
#     time.sleep(0.4)

# # Near me
# near_me_queries = [
#     "itr filing near me",
#     "ca for itr near me",
#     "income tax return help near me"
# ]

# for query in near_me_queries:
#     suggestions = get_suggestions(query)
#     for s in suggestions:
#         all_keywords.add(s.lower())
#     time.sleep(0.4)

# # ------------------------------------------
# # SAVE KEYWORDS
# # ------------------------------------------
# df = pd.DataFrame(sorted(all_keywords), columns=["Keyword"])
# df.to_csv("itr_keywords_full_list.csv", index=False)

# print(f"\n✅ Total Keywords Collected: {len(df)}")

# # ------------------------------------------
# # LOCATION DETECTION
# # ------------------------------------------
# location_data = []

# for kw in df["Keyword"]:
#     found_city = None
#     for city in cities:
#         if city in kw:
#             found_city = city.title()
#             break

#     if "near me" in kw:
#         found_city = "Near Me"

#     location_data.append(found_city)

# df["Detected_Location"] = location_data

# # Count demand per location
# location_summary = df["Detected_Location"].value_counts().dropna()

# print("\n📊 Location-wise Search Intent")
# print(location_summary)

# location_summary.to_csv("itr_location_demand.csv")

# # ------------------------------------------
# # HEATMAP VISUAL
# # ------------------------------------------
# plt.figure(figsize=(8,5))
# sns.heatmap(location_summary.to_frame(), annot=True, cmap="Reds", fmt="g")
# plt.title("ITR Search Location Demand (Keyword Intent Based)")
# plt.show()
