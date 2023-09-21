import json
import time
from typing import List, Optional, Union

import requests
from bs4 import BeautifulSoup


def youtube_crawling(search_word: str, count: int) -> Union[List[List[str]], str]:
    try:
        start = time.time()
        cookies = {
            "__Secure-1PSID": "JAg5BJrA6EnVN1WpL0Sw0anBTMM0wrRUlpcowNXsb4LFzpOzqfaZlEbBctIecskJfJWv8g.",
        }

        params = {
            "key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8",
            "prettyPrint": "false",
        }

        json_data = {
            "context": {
                "client": {
                    "hl": "ko",
                    "gl": "KR",
                    "clientName": "WEB",
                    "clientVersion": "2.20220406.09.00",
                },
            },
            "query": search_word,
        }

        response = requests.post(
            "https://www.youtube.com/youtubei/v1/search",
            params=params,
            cookies=cookies,
            json=json_data,
            timeout=2,
        )
        json_res = json.loads(response.text)
        results = json_res["contents"]["twoColumnSearchResultsRenderer"][
            "primaryContents"
        ]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]

        answer = []
        for row in results:
            if "videoRenderer" in row:
                title = row["videoRenderer"]["title"]["runs"][0]["text"]
                views = row["videoRenderer"]["shortViewCountText"]["accessibility"][
                    "accessibilityData"
                ]["label"]
                youtube_base_url = "https://www.youtube.com/embed/"
                video_id = row["videoRenderer"]["videoId"]
                video_already = "False"
                answer.append(
                    [youtube_base_url + video_id, title, views, video_already]
                )
        print("youtube crawling function time is ", time.time() - start, "seconds")
        if len(answer) < count:
            count = len(answer)
        return answer[0:count]
    except TimeoutError:
        return "TimeOut"


def shopping_crawling(search_word: str, count: int) -> Union[List[List[str]], str]:
    try:
        start = time.time()
        params = {"component": "", "q": search_word, "channel": "user"}
        response = requests.post(
            "https://www.coupang.com/np/search", params=params, timeout=3
        )
        soup = BeautifulSoup(response.text, "html.parser")
        result = soup.select(".search-product")
        cnt = 0
        answer = []
        for row in result:
            title = row.select_one(".name").text.strip()
            price = row.select_one(".price-value").text.strip()
            base_url = "https://coupang.com"
            content_url = row.select_one("a").attrs["href"]
            thumbnail = row.select_one("img").attrs["src"]
            answer.append([thumbnail, title, price, base_url + content_url, False])
            cnt += 1

        print("Shopping crawling function time is ", time.time() - start, "seconds")
        return answer[0:count]

    except TimeoutError:
        return "TimeOut"
