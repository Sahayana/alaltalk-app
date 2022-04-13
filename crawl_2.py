import json

import requests

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
    "query": "아이유",
}

response = requests.post("https://www.youtube.com/youtubei/v1/search", params=params, cookies=cookies, json=json_data)
json_res = json.loads(response.text)
results = json_res["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]

for row in results:
    if "videoRenderer" in row:
        youtube_data = []
        thumbnail = row["videoRenderer"]["thumbnail"]["thumbnails"][-1]["url"]
        title = row["videoRenderer"]["title"]["runs"][0]["text"]
        views = row["videoRenderer"]["viewCountText"]["simpleText"]
        youtube_base_url = "https://www.youtube.com/embed/"
        video_id = row["videoRenderer"]["videoId"]
        video_already = "False"
        youtube_data.append(title)
        youtube_data.append(views)
        youtube_data.append(youtube_base_url + video_id)
        youtube_data.append(video_already)
        print(youtube_data)
