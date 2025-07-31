import streamlit as st
import pandas as pd
from ui.dashboard import show_homepage
from ui.sidebar import init_sidebar

st.set_page_config(
    page_title="7번방의 기적",
    layout="wide",
    initial_sidebar_state="collapsed"
)



# 샘플 매물 데이터 
# 2025.07.30 백두현
# TODO: 크롤링, api 호출 데이터 들어오면 여기서 호출 구조로 변경해야함.
df = pd.DataFrame({
    '시': ['서울특별시'] * 3,
    '구': ['강남구', '마포구', '송파구'],
    '동': ['역삼동', '서교동', '잠실동'],
    '보증금': [1000, 500, 1500],
    '월세': [80, 55, 72],
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



# 🔹 2. 사용자 입력값 사이드바로부터 받기
selected_location, deposit_range, rent_range = init_sidebar(df)

# 🔹 3. 지역 문자열 분해 (서울특별시 강남구 역삼동)
try:
    city, district, town = selected_location.split()
except ValueError:
    city, district, town = "", "", ""

# 🔹 4. 필터링 적용
filtered_df = df[
    (df['시'] == city) &
    (df['구'] == district) &
    (df['동'] == town) &
    (df['보증금'] >= deposit_range[0]) & (df['보증금'] <= deposit_range[1]) &
    (df['월세'] >= rent_range[0]) & (df['월세'] <= rent_range[1])
]




st.title("🏡 7번방의 기적")
st.write("선택한 지역:", selected_location)
st.write("보증금 범위:", deposit_range)
st.write("월세 범위:", rent_range)

# 메인화면 불러오기기
show_homepage(filtered_df)

