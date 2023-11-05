import ssl
import time
import urllib.request
from typing import List
from urllib import parse

import requests
from bs4 import BeautifulSoup


def refactoring_crawling_news(search: str) -> List[List[str]]:
    start = time.time()

    url = "https://search.naver.com/search.naver"
    params = {
        "where": "news",
        "query": search,
    }
    response = requests.get(url, params=params, timeout=2)
    soup = BeautifulSoup(response.text, "html.parser")
    news = soup.select(".list_news > li")

    answer = []

    for row in news:

        title = row.select_one("a.news_tit").attrs["title"]
        date = row.select_one("span.info").text
        company = row.select_one("a.press").text
        content = row.select_one("a.dsc_txt_wrap").text
        thumbnail = row.select_one(" a.dsc_thumb > img").attrs["src"]
        link = row.select_one(" a.dsc_thumb").attrs["href"]
        answer.append([company, date, title, link, content, thumbnail, False])

    print("news crawling function time is ", time.time() - start, "seconds")
    return answer


def refactoring_crawling_book(search: str) -> List[List[str]]:
    start = time.time()

    url = "https://search.kyobobook.co.kr/web/search"
    params = {
        "vPstrKeyWord": search,
        "orderClick": "LAG",
    }

    response = requests.get(url, params=params, timeout=1)

    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.select("#search_list tr")

    answer = []
    for row in books:
        title = row.select_one(".title > a").text.split(":")[0]
        author = row.select_one(".author > a:nth-child(1)").text
        company = row.select(".author > a")[-1].text
        series = row.select_one(".series > a")
        if series is None:
            series = "없음"
        else:
            series = series.text

        price = row.select_one(".sell_price > strong").text
        link = row.select_one(".cover > a").attrs["href"]
        thumbnail = row.select_one(".cover > a > img").attrs["src"]
        answer.append([title, author, company, series, price, link, thumbnail, False])

    print("book crawling function time is ", time.time() - start, "seconds")
    return answer
