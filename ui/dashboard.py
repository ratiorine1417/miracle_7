import streamlit as st
import pandas as pd
from ui.sidebar.sidebar import init_sidebar

def show_homepage(df):
    #사이드바 불러오기기
    init_sidebar(df)

    # ---------------------
    # 지도 기반 시각화
    # ---------------------
    st.subheader("🗺️ 지도 기반 매물 시각화")


    st.markdown("""
    <div style='
        border: 2px dashed #999;
        height: 400px;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #f9f9f9;
        font-size: 20px;
        font-weight: bold;
        color: #555;
    '>
    지도 기반 매물 시각화 영역 (추후 KakaoMap 삽입 예정)
    </div>
    """, unsafe_allow_html=True)
    # st.subheader("🗺️ 지도 기반 매물 시각화")
    # m = folium.Map(location=[37.5, 127], zoom_start=11)

    # for i, row in filtered_df.iterrows():
    #     popup_text = f"{row['지역']}<br>{row['가격']}만원<br>{row['주소']}"
    #     folium.Marker([row['위도'], row['경도']], popup=popup_text).add_to(m)

    # st_data = st_folium(m, width=700, height=500)

