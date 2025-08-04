import streamlit as st
import streamlit_authenticator as stauth
import sqlite3
import pandas as pd
from ui.dashboard import show_homepage
from ui.sidebar.sidebar import init_sidebar
from scraping.crawling import crawling
import data.database as DB
# -------------- 초기 설정 --------------------
# URL 쿼리 매개변수에서 로그인 상태 확인
params = st.query_params
is_logged_in = params.get('logged_in', 'False') == 'True'
user = params.get('user', '')
# 세션 상태에 로그인 정보 저장
if is_logged_in:
    st.session_state.logged_in = True
    st.session_state.user = user
# -------------------------------------------

def convert_to_won(value_in_manwon):
    "사용자 입력값(만원)을 원 단위로 변환"
    try:
        return int(value_in_manwon) * 10000
    except ValueError:
        return None  # 숫자가 아닌 경우 처리
    
# 데이터베이스에서 사용자 정보 불러오기
def load_db_data(value, query):
    conn = DB.get_connection()
    cursor = conn.cursor()
    # DB에서 users 테이블에서 입력한 username이 같은 행 가져오기
    cursor.execute(query, (value,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data

# 데이터베이스에서 로그인 상태 정보 수정하기
def update_state(username, state):
    conn = DB.get_connection()
    cursor = conn.cursor()
    try:
        # users 테이블에 username, state 수정
        cursor.execute("UPDATE users SET state = ? WHERE username = ?", 
                       (state, username))
        conn.commit()
        print("DB에 상태 정보를 성공적으로 저장했습니다.")
    finally:
        conn.close()

# 사용자 정보(아이디, 비밀번호만) 데이터베이스에 저장하기(하드코딩)
def save_db_user_data():

    # ----------------------- #
    # DB에 저장 원하는 아이디와 비밀번호(변경)
    name = 'do'
    pw = 'miracle'
    # ----------------------- #

    conn = DB.get_connection()
    cursor = conn.cursor()
    
    # 테이블 생성(이미 존재 시 생략)
    cursor.execute(DB.create_user_table())
    # 비밀번호 해시 처리
    hashed_pw = stauth.Hasher().hash(pw)

    try:
        # users 테이블에 username, hashed_password 저장
        cursor.execute("INSERT INTO users (username, password, state) VALUES (?, ?, ?)", 
                       (name, hashed_pw, False))
        conn.commit()
        print("DB에 정보를 성공적으로 저장했습니다.")
    except sqlite3.IntegrityError:
        print("이미 DB에 존재하는 사용자 이름입니다.")
    finally:
        conn.close()

def show_login_page():
    st.image("./image/miracle_7_logo.png", width=500)
    st.title("💫 7번 방에서 행운을 찾으세요 💫")

    username = st.text_input("아이디")
    password = st.text_input("비밀번호", "", type="password")

    # 입력한 아이디, 비밀번호와 DB에 저장된 아이디, 비밀번호 비교 후 로그인
    if st.button("로그인"):
        query = "SELECT * FROM users WHERE username = ?"
        user = load_db_data(username, query)
        if user:
            db_password = user[2]
            password_match = stauth.Hasher().check_pw(password, db_password)
            if password_match:
                st.success(f"로그인되었습니다, {username} 님. 환영합니다!")
                # 로그인 성공 시 URL에 로그인 상태 저장
                st.query_params['logged_in'] = True
                st.query_params['user'] = username
                update_state(username, True)
                st.rerun()
            else:
                st.error("비밀번호가 올바르지 않습니다.")
        else:
            st.error("등록된 사용자가 없습니다. 회원가입을 먼저 진행해 주세요!")

def show_main_page():
    st.set_page_config(
        page_title="7번방의 기적",
        page_icon="image/miracle_7_logo.png",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    #사용자 입력값 사이드바로부터 받기
    selected_location, deposit_range, rent_range, coords = init_sidebar()

    # 필터링 적용
    filtered_df = crawling(selected_location, rent_range[1], rent_range[0], deposit_range[1], deposit_range[0])

    st.title("🏡 7번 방의 기적")

    # 지역 이름 길이에 따라 너비 가중치 계산
    location_length = len(selected_location) 
    if location_length == 0:
        location_length = 1
    col_ratio = min(location_length / 5, 2)  # 최대 비율 제한

    col1, col2, col3 = st.columns([col_ratio, 1, 1])

    col1.metric("📍 지역", selected_location, selected_location)
    col2.metric("💰 보증금", f"{deposit_range[0]}~{deposit_range[1]}")
    col3.metric("💸 월세", f"{rent_range[0]}~{rent_range[1]}")
    
    username = st.session_state.get('user', '')

    # 메인화면 불러오기
    if filtered_df:
        show_homepage(filtered_df, selected_location, coords[0], coords[1], username)
    else:
        st.markdown(f"""
            <div style="
                background-color: #ffe6e6;
                padding: 15px;
                border-radius: 10px;
                border-left: 6px solid #ff4d4d;
                font-size: 16px;
                color: #990000;
            ">
                <strong> 검색되지 않습니다. 다시 시도해주세요. <br>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("")
    if st.button("로그아웃"):
        update_state(username, False)
        # 로그아웃 시, URL에서 로그인 상태 제거
        del st.query_params['logged_in']
        st.session_state.clear()
        st.rerun()

# 로그인 상태에 따라 다른 페이지 표시
if st.session_state.get('logged_in', False):
    # username = params.get('user', '')
    show_main_page()
else:
    show_login_page()

# 아이디, 비밀번호 DB에 추가
save_db_user_data()