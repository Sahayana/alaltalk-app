from typing import List
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver


def crawling_youtube(search_word: str,  content_count: int) -> List[str]:
    crawling_data = []
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument('--incognito')
    options.add_argument('window-size=1280,720')
    driver = webdriver.Chrome(executable_path="D:/projects/alaltalk-app/search/chromedriver.exe", options=options)
    driver.delete_all_cookies()
    url = 'https://www.youtube.com/results?search_query=' + search_word
    print('url :', url)
    driver.get(url)
    crawling_temp_data =[]
    while len(crawling_temp_data) < content_count:

        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # 검색결과에 따른 비디오
        crawling_temp_data = soup.select('#contents > ytd-video-renderer')
        cnt = 0
        print('craling_temp_data length: ', len(crawling_temp_data))

    for data in crawling_temp_data:
        video_url = data.select('a')[0].attrs['href']
        youtube_base_url = 'https://www.youtube.com'
        crawling_url = youtube_base_url + video_url
        crawling_data.append(crawling_url)

    return crawling_data[0:11]


    # for index, i in enumerate(crawling_temp_data):
    #     cnt +=1
    #     print(i.select('a')[1].attrs['aria-label'])
    #     print(cnt, '번째 게시글 입니다아아아아')
    #     print('.............................')
    #     print('###################')




    # 최신 동영상, 관련 비디오
    # crawling_temp_data_latest_video = soup.select('#contents > ytd-shelf-renderer')
    # if crawling_temp_data_latest_video is not None:
    #     print('latest vidio!!')
    #     print('shelf length',  len(crawling_temp_data_latest_video))
    #     for k in crawling_temp_data_latest_video:
    #         print('############# shelf 구분선 #############')
    #         cnt = 0
    #         for j in k.select('ytd-video-renderer'):
    #
    #             print('############# render 구분선 #############')
    #             print(j.select('a')[1].attrs['aria-label'])
    #             cnt += 1
    #             print(cnt, '번째 비디오')
    #             print('#@$@#$@#$@#$@#$#@$@#$@')
    #
    # for i in range(1000):
    #     time.sleep(1)


    return 0

print('function result : ', crawling_youtube('디퓨저', 10))
