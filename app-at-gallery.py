import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="Art Gallery Dashboard", layout="wide", page_icon="🎨")

# 커스텀 CSS로 분위기 살리기
st.markdown("""
    <style>
    .main { background-color: #fdfcf0; }
    stMetric { background-color: #ffffff; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎨 Modern Art Gallery Dashboard")
st.markdown("Welcome to the digital curator's desk. Manage your collection with style.")

# --- 1. 샘플 데이터 로드 ---
if 'gallery_data' not in st.session_state:
    samples = [
        {"Title": "Starry Night", "Artist": "Vincent van Gogh", "Year": 1889, "Medium": "Oil on Canvas", "Price": 100000000, "Period": "Post-Impressionism"},
        {"Title": "The Persistence of Memory", "Artist": "Salvador Dalí", "Year": 1931, "Medium": "Oil on Canvas", "Price": 50000000, "Period": "Surrealism"},
        {"Title": "The Kiss", "Artist": "Gustav Klimt", "Year": 1907, "Medium": "Oil and Gold Leaf", "Price": 135000000, "Period": "Symbolism"},
        {"Title": "Girl with a Pearl Earring", "Artist": "Johannes Vermeer", "Year": 1665, "Medium": "Oil on Canvas", "Price": 30000000, "Period": "Dutch Golden Age"},
        {"Title": "Campbell's Soup Cans", "Artist": "Andy Warhol", "Year": 1962, "Medium": "Synthetic Polymer Paint", "Price": 12000000, "Period": "Pop Art"}
    ]
    st.session_state.gallery_data = pd.DataFrame(samples)

# --- 2. 사이드바: 새로운 작품 추가 ---
with st.sidebar:
    st.header("✨ Add New Masterpiece")
    with st.form("art_form", clear_on_submit=True):
        new_title = st.text_input("Title")
        new_artist = st.text_input("Artist")
        new_year = st.number_input("Year", min_value=0, max_value=2026, value=2024)
        new_medium = st.selectbox("Medium", ["Oil on Canvas", "Sculpture", "Digital", "Mixed Media", "Photography"])
        new_price = st.number_input("Estimated Price ($)", min_value=0)
        new_period = st.text_input("Art Period (e.g., Renaissance)")

        submit = st.form_submit_button("Add to Collection")
        if submit and new_title and new_artist:
            new_entry = {
                "Title": new_title, "Artist": new_artist, "Year": new_year,
                "Medium": new_medium, "Price": new_price, "Period": new_period
            }
            st.session_state.gallery_data = pd.concat([st.session_state.gallery_data, pd.DataFrame([new_entry])], ignore_index=True)
            st.success(f"Added '{new_title}' successfully!")

# --- 3. 메인 영역: 필터 및 테이블 ---
df = st.session_state.gallery_data

# 검색 필터
search_query = st.text_input("🔍 Search by Artist Name", "").lower()
filtered_df = df[df['Artist'].str.lower().str.contains(search_query)]

st.subheader("🖼️ Collection Catalog")
st.dataframe(filtered_df.style.format({"Price": "${:,.0f}"}).background_gradient(subset=['Price'], cmap='YlGnBu'), use_container_width=True)

# --- 4. 시각화 영역 ---
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Price Analysis")
    fig_bar = px.bar(filtered_df, x='Title', y='Price', color='Artist',
                     text_auto='.2s', title="Artwork Price Comparison",
                     color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("🕰️ Period Distribution")
    fig_pie = px.pie(filtered_df, names='Period', values='Price',
                     hole=0.4, title="Value Distribution by Period",
                     color_discrete_sequence=px.colors.qualitative.Prism)
    st.plotly_chart(fig_pie, use_container_width=True)

# 하단 통계
st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("Total Artworks", len(df))
m2.metric("Total Collection Value", f"${df['Price'].sum():,.0f}")
m3.metric("Featured Period", df['Period'].mode()[0] if not df.empty else "N/A")
