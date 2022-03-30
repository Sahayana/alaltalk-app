import ssl
import urllib.request
from typing import List
from urllib import parse

from bs4 import BeautifulSoup


def crawling_news(search: str) -> List[List[str]]:
    context = ssl._create_unverified_context()

    # search = input("검색어를 입력하세요:")
    url = "https://search.naver.com/search.naver?where=news&query="
    newUrl = url + parse.quote(search)

    html = urllib.request.urlopen(newUrl, context=context).read()
    soup = BeautifulSoup(html, "html.parser")
    name = soup.select("#main_pack > section > div > div.group_news > ul > li > div > div > a")
    content = soup.select("#main_pack > section > div > div.group_news > ul > li > div > div > div.news_dsc > div > a")
    news = soup.select("#main_pack > section > div > div.group_news > ul > li > div > div > div.news_info > div.info_group > a.info.press")
    date = soup.select("#main_pack > section > div > div.group_news > ul > li > div > div > div.news_info > div.info_group > span")
    image = soup.select("#main_pack > section > div > div.group_news > ul > li > div > a > img")
    answer = []

    for i in range(len(news)):
        test_title = []
        test_title.append(news[i].get_text())
        test_title.append(date[i].get_text())
        test_title.append(name[i]["title"])
        test_title.append(name[i]["href"])
        test_title.append(content[i].get_text())
        test_title.append(image[i]["src"])
        answer.append(test_title)

    return answer


def crawling_book(search: str) -> List[List[str]]:

    context = ssl._create_unverified_context()

    # search = input("검색어를 입력하세요:")
    url = "https://search.kyobobook.co.kr/web/search?vPstrKeyWord="
    newUrl = url + parse.quote(search)

    html = urllib.request.urlopen(newUrl, context=context).read()
    soup = BeautifulSoup(html, "html.parser")

    title = soup.select("div.title > a > strong")
    short_href = soup.select("div.title > a ")
    price = soup.select("div.sell_price > strong")
    link = soup.select("div.title > a")
    image = soup.select("div.cover > a > img")
    author = soup.select("td.detail > div.author > a:nth-child(1)")
    company = soup.select("td.detail > div.author > a:last-of-type")
    search_list = soup.select("#search_list tr")
    answer = []

    # for row in search_list:
    #     print('#####################')
    #     print(row)
    #     print(row.select_one('detail'))

    for i in range(len(author)):
        test_title = []
        test_title.append(title[i].get_text())
        test_title.append(author[i].get_text())
        test_title.append(company[i].get_text())
        short = short_href[i].get_text().split(":")
        if len(short) == 1:
            short.append("")
        test_title.append(short[-1])

        test_title.append(price[i].get_text())
        test_title.append(link[i]["href"])
        test_title.append(image[i]["src"])
        answer.append(test_title)
    return answer
