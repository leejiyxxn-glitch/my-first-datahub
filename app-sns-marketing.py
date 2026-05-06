import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="SNS Marketing Analytics", layout="wide")

st.title("📊 SNS Marketing Analytics Suite")
st.markdown("Professional Performance Dashboard for 2026")

# --- Sample Data ---
if 'data' not in st.session_state:
    sample_data = [
        {"Campaign": "Spring Sale", "Platform": "Instagram", "Budget": 1200, "Revenue": 4500, "Likes": 8500, "Comments": 400, "Shares": 120, "Followers": 50000},
        {"Campaign": "Tech Review", "Platform": "YouTube", "Budget": 3000, "Revenue": 2500, "Likes": 12000, "Comments": 800, "Shares": 2000, "Followers": 150000},
        {"Campaign": "Dance Challenge", "Platform": "TikTok", "Budget": 800, "Revenue": 3200, "Likes": 45000, "Comments": 1200, "Shares": 5000, "Followers": 25000}
    ]
    st.session_state.data = pd.DataFrame(sample_data)

# --- Sidebar Input ---
with st.sidebar:
    st.header("Add New Campaign")
    c_name = st.text_input("Campaign Name")
    platform = st.selectbox("Platform", ["Instagram", "TikTok", "YouTube"])
    budget = st.number_input("Budget ($)", min_value=0.0, value=500.0)
    rev = st.number_input("Revenue ($)", min_value=0.0, value=1000.0)
    foll = st.number_input("Followers", min_value=1, value=10000)

    if st.button("Add Data"):
        new_row = {"Campaign": c_name, "Platform": platform, "Budget": budget, "Revenue": rev, "Followers": foll, "Likes": 0, "Comments": 0, "Shares": 0}
        st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)

df = st.session_state.data
df['ROI (%)'] = ((df['Revenue'] - df['Budget']) / df['Budget']) * 100
df['Eng. Rate (%)'] = ((df['Likes'] + df['Comments'] + df['Shares']) / df['Followers']) * 100

# --- Metrics ---
m1, m2, m3 = st.columns(3)
m1.metric("Avg ROI", f"{df['ROI (%)'].mean():.1f}%")
m2.metric("Total Spend", f"${df['Budget'].sum():,.0f}")
m3.metric("Top Platform", df.loc[df['ROI (%)'].idxmax(), 'Platform'])

# --- Chart & Status ---
col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Weekly Trend (Mockup)")
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['IG', 'TT', 'YT'])
    st.line_chart(chart_data)

with col2:
    st.subheader("ROI Status")
    for _, row in df.iterrows():
        color = "green" if row['ROI (%)'] >= 100 else "red"
        st.markdown(f"**{row['Campaign']}**: <span style='color:{color}'>{row['ROI (%)']:.1f}%</span>", unsafe_allow_html=True)

st.dataframe(df, use_container_width=True)
