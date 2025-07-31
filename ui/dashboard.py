import streamlit as st
import pandas as pd
from ui.sidebar.sidebar import init_sidebar

def show_homepage(df):
    #사이드바 불러오기
    filter_option = init_sidebar(df)
    filter_option = ['홈', ['서울 강남', '서울 마포', '서울 송파'], [20000, 40000], [300, 400]]
    
    filter_region = filter_option[1][0] # 지역
    filter_deposit_min = filter_option[2][0] # 최소 보증금
    filter_deposit_max = filter_option[2][1] # 최소 보증금
    filter_monthly_rent_min = filter_option[3][0] # 최소 월세
    filter_monthly_rent_max = filter_option[3][1] # 최대 월세
    
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

    # 필터링 적용
    filtered_df = df[
          df['지역'].isin([filter_region]) &
          df['가격'].between(filter_deposit_min, filter_deposit_max) &
          df['면적'].between(filter_monthly_rent_min, filter_monthly_rent_max)
     ]

    st.subheader("📋 매물 리스트")

    standard_sort = st.selectbox("정렬 기준", ['가격', '면적', '주소']) # 정렬 기준 [백두현: 추후 정렬 기준 대상 확대 가능]
    type_sort = st.radio("정렬 방식", ['오름차순', '내림차순'])  # 정렬 방식

    ascending = True if type_sort == '오름차순' else False
    sorted_df = filtered_df.sort_values(by=standard_sort, ascending=ascending)

    st.dataframe(sorted_df[['지역', '가격', '면적', '주소']])

    # ---------------------
    # 매물 상세 정보 모달 구성 
    # ---------------------
    st.subheader("🏠 매물 상세 보기")

    if not sorted_df.empty:
        select_house = st.selectbox("매물 선택", sorted_df['주소'].tolist())
        selected_df = sorted_df[sorted_df['주소'] == select_house]

        if not selected_df.empty:
            info_house = selected_df.iloc[0]
            with st.expander(f"{info_house['주소']} 상세 정보 보기"):
                st.write(f"📍 위치: {info_house['지역']} - {info_house['주소']}")
                st.write(f"💰 가격: {info_house['가격']}만원")
                st.write(f"📐 면적: {info_house['면적']}㎡")
                st.write(f"🚪 방수: {info_house['방수']} / 층수: {info_house['층']}")
                st.write(f"🔥 난방: {info_house['난방']} / 🛗 엘리베이터: {info_house['엘리베이터']}")
                st.image("https://via.placeholder.com/300x200.png?text=매물+이미지", caption="샘플 이미지")
                st.write("📞 주변 공인중개사: 02-1234-5678")
        else:
            st.warning("해당 매물 정보가 없습니다.")
    else:
        st.info("조건에 맞는 매물이 없습니다.")







    

