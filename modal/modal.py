# ui/modal_display.py
import streamlit as st
import pandas as pd
import json
from streamlit_modal import Modal

def show_property_modal():

    st.subheader("🏠 매물 목록")

    # land_data.json 파일 로드
    try:

        with open('../data/land_data.json', 'r', encoding='utf-8') as f:
            land_data = json.load(f)
        df_properties = pd.DataFrame(land_data)
    except FileNotFoundError:
        st.error("land_data.json 파일을 찾을 수 없습니다. 'data' 폴더에 파일이 있는지 확인해주세요.")
        return
    except json.JSONDecodeError:
        st.error("land_data.json 파일이 유효한 JSON 형식이 아닙니다.")
        return

    if df_properties.empty:
        st.info("land_data.json 파일에 매물 데이터가 없습니다.")
        return

    # 'articleName'과 'realEstateTypeName'을 결합하여 매물 선택 드롭다운에 표시할 이름을 만듭니다.
    # 중복을 피하기 위해 articleNo를 함께 사용하거나 고유한 식별자를 사용합니다.
    df_properties['display_name'] = df_properties['articleName'] + ' (' + df_properties['realEstateTypeName'] + ' - ' + df_properties['sameAddrMaxPrc'] + ')'
    
    # 매물 선택 드롭다운
    selected_display_name = st.selectbox(
        "상세 정보를 볼 매물을 선택하세요:", 
        df_properties['display_name'].tolist(), 
        key="select_property_for_modal"
    )

    # 선택된 매물 필터링
    selected_property_data = df_properties[df_properties['display_name'] == selected_display_name].iloc[0]

    # 모달 인스턴스 생성
    # 각 매물별로 고유한 키를 사용해야 합니다. 여기서는 articleNo를 사용합니다.
    modal = Modal(key=f"modal_{selected_property_data['articleNo']}", title="매물 상세 정보")

    # "상세 정보 보기" 버튼 클릭 시 모달 열기
    if st.button(f"'{selected_property_data['articleName']}' 상세 정보 보기", key=f"show_details_btn_{selected_property_data['articleNo']}"):
        with modal.container():
            
            deal_or_warrant_prc = selected_property_data.get('dealOrWarrantPrc', '정보 없음')
            rent_prc = selected_property_data.get('rentPrc', '정보 없음')

            # 'dealOrWarrantPrc'가 '억' 단위를 포함할 경우 처리
            if '억' in str(deal_or_warrant_prc):
                parts = deal_or_warrant_prc.replace('억', '').replace(',', '').strip().split()
                if len(parts) == 2:
                    deal_or_warrant_prc_formatted = f"{parts[0]}억 {parts[1]}"
                elif len(parts) == 1:
                    deal_or_warrant_prc_formatted = f"{parts[0]}억"
                else:
                    deal_or_warrant_prc_formatted = deal_or_warrant_prc
            else:
                deal_or_warrant_prc_formatted = deal_or_warrant_prc

            price_display = f"{deal_or_warrant_prc_formatted}"
            if selected_property_data.get('tradeTypeName') == '월세':
                price_display = f"{deal_or_warrant_prc_formatted}/{rent_prc}"

            area1 = selected_property_data.get('area1', '정보 없음')
            area2 = selected_property_data.get('area2', '정보 없음')
            area_display = f"{area1}/{area2}㎡" if area1 and area2 else f"{area2}㎡" if area2 else "면적 정보 없음"

            floor_info = selected_property_data.get('floorInfo', '정보 없음')

            tag_list = selected_property_data.get('tagList', [])
            tag_html = ' '.join([f"<span style='background-color: #ffffff; padding: 3px 6px; border-radius: 3px; font-size: 0.8em; margin-right: 5px;'>{tag}</span>" for tag in tag_list])


            img_url = selected_property_data.get('representativeImgUrl', '')

            # if img_url and not img_url.startswith('http'):
            #     img_url = f"https://your_image_server_url{img_url}" # 실제 이미지 서버 URL로 변경 필요
            # else:
            #     img_url = "https://placehold.co/300x200/cccccc/333333?text=매물+이미지"
            img_to_display = "https://placehold.co/300x200/cccccc/333333?text=매물+이미지"


            st.markdown(f"""
            <div style="
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 10px;
                box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
                background-color: #ffffff;
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <div>
                        <span style="background-color: #e6f7ff; color: #1890ff; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 0.8em;">
                            {'집주인' if selected_property_data.get('isDirectTrade', False) else '중개사'}
                        </span>
                        <span style="font-size: 1.2em; font-weight: bold; margin-left: 8px;">{selected_property_data.get('buildingName', selected_property_data.get('articleName', '건물명 미정'))}</span>
                    </div>
                    <div style="color: #ff4b4b; font-size: 1.5em;">★</div> <!-- Star icon -->
                </div>
                <div style="margin-bottom: 10px;">
                    <span style="font-size: 1.4em; font-weight: bold; color: #007bff;">
                        {selected_property_data.get('tradeTypeName', '거래 유형')} {price_display}
                    </span>
                </div>
                <div style="font-size: 0.9em; color: #f0f0f0;">
                    {selected_property_data.get('realEstateTypeName', '부동산 유형')} · {area_display}, {floor_info}층, {selected_property_data.get('direction', '방향 미정')}
                </div>
                <div style="font-size: 0.9em; color: #f0f0f0; margin-top: 5px;">
                    {selected_property_data.get('articleFeatureDesc', '상세 설명 없음')}
                </div>
                <div style="margin-top: 10px;">
                    {tag_html}
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px; font-size: 0.85em; color: #777;">
                    <span>확인매물 {selected_property_data.get('articleConfirmYmd', '날짜 미정')}.</span>
                    {f"<a href='{selected_property_data.get('cpPcArticleUrl', '#')}' target='_blank' style='text-decoration: none; color: #007bff;'>{selected_property_data.get('cpName', '링크')}에서 보기 ></a>" if selected_property_data.get('cpPcArticleUrl') else ""}
                </div>
                <div style="text-align: center; margin-top: 15px;">
                    <img src="{img_to_display}" alt="매물 이미지" style="width: 100%; height: auto; border-radius: 8px;">
                </div>
            </div>
            """, unsafe_allow_html=True)
