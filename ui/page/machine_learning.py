#machinelearning.py

# https://www.youtube.com/watch?v=CkI7YvZWlCM

#다중선형회귀(Multiple Linear Regression) 기본 예제 - 월세예측

# machinelearning.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pickle

# JSON 데이터 불러오기
rent_Data = pd.read_json("data/land_data.json")

# 전처리
rent_Data['floor'] = rent_Data['floorInfo'].str.extract(r'(\d+)').astype(float)
direction_map = {d: i for i, d in enumerate(rent_Data['direction'].dropna().unique())}
rent_Data['direction_code'] = rent_Data['direction'].map(direction_map)
rent_Data['rent'] = rent_Data['rentPrc'].astype(float)

# 유효한 데이터만 사용
rent_Data = rent_Data.dropna(subset=['floor', 'direction_code', 'rent'])

# x, y 분리
x = rent_Data[['floor', 'direction_code']]
y = rent_Data[['rent']]

# 학습/테스트 분할
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8)

# 모델 학습
lr = LinearRegression()
lr.fit(x_train, y_train)

# 정확도 확인
print("모델 정확도:", lr.score(x_test, y_test))

# 모델 저장
with open("models/rent_model.pkl", "wb") as f:
    pickle.dump((lr, direction_map), f)

# 시각화
y_predicted = lr.predict(x_test)
plt.scatter(y_test, y_predicted, alpha=0.5)
plt.xlabel("실제 월세")
plt.ylabel("예측 월세")
plt.title("실제 vs 예측")
plt.show()
