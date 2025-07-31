import streamlit as st
import pandas as pd
from ui.dashboard import show_homepage
from ui.header.header import set_header

# 헤더 세팅
set_header()

st.set_page_config(
    page_title="7번방의 기적",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 샘플 매물 데이터 
# 2025.07.30 백두현
# TODO: 크롤링, api 호출 데이터 들어오면 여기서 호출 구조로 변경해야함.
df = pd.DataFrame({
    '지역': ['서울 강남', '서울 마포', '서울 송파'],
    '가격': [80000, 55000, 72000],
    '면적': [30, 20, 25],
    '위도': [37.4979, 37.5407, 37.5065],
    '경도': [127.0276, 126.9469, 127.1060],
    '주소': ['강남역 근처', '홍대입구역 근처', '잠실역 근처'],
    '층': [10, 5, 7],
    '방수': [2, 1, 3],
    '엘리베이터': ['있음', '없음', '있음'],
    '난방': ['중앙난방', '개별난방', '지역난방']
})
################################################################

# 메인화면 불러오기
show_homepage(df)

