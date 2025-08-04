import streamlit as st
from pathlib import Path
import requests
import json
from ui.sidebar.page_of_distance_per_method import get_coords
# 행정안전부 도로명주소 검색 API 키 (~20251031까지)
API_KEY = "	devU01TX0FVVEgyMDI1MDgwMjE1MzU0NTExNjAxNTA="

# kakao API 키
kakao_api_key = "fb1bd569e343b2b3821ea18ec1694b74"

def is_unit(code):
    code_str = str(code)
    # 길이가 10자리인 경우: 마지막 체크디지트는 제거
    if len(code_str) == 10:
        code_str = code_str[:9]

    # 읍/면/동 단위인지 판단: 뒤 4자리가 '0000'이 아니면 동단위
    return code_str[-4:] != '0000'


def address_maker(user_input):
    st.sidebar.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            min-width: 300px;  /* 최소 너비 */
            max-width: 800px;  /* 최대 너비 */
            width: 700px;      /* 고정 너비 */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    file_path = Path(__file__).resolve().parent.parent.parent / "data" / "cortar.json"
    with open(file_path, encoding="utf-8") as f:
        address_data = json.load(f)

    address = [key for key in address_data if user_input in key]
    matched_dict = {key : value for key, value in address_data.items() if user_input in key}
 
    return address, matched_dict

def search_address(keyword):
    url = "https://www.juso.go.kr/addrlink/addrLinkApi.do"
    params = {
        "confmKey": API_KEY,
        "keyword": keyword,
        "resultType": "json"
    }
    res = requests.get(url, params=params)

    return res.json()


def init_starting_path():
    st.write("🏢 회사/사무실 주소를 기입해주세요.")
    company_input = st.sidebar.text_input("📍 위치를 입력하세요.", placeholder="주소 입력 후 Enter")

    if company_input:
            respond_json = search_address(company_input)
            address_json = respond_json["results"]["juso"]
            
            if address_json:
                st.sidebar.subheader(f"🔍 관련 주소 결과")
                addr_options = ["선택해주세요."] + [
                    f"{addr['roadAddr']}"
                    for addr in address_json
                ]
                company_input = st.selectbox("📍 관련 주소 목록", addr_options)
            else:
                st.warning("주소를 상세히 입력해주세요. (예: 대방동)")
    return company_input

def init_sidebar():
    #st.sidebar.image("./image/miracle_7_logo.png", width=200)
    st.sidebar.title("🔍 필터링 검색")

    st.sidebar.subheader("💰 보증금 범위")
    deposit_range = st.sidebar.slider("단위: 만원", 0, 5000, (500, 2000), step=100, key="sidebar_deposit_slider")
    st.sidebar.subheader("💸 월세 범위")
    rent_range = st.sidebar.slider("단위: 만원", 10, 200, (30, 80), step=5, key="sidebar_rent_slider")

    st.sidebar.subheader("📍 회사/사무실 위치 선택")
    
    user_input = st.sidebar.text_input("지역을 입력하세요.", placeholder="주소 입력 후 Enter")

    coords = []
    if user_input:
        respond_json = search_address(user_input)
        address_json = respond_json["results"]["juso"]
        print(address_json)
        if address_json:
                st.sidebar.subheader(f"🔍 관련 주소 결과")
                addr_options = ["선택해주세요."] + [
                    f"{addr["roadAddr"]}"
                    for addr in address_json
                ]

                user_input = st.sidebar.selectbox("📍 관련 주소 목록", addr_options)
                coords = get_coords(user_input, kakao_api_key)

                # 다시 for문 돌려서 해당하는 도로명이 있는 인덱스의 지번주소를 들고오기기
                for addr in address_json:
                    if addr["roadAddr"] == user_input:
                         user_input = f"{addr['siNm']} {addr['sggNm']} {addr['emdNm']}"
        else:
            st.warning("주소를 상세히 입력해주세요. (예: 대방동)")
    
    else:
        st.sidebar.markdown("❌ 관련된 주소를 찾을 수 없어요.")
    
    return user_input, deposit_range, rent_range, coords
