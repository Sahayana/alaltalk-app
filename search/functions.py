import time
from typing import List

import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from search.apps import SearchConfig


def crawling_youtube(search_word: str, content_count: int) -> List[List[str]]:
    start = time.time()

    # 검색 단어 분리
    search_word = search_word.replace(" ", "+")

    # 현재 폴더 + chromedriver 경로 붙이기
    webdriver_path = os.getcwd() + '/search/chromedriver'

    # webdriver option 설정 - 창 안 보이기, 시크릿 모드
    options = webdriver.ChromeOptions()
    # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    options.add_argument("headless")
    options.add_argument("--incognito")

    driver = webdriver.Chrome(executable_path=webdriver_path, options=options)

    # 쿠기 삭제
    driver.delete_all_cookies()

    # 유튜브 링크 들어 가기 ( 검색 결과한 결과 )
    url = "https://www.youtube.com/results?search_query=" + search_word

    driver.get(url)
    driver.implicitly_wait(50)
    crawling_temp_data = []

    # 목표 량이 10개를 넘을 때까지 반복
    while len(crawling_temp_data) < content_count:
        # 스크롤 내리기
        driver.execute_script("window.scrollTo(0, window.scrollY + 10000);")
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # 검색 결과에 따른 비디오만 추출 ( 관련동영상 X )
        crawling_temp_data = soup.select("#contents > ytd-video-renderer")

    crawling_data = []
    # 각 검색 결과에서 URL 얻기
    for data in crawling_temp_data:
        video_channels = data.select_one("#text-container a").text
        video_channels_link = data.select_one("#text-container a").attrs["href"]
        video_views = data.select("span.ytd-video-meta-block")[0].text
        video_url = data.select("a")[0].attrs["href"]
        video_title = data.select("a")[1].attrs["title"]
        youtube_base_url = "https://www.youtube.com"
        video_already = 'False'
        if "/shorts" in video_url:
            continue
        else:
            crawling_url = str(video_url).split("=")[1]
        crawling_url = youtube_base_url + "/embed/" + crawling_url
        crawling_data.append([crawling_url, youtube_base_url + video_url, video_title, video_views, video_already])

    print("youtube crawling function time is ", time.time() - start, "seconds")
    return crawling_data[0:content_count]


def crawling_shopping_only_bs4(search_word: str, count: int) -> List[List[str]]:
    start = time.time()
    url = "https://www.coupang.com/np/search?component=&&channel=user" + "&q=" + search_word + "&page=1"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
    data = requests.get(url, headers=headers)

    soup = BeautifulSoup(data.text, "html.parser")

    answer = []
    product_list = soup.select("#productList > li")

    for row in product_list:
        shopping_product = []
        shopping_img_src = row.select_one("img").get("data-img-src")
        if shopping_img_src is None:
            shopping_img_src = row.select_one("img").attrs["src"]
        shopping_name = row.select_one(".name").text
        shopping_price = row.select_one(".price-value").text
        shopping_url = "https://www.coupang.com" + row.select_one("a").attrs["href"]

        # list 에 담기
        shopping_product.append(shopping_img_src)
        shopping_product.append(shopping_name)
        shopping_product.append(shopping_price)
        shopping_product.append(shopping_url)
        shopping_product.append('False')
        answer.append(shopping_product)
    print("shopping crawling function time is ", time.time() - start, "seconds")
    return answer[:count]
