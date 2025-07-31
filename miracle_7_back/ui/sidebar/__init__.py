import streamlit as st

def init_sidebar(df):
    #st.sidebar.image("./image/miracle_7_logo.png", width=200)
    st.sidebar.title("🔍 필터링 검색")

    deposit_range = st.sidebar.slider("💰 보증금 범위 (만원)", 0, 5000, (500, 2000), step=100)
    rent_range = st.sidebar.slider("💸 월세 범위 (만원)", 10, 200, (30, 80), step=5)

    st.sidebar.subheader("📍 지역 선택")

    cities = df['시'].unique()
    selected_city = st.sidebar.selectbox("시", cities, key="city_select")

    districts = df[df['시'] == selected_city]['구'].unique()
    selected_district = st.sidebar.selectbox("구", districts, key="district_select")

    towns = df[(df['시'] == selected_city) & (df['구'] == selected_district)]['동'].unique()
    selected_town = st.sidebar.selectbox("동", towns, key="town_select")

    selected_location = f"{selected_city} {selected_district} {selected_town}"

    return selected_location, deposit_range, rent_range
