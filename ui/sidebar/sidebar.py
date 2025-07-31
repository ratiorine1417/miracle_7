import streamlit as st
from pathlib import Path
import json

def address_maker():

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

    # 행정구역코드 XX00000000 이면 시/도 단위의 코드
    si_level = {
        name: code 
        for name, code in address_data.items()
        if code % 10**8 == 0
    }
    si_level_keys = si_level.keys()

    # 행정구역코드의 뒤 5자리가 0이면서 앞 5자리는 0이 아닌코드면 시/군/구구
    gu_level = {
        name: code
        for name, code in address_data.items()
        if code % 10**5 == 0 and code % 10**8 != 0
    }
    gu_level_keys = gu_level.keys()

    # 행정구역코드의 마지막 2자리가 00이 아님 → 리/통/반 제외하면 읍/면/동 단위의 코드
    dong_level = {
        name: code
        for name, code in address_data.items()
        if code % 100 != 0  
    }
    dong_level_keys = dong_level.keys()

    return si_level_keys, gu_level_keys, dong_level_keys

def init_sidebar():
    #st.sidebar.image("./image/miracle_7_logo.png", width=200)
    st.sidebar.title("🔍 필터링 검색")

    deposit_range = st.sidebar.slider("💰 보증금 범위 (만원)", 0, 5000, (500, 2000), step=100, key="sidebar_deposit_slider")
    rent_range = st.sidebar.slider("💸 월세 범위 (만원)", 10, 200, (30, 80), step=5, key="sidebar_rent_slider")

    st.sidebar.subheader("📍 지역 선택")
    
    
    cities, districts, towns = address_maker()

    user_input = st.sidebar.text_area("지역을 입력하세요.", placeholder="주소 입력 후 ctrl + Enter")
    st.sidebar.markdown(
    """
    <style>
    textarea {
        resize: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
    )

    if user_input:
        # 시/군/구 dict에서 사용자 입력과 관련 있는 키워드 찾기
        matched_districts = [name for name in cities if user_input.strip() in name]
        matched_districts = [name for name in districts if user_input.strip() in name]
        matched_districts = [name for name in towns if user_input.strip() in name]
        if matched_districts:
            selected_location = st.sidebar.selectbox("📍 추천 주소를 선택하세요", matched_districts)
    
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
            st.sidebar.markdown("❌ 관련된 주소를 찾을 수 없어요.")
    
    return selected_location, deposit_range, rent_range
