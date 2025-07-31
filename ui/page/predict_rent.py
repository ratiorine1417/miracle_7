#predict_rent

# predict_rent.py

import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# 제목
st.title("🏠 월세 예측 페이지")

# CSV 데이터 업로드
st.markdown("### 예측에 사용할 데이터를 업로드하세요 (CSV)")
uploaded_file = st.file_uploader("CSV 파일을 선택해주세요", type=["csv"])

if uploaded_file is not None:
    rent_Data = pd.read_csv(uploaded_file)

    # 입력 변수(x), 목표 변수(y) 설정
    x = rent_Data[['bedrooms', 'bathroom', 'size_sqft', 'min_to_subway', 'floor', 'building_age_yrs']]
    y = rent_Data[['rent']]

    # 데이터 분리
    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8)

    # 모델 훈련
    lr = LinearRegression()
    lr.fit(x_train, y_train)

    # 사용자 입력 폼
    st.markdown("### 예측할 정보를 입력하세요")
    bedrooms = st.number_input("침실 수", min_value=0, value=1)
    bathroom = st.number_input("욕실 수", min_value=0, value=1)
    size_sqft = st.number_input("면적 (sqft)", min_value=0, value=500)
    min_to_subway = st.number_input("지하철역까지 거리 (분)", min_value=0, value=10)
    floor = st.number_input("층수", min_value=0, value=2)
    building_age_yrs = st.number_input("건물 연식 (년)", min_value=0, value=10)

    if st.button("📊 월세 예측하기"):
        user_input = [[bedrooms, bathroom, size_sqft, min_to_subway, floor, building_age_yrs]]
        rent_prediction = lr.predict(user_input)
        st.success(f"예측된 월세는 약 **{int(rent_prediction[0][0]):,}원**입니다")

        # 시각화
        y_predicted = lr.predict(x_test)
        fig, ax = plt.subplots()
        ax.scatter(y_test, y_predicted, alpha=0.5)
        ax.set_xlabel("실제 월세")
        ax.set_ylabel("예측 월세")
        ax.set_title("실제 vs 예측 월세")
        st.pyplot(fig)

        # 모델 정확도
        st.markdown(f"#### 모델의 정확도: **{lr.score(x_test, y_test)*100:.2f}%**")

else:
    st.warning("먼저 CSV 파일을 업로드해주세요.")
