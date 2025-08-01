import requests
import pandas as pd
import time

def geocode_address(address, appKey):
    url = "https://apis.openapi.sk.com/tmap/geo/fullAddrGeo"
    params = {
        "version": 1,
        "format": "json",
        "appKey": appKey,
        "fullAddr": address
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        try:
            info = response.json()["coordinateInfo"]["coordinate"][0]
            lon = float(info["newLon"])
            lat = float(info["newLat"])
            return lon, lat
        except:
            print(f"⚠️ 주소 변환 실패: {address}")
            return None, None
    else:
        print(f"❌ API 오류: {response.status_code} - {address}")
        return None, None

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
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        try:
            props = response.json()["features"][0]["properties"]
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
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        try:
            path = response.json()["metaData"]["plan"]["itineraries"][0]
            return ("대중교통", path["totalDistance"], path["totalTime"])
        except:
            return ("대중교통", None, None)
    return ("대중교통", None, None)

def collect_routes_from_addresses(address_pairs, appKey):
    location_pairs = []

    for start_addr, end_addr in address_pairs:
        start = geocode_address(start_addr, appKey)
        end = geocode_address(end_addr, appKey)
        if start and end:
            location_pairs.append((start_addr, end_addr, start[0], start[1], end[0], end[1]))

    records = []

    for start_addr, end_addr, startX, startY, endX, endY in location_pairs:
        for func in [get_walk_route, get_car_route, get_transit_route]:
            method, dist, time_sec = func(startX, startY, endX, endY, appKey)
            records.append({
                "출발지주소": start_addr,
                "도착지주소": end_addr,
                "startX": startX,
                "startY": startY,
                "endX": endX,
                "endY": endY,
                "이동수단": method,
                "거리(m)": dist,
                "소요시간(초)": time_sec
            })
            time.sleep(0.1)

    df = pd.DataFrame(records)
    df = df.dropna(subset=["거리(m)", "소요시간(초)"])
    df["거리(km)"] = df["거리(m)"] / 1000
    df["소요시간(분)"] = df["소요시간(초)"] // 60

    fastest = df.loc[df.groupby(['출발지주소', '도착지주소'])['소요시간(초)'].idxmin()]
    fastest = fastest[["출발지주소", "도착지주소", "이동수단"]].rename(columns={"이동수단": "추천수단"})
    df = df.merge(fastest, on=["출발지주소", "도착지주소"], how="left")

    return df

if __name__ == "__main__":
    appKey = "여기에_당신의_TMAP_API_KEY_입력"
    address_pairs = [
        ("서울특별시 강남구 역삼동 736", "경기도 성남시 분당구 정자동 178-1"),
        ("서울특별시 서초구 반포대로 222", "서울특별시 용산구 이태원동 123-4")
    ]
    df_result = collect_routes_from_addresses(address_pairs, appKey)
    print(df_result.head())
    df_result.to_csv("routes_from_addresses.csv", index=False, encoding="utf-8-sig")
    print("📁 CSV 저장 완료: routes_from_addresses.csv")
