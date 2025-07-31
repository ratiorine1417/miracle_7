import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 상위 디렉토리 경로 등록
from data.database import init_db, get_connection
import streamlit as st
import pandas as pd
from ui.sidebar.sidebar import init_sidebar
import folium
from streamlit.components.v1 import html


def show_homepage(df):
    # TODO: 이제 로그인 시 사용자마다 값을 저장할수있게 로직을 처리해보자! 20250731 백두현현
    #init_db()

    # ---------------------
    # 지도 기반 시각화
    # ---------------------
    st.subheader("🗺️ 지도 기반 매물 시각화")

    center_longitude = float(df[0]["longitude"])
    center_latitude  = float(df[0]["latitude"])
    map_center = [center_latitude, center_longitude]


    # 지도 표출
    map = folium.Map(location=map_center, zoom_start=30)


    # 크롤링된 매물들 처리
    for listing in df:
        popup_html = f"""
                    <div style="width:auto">
                        <br>
                        <h4>매물 정보</h4>
                        {listing["tradeTypeName"]} {listing["sameAddrMaxPrc"]}<br><br>
                        <h4>매물 특징</h4>
                        {listing["tagList"]}
                    </div>
                    """
        folium.Marker([listing["latitude"], listing["longitude"]], popup=folium.Popup(popup_html, max_width=500), tooltip="클릭해서 매물보기").add_to(map)

    m_html = map._repr_html_() 
    html(m_html, height=500)

    st.subheader("📋 매물 리스트")

    standard_sort = st.selectbox("정렬 기준", ['sameAddrMaxPrc']) # 정렬 기준 
    type_sort = st.radio("정렬 방식", ['오름차순', '내림차순'])  # 정렬 방식

    ascending = True if type_sort == '오름차순' else False
    real_df = pd.DataFrame(df)
    sorted_df = real_df.sort_values(by=standard_sort, ascending=ascending)

    st.dataframe(sorted_df[['sameAddrMaxPrc']])

    # ---------------------
    # 매물 상세 정보 모달 구성 
    # ---------------------
    st.subheader("🏠 매물 상세 보기")

    for sort_item in sorted_df:
        if not sort_item.empty:
            select_house = st.selectbox("매물 선택", sort_item['sameAddrMaxPrc'].tolist())
            selected_df = sort_item[sort_item['sameAddrMaxPrc'] == select_house]

            if not selected_df.empty:
                info_house = selected_df.iloc[0]
                with st.expander("매물 상세 정보 보기"):
                    st.write("📞 주변 공인중개사: 02-1234-5678")
            else:
                st.warning("해당 매물 정보가 없습니다.")
        else:
            st.info("조건에 맞는 매물이 없습니다.")

        # if not sort_item.empty:
        #     select_house = st.selectbox("매물 선택", sort_item['주소'].tolist())
        #     selected_df = sort_item[sort_item['주소'] == select_house]

        #     if not selected_df.empty:
        #         info_house = selected_df.iloc[0]
        #         with st.expander(f"{info_house['주소']} 상세 정보 보기"):
        #             st.write(f"📍 위치: {info_house['지역']} - {info_house['주소']}")
        #             st.write(f"💰 가격: {info_house['가격']}만원")
        #             st.write(f"📐 면적: {info_house['면적']}㎡")
        #             st.write(f"🚪 방수: {info_house['방수']} / 층수: {info_house['층']}")
        #             st.write(f"🔥 난방: {info_house['난방']} / 🛗 엘리베이터: {info_house['엘리베이터']}")
        #             st.image("https://via.placeholder.com/300x200.png?text=매물+이미지", caption="샘플 이미지")
        #             st.write("📞 주변 공인중개사: 02-1234-5678")
        #     else:
        #         st.warning("해당 매물 정보가 없습니다.")
        # else:
        #     st.info("조건에 맞는 매물이 없습니다.")

