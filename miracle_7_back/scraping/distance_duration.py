from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# 전예진
def get_distance_duration(transportation, origin, destination):
    '''
    transportation: 이동수단(자동차, 도보, 대중교통, 자전거 중 택1)
    origin: 출발지(articleName, latitude, longitude) (ex)'송파파크하비오푸르지오', 37.481453, 127.123735
    destination: 목적지(articleName, latitude, longitude) (ex) ('카카오판교아지트',37.3952969470752,127.110449292622)
    '''

    o_name, o_x, o_y = origin
    d_name, d_x, d_y = destination

    # selenium 설정 (# + user-agent 제외 삭제 가능)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new") # GUI 없이 브라우저 실행
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('disable-infobars')
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled') # 탐지 방지
    chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"')
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "none"

    url = f"https://map.kakao.com/link/by/{transportation}/{o_name},{o_x},{o_y}/{d_name},{d_x},{d_y}"

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    try:
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        # 대중교통
        if transportation == 'traffic':
            div_tag = soup.select_one("ul li.TransitRouteItem div.title")
            if div_tag:
                # 시간
                duration = div_tag.select_one("span.time").text.strip()
                # 거리
                distance = div_tag.select_one("span.walkTime span.bar+span.num").text.strip()
        # 자동차, 도보, 자전거
        elif transportation in ['car', 'walk', 'bicycle']:
            p_tag = soup.select("p.header")
            if p_tag:
            # 거리
                span_tag = p_tag[0].select_one("span.distance")
                distance = span_tag.text.strip()
                # 시간
                span_tag2 = p_tag[0].select_one("span.time")
                duration = span_tag2.text.strip()
        print('거리/시간 추출 성공!') if distance&duration else print('거리/시간 추출 실패')
    except AttributeError as e:
        print(f'오류가 발생했습니다! Error: {e}')
    except UnboundLocalError as e:
        print(f'오류가 발생했습니다! Error: {e}')
    finally:
        driver.quit()
        # 거리와 시간 반환 (5~6초 정도 소요)
        return distance, duration