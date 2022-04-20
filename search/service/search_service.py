import ssl
import time
import urllib.request
from typing import List
from urllib import parse
import requests

from bs4 import BeautifulSoup

# def crawling_news(search: str) -> List[List[str]]:
#     start = time.time()
#     # context = ssl._create_unverified_context()
#
#     # search = input("검색어를 입력하세요:")
#     url = "https://search.naver.com/search.naver?where=news&query="
#     newUrl = url + parse.quote(search)
#
#     html = urllib.request.urlopen(newUrl, timeout=2).read()
#     soup = BeautifulSoup(html, "html.parser")
#     name = soup.select("#main_pack > section > div > div.group_news > ul > li > div > div > a")
#     content = soup.select("#main_pack > section > div > div.group_news > ul > li > div > div > div.news_dsc > div > a")
#     news = soup.select("#main_pack > section > div > div.group_news > ul > li > div > div > div.news_info > div.info_group > a.info.press")
#     date = soup.select("#main_pack > section > div > div.group_news > ul > li > div > div > div.news_info > div.info_group > span")
#     image = soup.select("#main_pack > section > div > div.group_news > ul > li > div > a > img")
#     answer = []
#
#     for i in range(len(news)):
#         test_title = []
#         test_title.append(news[i].get_text())
#         test_title.append(date[i].get_text())
#         test_title.append(name[i]["title"])
#         test_title.append(name[i]["href"])
#         test_title.append(content[i].get_text())
#         test_title.append(image[i]["src"])
#         test_title.append("False")
#         answer.append(test_title)
#     print("news crawling function time is ", time.time() - start, "seconds")
#     return answer


def refactoring_crawling_news(search: str) -> List[List[str]]:
    start = time.time()

    url = "https://search.naver.com/search.naver"
    params = {
        "where": "news",
        "query": search,
    }
    response = requests.get(url, params=params, timeout=2)
    soup = BeautifulSoup(response.text, "html.parser")
    news = soup.select('.list_news > li')

    answer = []

    for row in news:

        title = row.select_one('a.news_tit').attrs['title']
        date = row.select_one('span.info').text
        company = row.select_one('a.press').text
        content = row.select_one('a.dsc_txt_wrap').text
        thumbnail = row.select_one(' a.dsc_thumb > img').attrs['src']
        link = row.select_one(' a.dsc_thumb').attrs['href']
        answer.append([company, date, title, link, content, thumbnail, False])

    print("news crawling function time is ", time.time() - start, "seconds")
    return answer


# def crawling_book(search: str) -> List[List[str]]:
#     start = time.time()
#     # context = ssl._create_unverified_context()
#
#     # search = input("검색어를 입력하세요:")
#     url = "https://search.kyobobook.co.kr/web/search?vPstrKeyWord="
#     newUrl = url + parse.quote(search)
#
#     html = urllib.request.urlopen(newUrl, timeout=2).read()
#     soup = BeautifulSoup(html, "html.parser")
#
#     title = soup.select("div.title > a > strong")
#     short_href = soup.select("div.title > a ")
#     price = soup.select("div.sell_price > strong")
#     link = soup.select("div.title > a")
#     image = soup.select("div.cover > a > img")
#     author = soup.select("td.detail > div.author > a:nth-child(1)")
#     company = soup.select("td.detail > div.author > a:last-of-type")
#     search_list = soup.select("#search_list tr")
#     answer = []
#
#     for i in range(len(author)):
#         test_title = []
#         test_title.append(title[i].get_text())
#         test_title.append(author[i].get_text())
#         test_title.append(company[i].get_text())
#         short = short_href[i].get_text().split(":")
#         if len(short) == 1:
#             short.append("")
#         test_title.append(short[-1])
#
#         test_title.append(price[i].get_text())
#         test_title.append(link[i]["href"])
#         test_title.append(image[i]["src"])
#         test_title.append("False")
#         answer.append(test_title)
#     print("book crawling function time is ", time.time() - start, "seconds")
#     return answer


def refactoring_crawling_book(search: str) -> List[List[str]]:
    start = time.time()

    url = "https://search.kyobobook.co.kr/web/search"
    params = {
        "vPstrKeyWord": search,
        "orderClick": 'LAG',
    }

    response = requests.get(url, params=params, timeout=1)

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.select('#search_list tr')

    answer = []
    for row in books:
        title = row.select_one('.title > a').text.split(':')[0]
        author = row.select_one('.author > a:nth-child(1)').text
        company = row.select('.author > a')[-1].text
        series = row.select_one('.series > a')
        if series is None:
            series = '없음'
        else:
            series = series.text

        price = row.select_one('.sell_price > strong').text
        link = row.select_one('.cover > a').attrs['href']
        thumbnail = row.select_one('.cover > a > img').attrs['src']
        answer.append([title, author, company, series, price, link, thumbnail, False])

    print("book crawling function time is ", time.time() - start, "seconds")
    return answer
