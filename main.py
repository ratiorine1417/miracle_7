import streamlit as st
import pandas as pd
from ui.dashboard import show_homepage
from ui.sidebar.sidebar import init_sidebar
from scraping import crawling

st.set_page_config(
    page_title="7번방의 기적",
    layout="wide",
    initial_sidebar_state="collapsed"
)

#사용자 입력값 사이드바로부터 받기
selected_location, deposit_range, rent_range = init_sidebar()

# 필터링 적용
filtered_df = crawling(selected_location, deposit_range[1], deposit_range[0], rent_range[1], rent_range[0])
print("크롤링데이터" + filtered_df)
st.title("🏡 7번방의 기적")
st.write("선택한 지역:", selected_location)
st.write("보증금 범위:", deposit_range)
st.write("월세 범위:", rent_range)

print(filtered_df)

# 메인화면 불러오기
show_homepage(filtered_df)

