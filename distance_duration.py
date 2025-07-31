from selenium import webdriver
from bs4 import BeautifulSoup

def get_distance_duration(transportation, origin, destination):

    o_name, o_x, o_y = origin
    d_name, d_x, d_y = destination

    url = f"https://map.kakao.com/link/by/{transportation}/{o_name},{o_x},{o_y}/{d_name},{d_x},{d_y}"
    driver = webdriver.Chrome()  # 드라이버 경로
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')

    if transportation == 'traffic':
        li_tag = soup.select_one("ul li.TransitRouteItem")
        div_tag = li_tag.select_one("div.title")
        # 시간
        duration = div_tag.select_one("span.time span.num").text.strip()
        time_unit = div_tag.select_one("span.time span.minitueTxt").text.strip()
        duration = f"{duration+time_unit}"
        # 거리
        span_tags = div_tag.select("span.walkTime span.num")
        distance = span_tags[-1].text.strip()
    elif transportation in ['car', 'walk', 'bicycle']:
        p_tag = soup.select("p.header")
        # 거리
        span_tag = p_tag[0].select_one("span.distance")
        distance = span_tag.text.strip()
        # 시간
        span_tag2 = p_tag[0].select_one("span.time")
        duration = span_tag2.text.strip()
    else:
        driver.quit()
        exit()

    driver.quit()  
    # driver.close()

    return distance, duration

origin = ('송파파크하비오푸르지오',37.481453,127.123735)
destination = ('카카오판교아지트',37.3952969470752,127.110449292622)

transport = ['car', 'walk', 'traffic', 'bicycle']
selected_transportation = transport[0]

distance, duration = get_distance_duration(selected_transportation, origin, destination)
print(f'거리: {distance} / 걸리는 시간: {duration}')