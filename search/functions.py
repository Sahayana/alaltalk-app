from typing import List
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver


def crawling_youtube(search_word: str,  crawling: int) -> List[str]:
    crawling_data = []

    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome(executable_path="D:/projects/alaltalk-app/search/chromedriver.exe", options=options)

    url = 'https://www.youtube.com/results?search_query=' + search_word
    print('url :', url)
    # driver.implicitly_wait(10)
    driver.get(url)
    # for k in range(10000):
    #     time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    crawling_temp_data = soup.select('#contents > ytd-video-renderer')
    crawling_temp_data_palay_list = soup.select('#contents')

    for i in crawling_temp_data_palay_list:
        print('########################')
        print(i)


    # for index, i in enumerate(crawling_temp_data):
    #     url_link_value_href = i.select_one('#thumbnail').attrs['href']
    #     youtube_base_url = 'https://www.youtube.com'
    #     print(youtube_base_url + url_link_value_href)
    #
    # for index, i in enumerate(crawling_temp_data_palay_list):
    #     url_link_value_href = i.select_one('#thumbnail').attrs['href']
    #     youtube_base_url = 'https://www.youtube.com'
    #     print(youtube_base_url + url_link_value_href)

    return crawling_data


print('function result : ', crawling_youtube('파이썬', 10))
