##sidebar.py

import streamlit as st

def init_sidebar(df):
    st.sidebar.title("🔍 필터링 검색")

    cities = df['시'].unique()
    selected_city = st.sidebar.selectbox("시", cities)

    districts = df[df['시'] == selected_city]['구'].unique()
    selected_district = st.sidebar.selectbox("구", districts)

    towns = df[(df['시'] == selected_city) & (df['구'] == selected_district)]['동'].unique()
    selected_town = st.sidebar.selectbox("동", towns)

    selected_location = f"{selected_city} {selected_district} {selected_town}"

    
    # ✅ 보증금 필터 추가
    deposit_range = st.sidebar.slider("💰 보증금 범위 (만원)", 0, 10000, (500, 2000), step=100)

    # ✅ 월세 필터 추가
    rent_range = st.sidebar.slider("💸 월세 범위 (만원)", 0, 500, (30, 80), step=5)

    # 페이지 선택
    with st.sidebar:
        st.header("📊 페이지 선택")
        option = st.selectbox("페이지 선택", ["홈", "집값 예측"])

    return option, selected_location, deposit_range, rent_range
