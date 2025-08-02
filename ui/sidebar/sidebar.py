import streamlit as st
from pathlib import Path
import requests
import json
# 행정안전부 도로명주소 검색 API 키 (~20251031까지)
API_KEY = "	devU01TX0FVVEgyMDI1MDgwMjE1MzU0NTExNjAxNTA="

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

def init_finding_path():
    st.sidebar.title("🔍 직장과 가까운 매물 검색")

    st.sidebar.subheader("🏢 회사/사무실 주소를 기입해주세요.")
    company_input = st.sidebar.text_input("📍 위치를 입력하세요.", placeholder="주소 입력 후 Enter")
    
    if company_input:
        respond_json = search_address(company_input)
        address_json = respond_json["results"]["juso"]

        if address_json:
            st.sidebar.subheader(f"🔍 '{company_input}' 관련 주소 결과")
            addr_options = [
                f"{addr['roadAddr']}"
                for addr in address_json
            ]
            company_input = st.sidebar.selectbox("📍 관련 주소 목록", addr_options)

            st.success(f"✅ 선택된 주소:\n\n{company_input}")
        else:
           st.sidebar.warning("검색 결과가 없습니다.")
    
    st.sidebar.subheader("🚊 교통수단을 선택해주세요.")
    vehicles = {"🚶‍♂️ 도보":"walk", "🚇 지하철":"subway", "🚕 택시":"texi", "🚌 버스":"bus"}
    user_input = st.sidebar.selectbox("📍 교통수단", list(vehicles.keys()))
    return company_input, vehicles[user_input]

def init_sidebar():
    #st.sidebar.image("./image/miracle_7_logo.png", width=200)
    st.sidebar.title("🔍 필터링 검색")

    deposit_range = st.sidebar.slider("💰 보증금 범위 (만원)", 0, 5000, (500, 2000), step=100, key="sidebar_deposit_slider")
    rent_range = st.sidebar.slider("💸 월세 범위 (만원)", 10, 200, (30, 80), step=5, key="sidebar_rent_slider")

    st.sidebar.subheader("📍 지역 선택")
    
    user_input = st.sidebar.text_input("지역을 입력하세요.", placeholder="주소 입력 후 Enter")

    addresses = []
    if user_input:
        addresses, addresses_dict = address_maker(user_input)
    
    st.sidebar.markdown(
    """
    <style>
    text_input {
        res ize: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    if addresses:
        selected_location = st.sidebar.selectbox("📍 추천 주소를 선택하세요", addresses)
        code = addresses_dict.get(selected_location)

        print(is_unit(code))
        if is_unit(code):
            # 선택된 주소를 꾸며서 출력
            st.sidebar.markdown(
                f"""
                <div style="
                    background-color:#e6f7ff;
                    padding:10px;
                    border-radius:8px;
                    border-left:5px solid #3399ff;
                    font-size:16px;
                    color:#333;
                ">
                ✅ <strong>선택한 주소:</strong><br>{selected_location}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.warning("❗ 선택한 주소가 너무 간단해요. 자세한 지역 단위를 선택해주세요.")
    else:
        selected_location = ""
        st.sidebar.markdown("❌ 관련된 주소를 찾을 수 없어요.")
    
    return selected_location, deposit_range, rent_range
