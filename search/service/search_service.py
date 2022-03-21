from typing import List
import csv
import urllib.request
from urllib import parse
from bs4 import BeautifulSoup
import ssl


def crawling_news(search: str) -> List[List[str]]:
    context = ssl._create_unverified_context()

    # search = input("검색어를 입력하세요:")
    url = 'https://search.naver.com/search.naver?where=news&query='
    newUrl = url+parse.quote(search)

    html = urllib.request.urlopen(newUrl, context=context).read()
    soup = BeautifulSoup(html, 'html.parser')
    test_list = soup.select('#main_pack > section > div > div.group_news > ul > li > div > div > a')
    test_list2 = soup.select('#main_pack > section > div > div.group_news > ul > li > div > div > div.news_dsc > div > a')
    test_list3 = soup.select('#main_pack > section > div > div.group_news > ul > li > div > div > div.news_info > div.info_group > a.info.press')
    test_list4 = soup.select('#main_pack > section > div > div.group_news > ul > li > div > div > div.news_info > div.info_group > span')
    test_list5 = soup.select('#main_pack > section > div > div.group_news > ul > li > div > a > img')

    answer = []

    for i in range(len(test_list)):
        test_title = []
        test_title.append(test_list3[i].get_text())
        test_title.append(test_list4[i].get_text())
        test_title.append(test_list[i]['title'])
        test_title.append(test_list[i]['href'])
        test_title.append(test_list2[i].get_text())
        test_title.append(test_list5[i]['src'])
        answer.append(test_title)

    return answer

    # title = soup.findall(class='news_tit')
    # test_list = soup.select('#main_pack > section > div > div.group_news > ul>li ')
    # test_list = soup.select('#sp_nws1 > div > div > div.news_info')

    # print(test_list)

    # for i in title:
    #     print(i.attrs['title'])
    #     print(i.attrs['href'])
    #     print('\n')
