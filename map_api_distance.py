import requests
import os
from dotenv import load_dotenv
import math
import json

def load_key():
    load_dotenv()
    kakao_rest_key = f"KakaoAK {os.getenv('KAKAO_REST_API_KEY')}"
    return kakao_rest_key

# 차 기준
def get_distance_car(origin, destination):

    kakao_rest_key = load_key()

    url_distance = "https://apis-navi.kakaomobility.com/v1/directions"
    url_addr = "https://dapi.kakao.com/v2/local/search/address.json"

    ## 위도외 경도로 된 데이터를 받으면 삭제할 것/출발지는 그냥 주소로 받을 예정이면 그대로 둘 예정
    response = requests.get( 
        url_addr,
        params={"query": origin},
        headers={"Authorization": kakao_rest_key},
    ).json()
    origin = float(response['documents'][0]['x']), float(response['documents'][0]['y'])

    ## 위도외 경도로 된 데이터를 받으면 삭제할 것
    response = requests.get(
        url_addr,
        params={"query": destination},
        headers={"Authorization": kakao_rest_key},
    ).json()
    destination = float(response['documents'][0]['x']), float(response['documents'][0]['y'])

    params = {
        "origin": origin,
        "destination": destination
    }
    
    headers = {
        "Authorization": kakao_rest_key,
        "Content-Type": "application/json"
    }

    response = requests.get(url_distance, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return print(f'Error Code = {response.status_code}')
    
# 도보 기준 / 시간은 아직 구현 전
def get_distance_walk(origin, destination):
        
    kakao_rest_key = load_key()

    url_addr = "https://dapi.kakao.com/v2/local/search/address.json"

    ## 위도외 경도로 된 데이터를 받으면 삭제할 것/출발지는 그냥 주소로 받을 예정이면 그대로 둘 예정
    response = requests.get( 
        url_addr,
        params={"query": origin},
        headers={"Authorization": kakao_rest_key},
    ).json()
    addr1_x, addr1_y = float(response['documents'][0]['x']), float(response['documents'][0]['y'])

    ## 위도외 경도로 된 데이터를 받으면 삭제할 것
    response = requests.get(
        url_addr,
        params={"query": destination},
        headers={"Authorization": kakao_rest_key},
    ).json()
    addr2_x, addr2_y = float(response['documents'][0]['x']), float(response['documents'][0]['y'])

    # 출발지-목적지 거리 계산 - 오차 약 300m 정도
    r = 6371
    dlat = (addr1_x - addr2_x) * (math.pi/180) if (addr1_x - addr2_x) > 0 else (addr2_x - addr1_x) * (math.pi/180)
    dlon = (addr1_y - addr2_y) * (math.pi/180) if (addr1_y - addr2_y) > 0 else (addr1_y - addr2_y) * (math.pi/180)
    val = math.sin(dlat/2)**2 + math.cos(addr1_x*(math.pi/180)) * math.cos(addr2_x*(math.pi/180)) * (math.sin(dlon/2)**2)
    result = 2*r*math.atan2(math.sqrt(val), math.sqrt(1-val))
    return result if result < 30 else '직선 거리가 30km 이내인 경우만 도보 길찾기를 제공합니다.'

method = input('길찾기 방식을 선택해 주세요! [자동차 or 도보]: ')
if method == '자동차':
    # (json_name[latitude], json_name[longitude]), 이런 식으로 데이터 넣을 거라고 생각했습니다
    taxi_info = get_distance_car("경기 용인시 수지구 포은대로 530", "경기 용인시 수지구 죽전로 152")
    if taxi_info:
        distance = taxi_info['routes'][0]['summary']['distance']  # 오차 있음
        duration = taxi_info['routes'][0]['summary']['duration']
        print(f'거리: {round(distance/1000, 1)}km / 걸리는 시간: {round(duration/60)}분')
    else:
        print("API 호출에 실패했습니다.")
elif method == '도보':
    # (json_name[latitude], json_name[longitude]), 이런 식으로 데이터 넣을 거라고 생각했습니다
    distance = get_distance_walk("경기 용인시 수지구 포은대로 530", "경기 용인시 수지구 죽전로 152")
    if distance.isdigit():
        print(f'거리: {distance}km / 걸리는 시간: {distance*16}분')
else:
    print('잘못된 양식입니다. 다시 입력해 주세요!')