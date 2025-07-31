# https://www.youtube.com/watch?v=CkI7YvZWlCM

#다중선형회귀(Multiple Linear Regression) 기본 예제 - 월세예측

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import pandas as pd


#1 데이터 불러오기 (월세와 면적, 침실 수, 지하철 역 거리 정보 등)

rent_Data = pd.read_csv(" 데이터 링크 ")


#2 데이터 훈련과 테스트 (train_test_split 함수 이용) 
# x: 방갯수, 몇평, 지하철역 거리 .... y: 가격

from sklearn.model_selection import train_test_split
x = rent_Data [['bedrooms', 'bathroom', 'size_sqft', 'min_to_subway', 'floor', 'building_age_yrs']]
y = rent_Data [['rent']]
print(y)
print(y.shape)
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, test_size=0.2)


#3 예측 모델 생성하기 

from sklearn.linear_model import LinearRegression
lr = LinearRegression()
lr.fit(x_train, y_train)


#4 예측해보기

i_Want = [[3, 1, 720, 17, 5]]
rent_Fee = lr.predict(i_Want)
print(rent_Fee)

y_predicted = lr.predict(x_test)


#5 연관관계 살펴보고 모델의 정확도 평가하기

plt.scatter(y_test, y_predicted, alpha=0.4)
plt.xlabel("Actural Rent")
plt.ylabel("Predicted Rent")
plt.title("Rent Prediction")
plt.show()

print(lr.coef_)


#1 주택의 면적 'size_sqft'  과 가격 'rent'

plt.scatter(rent_Data[['size_sqft']], rent_Data[['rent']], alpha=0.4)
plt.show()

#2 침실 수와 가격

plt.scatter(rent_Data[['bedrooms']], rent_Data[['rent']], alpha=0.4)
plt.show()


#3 정원의 유무와 가격

plt.scatter(rent_Data[['has_patio']], rent_Data[['rent']], alpha=0.4)
plt.show()


# 4 지하철 역까지 거리와 가격

plt.scatter(rent_Data[['min_to_subway']], rent_Data[['rent']], alpha=0.4)
plt.show()


# 5 주택이 얼마나 오래 전에 지어졌는지와 가격

plt.scatter(rent_Data[['building_age_yrs']], rent_Data[['rent']], alpha=0.4)
plt.show()

# 모델의 정확도 평가하기

print(lr.score(x_train, y_train))