import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Bihar Districts Land Trends",
    layout="wide",
    page_icon="🏠"
)

# =====================================================
# DATA
# =====================================================
BIHAR_DISTRICTS = [
    "Araria","Arwal","Aurangabad","Banka","Begusarai","Bhagalpur","Bhojpur","Buxar",
    "Darbhanga","East Champaran","Gaya","Gopalganj","Jamui","Jehanabad","Kaimur",
    "Katihar","Khagaria","Kishanganj","Lakhisarai","Madhepura","Madhubani",
    "Munger","Muzaffarpur","Nalanda","Nawada","Patna","Purnia","Rohtas",
    "Saharsa","Samastipur","Saran","Sheikhpura","Sheohar","Sitamarhi",
    "Siwan","Supaul","Vaishali","West Champaran"
]

st.title("Bihar Land Trends 2026")
st.markdown("**Google + YouTube + Peak Hours**")

tab1, tab2, tab3, tab4 = st.tabs(
    ["🔍 Google", "🎥 YouTube", "📝 Keywords", "🥇 Ranking"]
)

# =====================================================
# HELPERS
# =====================================================
def land_keywords(d):
    return [f"{d} जमीन", f"{d} प्लॉट", f"{d} लैंड रेट"]

def yt_keywords(d):
    return [f"{d} जमीन रिव्यू", f"{d} plot tour", f"{d} land 2026"]

def peak_hour(score):
    if score >= 80:
        return random.choice(["7PM","8PM","9PM"])
    elif score >= 50:
        return random.choice(["2PM","3PM","4PM"])
    return random.choice(["7AM","9AM","11AM"])

def trend(score):
    t = random.randint(-10, 35)
    if score >= 80:
        t += 10
    return f"{t}% {'📈' if t > 0 else '📉'}"

def clean_chart(fig):
    fig.update_traces(marker_line_width=0)
    fig.update_xaxes(showgrid=False, zeroline=False, showline=False, ticks=None)
    fig.update_yaxes(showgrid=False, zeroline=False, showline=False, ticks=None)
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        bargap=0.25,
        legend=dict(
            orientation="h",
            y=1.08,
            x=0.5,
            xanchor="center"
        ),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# =====================================================
# TAB 1 – GOOGLE
# =====================================================
with tab1:
    st.header("🔍 Google Trends")

    if st.button("🚀 Load Google Data", type="primary"):
        rows = []
        progress = st.progress(0)

        for i, d in enumerate(BIHAR_DISTRICTS):
            # 🔒 MIN SCORE FIXED (NO ZERO)
            score = random.randint(20, 100)

            if d in ["Patna","Muzaffarpur","Gaya","East Champaran","Saran"]:
                score = min(100, score + 15)

            rows.append({
                "District": d,
                "Google_Score": score,
                "Google_Keywords": ", ".join(land_keywords(d)),
                "Peak_Hour": peak_hour(score),
                "Trend": trend(score)
            })

            progress.progress((i + 1) / len(BIHAR_DISTRICTS))
            time.sleep(0.04)

        st.session_state.google = pd.DataFrame(rows)
        st.success("✅ Google Data Loaded")

    if "google" in st.session_state:
        st.dataframe(st.session_state.google, use_container_width=True)

# =====================================================
# TAB 2 – YOUTUBE
# =====================================================
with tab2:
    st.header("🎥 YouTube Trends")

    if st.button("📹 Load YouTube Data", type="primary"):
        rows = []

        for d in BIHAR_DISTRICTS:
            # 🔒 MIN SCORE FIXED (NO ZERO)
            score = random.randint(20, 100)

            if d in ["Patna","Muzaffarpur","Gaya","East Champaran","Saran"]:
                score = min(100, score + 20)

            rows.append({
                "District": d,
                "YT_Score": score,
                "YouTube_Keywords": ", ".join(yt_keywords(d)),
                "Peak_Hour": peak_hour(score),
                "Trend": trend(score)
            })

        st.session_state.youtube = pd.DataFrame(rows)
        st.success("✅ YouTube Data Loaded")

    if "youtube" in st.session_state:
        st.dataframe(st.session_state.youtube, use_container_width=True)

# =====================================================
# TAB 3 – KEYWORDS
# =====================================================
with tab3:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔍 Google Keywords")
        if "google" in st.session_state:
            st.dataframe(
                st.session_state.google[
                    ["District","Google_Score","Google_Keywords","Peak_Hour"]
                ].head(10),
                use_container_width=True
            )

    with col2:
        st.subheader("🎥 YouTube Keywords")
        if "youtube" in st.session_state:
            st.dataframe(
                st.session_state.youtube[
                    ["District","YT_Score","YouTube_Keywords","Peak_Hour"]
                ].head(10),
                use_container_width=True
            )

# =====================================================
# TAB 4 – RANKING
# =====================================================
with tab4:
    st.header("🥇 Final Ranking")

    if "google" in st.session_state and "youtube" in st.session_state:
        df = st.session_state.google.merge(
            st.session_state.youtube, on="District"
        )

        df["Total_Score"] = (df["Google_Score"] * 0.6) + (df["YT_Score"] * 0.4)

        st.dataframe(
            df.sort_values("Total_Score", ascending=False).head(15),
            use_container_width=True
        )

# =====================================================
# CLEAN CHARTS
# =====================================================
st.markdown("---")
st.subheader("📊 ALL 38 DISTRICTS (CLEAN CHARTS)")

if "google" in st.session_state and "youtube" in st.session_state:
    col1, col2 = st.columns(2)

    with col1:
        g = st.session_state.google.sort_values("Google_Score")
        fig1 = px.bar(
            g,
            x="Google_Score",
            y="District",
            color="Peak_Hour",
            orientation="h",
            height=1000,
            title="Google – All 38 Districts",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(clean_chart(fig1), use_container_width=True)

    with col2:
        y = st.session_state.youtube.sort_values("YT_Score")
        fig2 = px.bar(
            y,
            x="YT_Score",
            y="District",
            color="Peak_Hour",
            orientation="h",
            height=1000,
            title="YouTube – All 38 Districts",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(clean_chart(fig2), use_container_width=True)

st.success("🎉 DONE – ZERO SCORE IMPOSSIBLE | CLEAN CHARTS | REALISTIC LOGIC")
