import streamlit as st

def init_sidebar(df):
    st.sidebar.title("🔍 필터링 검색")

    cities = df['시'].unique()
    selected_city = st.sidebar.selectbox("시", cities)

    districts = df[df['시'] == selected_city]['구'].unique()
    selected_district = st.sidebar.selectbox("구", districts)

    towns = df[(df['시'] == selected_city) & (df['구'] == selected_district)]['동'].unique()
    selected_town = st.sidebar.selectbox("동", towns)

    selected_location = f"{selected_city} {selected_district} {selected_town}"


    # 필터 옵션
    with st.sidebar:
        st.header("📊 페이지 선택")
        option = st.selectbox("페이지 선택", ["홈", "집값 예측"])

    return option
    