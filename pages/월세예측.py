# pages/월세예측기.py

import streamlit as st
import pandas as pd
import json
import pickle
import numpy as np
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="월세 예측기", layout="wide")
st.title("💡 머신러닝 기반 월세 예측기")

# JSON 데이터 로딩
@st.cache_data
def load_data():
    with open("data/land_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)

df = load_data()

# 전처리
df['floor'] = df['floorInfo'].str.extract(r'(\d+)').astype(float)
df['rent'] = pd.to_numeric(df['rentPrc'], errors='coerce')
df['deposit'] = pd.to_numeric(df['dealOrWarrantPrc'], errors='coerce')

# 인코딩 맵
house_type_map = {v: i for i, v in enumerate(df['realEstateTypeName'].dropna().unique())}
direction_map = {v: i for i, v in enumerate(df['direction'].dropna().unique())}
trade_type_map = {"월세": 0, "전세": 1}

# 인코딩 컬럼 추가
df['house_type'] = df['realEstateTypeName'].map(house_type_map)
df['direction_code'] = df['direction'].map(direction_map)
df['trade_type_code'] = df['tradeTypeName'].map(trade_type_map)

df = df.dropna(subset=['floor', 'house_type', 'direction_code', 'trade_type_code', 'rent', 'latitude', 'longitude'])

# st.session_state 초기화
if "predicted_result" not in st.session_state:
    st.session_state.predicted_result = None

# 👉 사이드바 입력 영역
st.sidebar.subheader("📋 예측 정보 입력")
floor = st.sidebar.number_input("층수", min_value=1, max_value=50, value=3)
direction = st.sidebar.selectbox("방향", list(direction_map.keys()))
house_type = st.sidebar.selectbox("집 종류", list(house_type_map.keys()))
trade_type = st.sidebar.selectbox("거래 유형", ["월세", "전세"])

predict_button = st.sidebar.button("📈 예측하기")

# 👉 예측 실행
if predict_button:
    try:
        x_input = np.array([[floor, house_type_map[house_type], direction_map[direction], trade_type_map[trade_type]]])

        with open("models/rent_model.pkl", "rb") as f:
            model, direction_map, house_type_map, trade_type_map = pickle.load(f)

        y_pred = int(model.predict(x_input)[0][0])
        st.session_state.predicted_result = {
            "y_pred": y_pred,
            "house_type": house_type,
            "direction": direction,
            "trade_type": trade_type
        }

    except Exception as e:
        st.error(f"❌ 예측 실패: {e}")

# 👉 결과 출력
if st.session_state.predicted_result:
    result = st.session_state.predicted_result
    y_pred = result["y_pred"]
    st.success(f"✅ 예측된 {result['trade_type']} 금액은 약 **{y_pred:,}만원** 입니다")

    compare_col = 'rent' if result["trade_type"] == "월세" else 'deposit'
    filtered = df[
        (df['house_type'] == house_type_map[result["house_type"]]) &
        (df['direction_code'] == direction_map[result["direction"]]) &
        (df['trade_type_code'] == trade_type_map[result["trade_type"]])
    ].copy()

    st.subheader("📍 유사 조건 매물 지도")
    m = folium.Map(location=[37.5, 127.0], zoom_start=11)
    for _, row in filtered.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"{int(row[compare_col])}만원",
            icon=folium.Icon(color='blue')
        ).add_to(m)
    st_folium(m, width=1200, height=500)

    if not filtered.empty:
        avg_price = int(filtered[compare_col].mean())
        st.metric("💡 예측값", f"{y_pred}만원")
        st.metric("🏘 실제 매물 평균", f"{avg_price}만원")
