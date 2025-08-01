import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

# --- API 호출 함수들 ---
def get_walk_route(startX, startY, endX, endY, appKey):
    url = f"https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1&format=json&appKey={appKey}"
    headers = {"Content-Type": "application/json"}
    body = {
        "startX": str(startX), "startY": str(startY),
        "endX": str(endX), "endY": str(endY),
        "reqCoordType": "WGS84GEO", "resCoordType": "WGS84GEO",
        "startName": "출발지", "endName": "도착지"
    }
    r = requests.post(url, headers=headers, json=body)
    if r.status_code == 200:
        try:
            props = r.json()["features"][0]["properties"]
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
    r = requests.post(url, headers=headers, json=body)
    if r.status_code == 200:
        try:
            props = r.json()["features"][0]["properties"]
            return ("자동차", props["totalDistance"], props["totalTime"])
        except:
            return ("자동차", None, None)
    return ("자동차", None, None)

def get_transit_route(startX, startY, endX, endY, appKey):
    url = f"https://apis.openapi.sk.com/transit/routes?lang=0&format=json&appKey={appKey}"
    headers = {"Content-Type": "application/json"}
    body = {
        "startX": str(startX), "startY": str(startY),
        "endX": str(endX), "endY": str(endY),
        "count": 1
    }
    r = requests.post(url, headers=headers, json=body)
    if r.status_code == 200:
        try:
            plan = r.json()["metaData"]["plan"]["itineraries"][0]
            return ("대중교통", plan["totalDistance"], plan["totalTime"])
        except:
            return ("대중교통", None, None)
    return ("대중교통", None, None)

# --- Streamlit 앱 ---
st.set_page_config(page_title="Tmap 경로 비교기", layout="centered")
st.title("🚦 Tmap 교통수단별 경로 비교기")

# --- 입력 UI ---
appKey = st.text_input("🔑 Tmap 앱키를 입력하세요", type="password")

col1, col2 = st.columns(2)
with col1:
    start_lat = st.number_input("출발지 위도", value=37.498095, format="%.6f")
    start_lon = st.number_input("출발지 경도", value=127.027636, format="%.6f")
with col2:
    end_lat = st.number_input("도착지 위도", value=37.554722, format="%.6f")
    end_lon = st.number_input("도착지 경도", value=126.970698, format="%.6f")

# --- 세션 상태 초기화 ---
if "route_results" not in st.session_state:
    st.session_state.route_results = []

# --- 버튼 클릭 시 경로 계산 ---
if st.button("🚀 경로 비교 시작"):
    if not appKey:
        st.error("앱키를 입력해주세요.")
    else:
        results = []
        with st.spinner("경로 계산 중..."):
            for method in [get_walk_route, get_car_route, get_transit_route]:
                name, dist, time = method(start_lon, start_lat, end_lon, end_lat, appKey)
                if time is not None:
                    results.append((name, dist, time))
        st.session_state.route_results = results

# --- 결과 출력 (있을 때만) ---
if st.session_state.route_results:
    st.subheader("📊 경로 비교 결과")
    for name, dist, time in st.session_state.route_results:
        st.success(f"**{name}**: {dist:,}m / {time // 60}분 {time % 60}초")

    # 최적 경로
    best = min(st.session_state.route_results, key=lambda x: x[2])
    st.markdown(f"✅ **가장 빠른 경로: `{best[0]}`**")
    st.markdown(f"⏱️ {best[2] // 60}분 {best[2] % 60}초, 📏 {best[1]:,}m")

    # 지도 시각화
    st.subheader("🗺️ 지도 보기")
    m = folium.Map(location=[(start_lat + end_lat) / 2, (start_lon + end_lon) / 2], zoom_start=13)
    folium.Marker([start_lat, start_lon], tooltip="출발지", icon=folium.Icon(color="green")).add_to(m)
    folium.Marker([end_lat, end_lon], tooltip="도착지", icon=folium.Icon(color="red")).add_to(m)
    folium.PolyLine([(start_lat, start_lon), (end_lat, end_lon)], color="blue", weight=4).add_to(m)
    st_folium(m, width=700, height=500)