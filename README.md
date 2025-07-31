
최대현, 전예진, 이유진 - 데이터 전처리, 수집
crawling.py: 웹 크롤링을 위한 코드로
import srawling.py
crawling.crawling(법정동, 최대보증금, 최소보증금, 최대 월세, 최소 월세) 형식으로 인자를 넘겨 받으면 해당 동 원룸 매물 정보를 data/land_data.json 파일로 저장합니다.

인스톨 필요 모듈: streamlit-modal, 


최대현, 전예진, 이유진 - 데이터 전처리, 수집

crawling.py: 웹 크롤링을 위한 코드
호출 예시)
```
from scraping.crawling import crawling

crawling('서울특별시 종로구 낙원동', 5000000, 0, 300000, 0)

서울특별시 종로구 낙원동의 최대보증금 5,000,000 최소보증금 0 최대월세 300,000 최소월세 0인 원룸 매물 정보를 data/land_data.json 파일로 저장합니다.
법정동: '서울특별시 종로구 낙원동', '서울특별시 강남구 역삼동', '서울특별시....
```


백두현, 남다겸 - 모델 및 웹개발
