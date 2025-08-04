import streamlit as st
import requests
import itertools
import pandas as pd
from streamlit_folium import st_folium
from scraping.crawling import crawling
import time
from geopy.geocoders import Nominatim
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import base64

# kakao API 키
kakao_api_key = "fb1bd569e343b2b3821ea18ec1694b74"
# TMAP API 키
tmap_api_key = "KXgnElYbnf9P4rPyZzanN91cHMyScabF1ZY4ifZR"

region_map = {
    "서울": "서울특별시",
    "경기": "경기도",
    "부산": "부산광역시",
    "인천": "인천광역시",
    "대구": "대구광역시",
    "광주": "광주광역시",
    "대전": "대전광역시",
    "울산": "울산광역시",
    "세종": "세종특별자치시",
    "강원": "강원특별자치도",
    "충북": "충청북도",
    "충남": "충청남도",
    "전북": "전라북도",
    "전남": "전라남도",
    "경북": "경상북도",
    "경남": "경상남도",
    "제주": "제주특별자치도"
}

st.set_page_config(
    page_title = "🚦 길찾기",
    layout = "wide"
)

def update_region_name(address_name):
    parts = address_name.split()
    if not parts:
        return address_name  # 비어있는 경우 그대로 반환
    region_key = parts[0]
    full_region = region_map.get(region_key)
    if full_region:
        parts[0] = full_region  # 변환된 명칭으로 교체
        return " ".join(parts)
    return address_name  # 변환 대상 아님

def get_route(startX, startY, endX, endY, appKey, method):
    if method == "🚶‍♂️ 도보":
        tmp = get_walk_route(startX, startY, endX, endY, tmap_api_key)
    elif method == "🚌 자동차":
        tmp = get_car_route(startX, startY, endX, endY, tmap_api_key)

    return convert_distance_time(tmp)

def get_walk_route(startX, startY, endX, endY, appKey):
    url = f"https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1&format=json&appKey={appKey}"
    headers = {"Content-Type": "application/json"}
    body = {
        "startX": str(startX), "startY": str(startY),
        "endX": str(endX), "endY": str(endY),
        "reqCoordType": "WGS84GEO", "resCoordType": "WGS84GEO",
        "startName": "출발지", "endName": "도착지"
    }
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        try:
            props = response.json()["features"][0]["properties"]
            return ("도보", props["totalDistance"], props["totalTime"])
        except:
            return ("도보", None, None)
    return ("도보", None, None)

def get_car_route(startX, startY, endX, endY, appKey):
    url = f"https://apis.openapi.sk.com/tmap/routes?version=1&format=json&appKey={appKey}"
    headers = {"Content-Type": "application/json"}
    body = {
        "startX": str(startX), "startY": str(startY),
        "endX": str(endX), "endY": str(endY),
        "reqCoordType": "WGS84GEO", "resCoordType": "WGS84GEO",
        "startName": "출발지", "endName": "도착지",
        "searchOption": 0, "trafficInfo": "Y"
    }
<<<<<<< HEAD
    response = requests.post(url, headers=headers, json=body, timeout=10)
=======
    response = requests.post(url, headers=headers, json=body)
>>>>>>> 8f26912c14d56e556fa94c3c4f8b8c6aca81d7dc

    if response.status_code == 200:
        try:
            props = response.json()["features"][0]["properties"]
            return ("자동차", props["totalDistance"], props["totalTime"])
        except:
            return ("자동차", None, None)
    return ("자동차", None, None)
    
def get_coords(address, kakao_api_key):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {kakao_api_key}"}
    params = {"query": address}
<<<<<<< HEAD
    response = requests.get(url, headers=headers, params=params, timeout=10)
=======
    response = requests.get(url, headers=headers, params=params)
>>>>>>> 8f26912c14d56e556fa94c3c4f8b8c6aca81d7dc
    result = response.json()
    if result['documents']:
        x = result['documents'][0]['x']  # 경도
        y = result['documents'][0]['y']  # 위도
        return x, y
    else:
        return None, None
    
def convert_distance_time(tuple):
    method, distance_m, time_sec = tuple[0], tuple[1], tuple[2]

    if distance_m is None or time_sec is None:
        return st.warning("❌ 거리 또는 시간 정보가 부족합니다.")

    distance_km = round(distance_m / 1000, 1)
    minutes = time_sec // 60
    seconds = time_sec % 60
    expect_minutes = round(distance_km / 5 * 60)

    return (
        f"{method}",
        f"{distance_km}km ({distance_m}m)",
        f"{minutes}분 {seconds}초"
    )

# geocoding을 reverse로 할때 정상적인 format으로 주소명 변환
def format_address(addr_dict):
    addr = addr_dict.get('address', {})
    parts = [
        addr.get('city', ''),
        addr.get('borough', ''),
        addr.get('road', ''),
        addr.get('suburb', '')
    ]
    formatted = ' '.join(filter(None, parts))
    return formatted
