import streamlit as st
import data.database as DB
import sqlite3
import requests
from main import load_db_data

st.title("마이페이지")
st.subheader("❤️ 내가 찜한 매물")

# 현재 로그인된 사용자 이름 가져오기
query = "SELECT * FROM users WHERE state = ?"
user =  load_db_data(True, query)
username = user[1]

def load_liked_db(username):
    with DB.get_connection() as conn:
        cursor = conn.cursor()
        try:
            # DB의 bookmarks 테이블에서 username이 같은 행 가져오기
            query = "SELECT * FROM bookmarks WHERE username = ?"
            cursor.execute(query, (username,))
            bookmarks_data = cursor.fetchall()
        except sqlite3.OperationalError as e:
            print(f'오류: {e}')
            bookmarks_data = []
        return bookmarks_data
    
# DB에 저장된 매물 삭제
def remove_bookmark(id):
    with DB.get_connection() as conn:
        cursor = conn.cursor()
        try:
            # DB의 bookmarks 테이블에서 id가 id인 행 삭제
            query = "DELETE FROM bookmarks WHERE id = ?"
            cursor.execute(query, (id,))
            conn.commit()
        except sqlite3.OperationalError as e:
            print(f'오류: {e}')


bookmarks = load_liked_db(username)

if not bookmarks:
    # 인포 스타일의 박스
    html = f"""
    <div style="background-color: #e6f2ff; padding: 20px; border-left: 6px solid #2196F3;">
        <div style="font-size:16px; color: #003366; margin-bottom: 10px;">
        찜한 매물이 없습니다 😢</div>
    </div>"""

    st.markdown(html, unsafe_allow_html=True)
else:
    for book_mark in bookmarks:
        col1 = st.columns(1)[0]
        with col1: 
            st.markdown(
                f"""
                <div style="background-color: #f7f9fc; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.1); padding:20px;">
                <h2>🏠 {book_mark[1]}</h2>
                <p>🧭 채광 방향           <strong>{book_mark[2]}</strong></p>                                  
                <p>🏢 층수(복층 여부)     <strong>{book_mark[3]}</strong></p>
                <p>📐 매물의 면적         <strong>{book_mark[4]}</strong></p>
                <p>📍 매물까지의 거리      <strong>{book_mark[5]}</strong></p>                                     
                <p>⏱️ 매물까지 소요 시간   <strong>{book_mark[6]} 소요</strong></p>
                <p>📅 확인일자           <strong>{book_mark[7]}</strong></p>
                <p>🧑‍💼 공인중개사         <strong>{book_mark[8]}</strong></p>
                <a href="{book_mark[9]}" style="color:black; border:none; padding:10px 15px; border-radius:8px; margin-top:10px;">
                    📄 매물 상세페이지 보기
                </a>
                </div>""", unsafe_allow_html=True)
            st.markdown("")
        # 좋아요 취소 버튼을 누를 시 매물 북마크 해제
        if st.button('좋아요 취소', key=book_mark[10], icon="🗑️"):
            remove_bookmark(book_mark[10])
            st.success("북마크에서 삭제되었습니다!")
            # 페이지를 다시 로드하여 변경사항 반영
            st.rerun()
        st.markdown("---")

    # page_size = 3
    # page_num = st.session_state.get('page_num', 0)
    # start_idx = page_num * page_size
    # end_idx = start_idx + page_size

    # col1 = st.columns(1)
    # with col1[0]: 
    #     if end_idx < len(bookmarks) and st.button("더보기"):
    #         st.session_state.page_num = page_num + 1
