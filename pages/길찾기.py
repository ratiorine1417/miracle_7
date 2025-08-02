import streamlit as st
import requests
import re
import folium
from streamlit_folium import st_folium
from ui.sidebar.sidebar import init_finding_path
from geopy.geocoders import Nominatim
st.set_page_config(
    page_title = "🚦 길찾기",
    layout = "wide"
)


geolocoder = Nominatim(user_agent = 'South Korea')


text, transit_into = init_finding_path()
office_info = re.sub(r"\([^)]*\)", "", text)

geo = geolocoder.geocode(office_info)
print(f"주소 좌표: {geo}")

# 1. 크롤링으로 위도, 경도에 따른 매물들을 검색
# 2. 직장 주소를 시작지점, 각 매물들을 종료지점으로 지정.
# 3. 보행자, 차량 기준으로 1km 이내, 5km 이내, 10km 이내에 대한 데이터 습득하면,
# 4. 습득한 데이터를 기반으로 어떤 매물을 추천할건지 리스트화 한다.
