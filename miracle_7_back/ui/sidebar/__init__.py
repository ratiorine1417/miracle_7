#init.py

import streamlit as st

def init_sidebar(df):
    st.sidebar.title("🔍 필터링 검색")

    # 1. 지역 선택 (시 → 구 → 동)
    cities = df['시'].unique()
    selected_city = st.sidebar.selectbox("시", cities)

    districts = df[df['시'] == selected_city]['구'].unique()
    selected_district = st.sidebar.selectbox("구", districts)

    towns = df[(df['시'] == selected_city) & (df['구'] == selected_district)]['동'].unique()
    selected_town = st.sidebar.selectbox("동", towns)

    selected_location = f"{selected_city} {selected_district} {selected_town}"

    # 2. 보증금 슬라이더 (단위: 만원)
    deposit_range = st.sidebar.slider(
        "💰 보증금 범위 (만원)", 
        min_value=0, max_value=10000, value=(500, 2000), step=100
    )

    # 3. 월세 슬라이더 (단위: 만원)
    rent_range = st.sidebar.slider(
        "💸 월세 범위 (만원)", 
        min_value=0, max_value=500, value=(30, 80), step=5
    )

    # 4. 페이지 선택
    st.sidebar.header("📊 페이지 선택")
    option = st.sidebar.selectbox("페이지 선택", ["홈", "집값 예측"])

    return option, selected_location, deposit_range, rent_range
