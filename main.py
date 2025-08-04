import streamlit as st
import pandas as pd
from ui.dashboard import show_homepage
from ui.sidebar.sidebar import init_sidebar
from scraping.crawling import crawling



st.set_page_config(
    page_title="7번방의 기적",
    page_icon="image/miracle_7_logo.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

#사용자 입력값 사이드바로부터 받기
selected_location, deposit_range, rent_range = init_sidebar()


# 필터링 적용
filtered_df = crawling(selected_location, rent_range[1], rent_range[0], deposit_range[1], deposit_range[0])

st.title("🏡 7번 방의 기적")

# 지역 이름 길이에 따라 너비 가중치 계산
location_length = len(selected_location) 
if location_length == 0:
    location_length = 1
col_ratio = min(location_length / 5, 2)  # 최대 비율 제한

col1, col2, col3 = st.columns([col_ratio, 1, 1])

col1.metric("📍 지역", selected_location, selected_location)
col2.metric("💰 보증금", f"{deposit_range[0]}~{deposit_range[1]}")
col3.metric("💸 월세", f"{rent_range[0]}~{rent_range[1]}")

# 메인화면 불러오기
if filtered_df:
    show_homepage(filtered_df, selected_location)
else:
    st.markdown(f"""
        <div style="
            background-color: #ffe6e6;
            padding: 15px;
            border-radius: 10px;
            border-left: 6px solid #ff4d4d;
            font-size: 16px;
            color: #990000;
        ">
            <strong> 검색되지 않습니다. 다시 시도해주세요. <br>
        </div>
        """, unsafe_allow_html=True)
# 수정