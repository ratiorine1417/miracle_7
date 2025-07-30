import streamlit as st

def init_sidebar(df):
    st.sidebar.title("🔍 필터링 검색")

    local_option = st.sidebar.multiselect("지역 선택",  options=df['지역'].unique(), default=df['지역'].unique())

    # 필터 옵션
    with st.sidebar:
        st.header("📊 페이지 선택")
        option = st.selectbox("페이지 선택", ["홈", "집값 예측"])

    return option, local_option