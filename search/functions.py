import time
from typing import List
from bs4 import BeautifulSoup
from search.apps import SearchConfig


def crawling_youtube(search_word: str, content_count: int) -> List[List[str]]:
    start = time.time()
    # 검색 단어 분리
    search_word = search_word.replace(" ", "+")

    # 클로링을 담을 배열
    crawling_data = []

    driver = SearchConfig.driver

    # 유튜브 링크 들어 가기 ( 검색 결과한 결과 )
    url = "https://www.youtube.com/results?search_query=" + search_word
    driver.get(url)
    crawling_temp_data = []

    # 목표 량이 10개를 넘을 때까지 반복
    while len(crawling_temp_data) < content_count:
        print('hi')
        # 스크롤 내리기
        driver.execute_script('window.scrollTo(0, window.scrollY + 10000);')
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        # 검색 결과에 따른 비디오만 추출 ( 관련동영상 X )
        crawling_temp_data = soup.select("#contents > ytd-video-renderer")

    crawling_data =[]
    # 각 검색 결과에서 URL 얻기
    for data in crawling_temp_data:
        video_channels = data.select_one('#text-container a').text
        video_channels_link = data.select_one('#text-container a').attrs['href']
        video_views = data.select('span.ytd-video-meta-block')[0].text
        video_url = data.select('a')[0].attrs['href']
        video_title = data.select('a')[1].attrs['title']
        youtube_base_url = 'https://www.youtube.com'
        if '/shorts' in video_url:
            continue
        else:
            crawling_url = str(video_url).split('=')[1]
        crawling_url = youtube_base_url + '/embed/' + crawling_url
        crawling_data.append([crawling_url, video_url, video_title, video_views])

    print('function time is ', time.time()-start, 'seconds')
    return crawling_data[0:content_count]


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

def crawling_shopping():
    return 0