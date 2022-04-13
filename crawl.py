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
    "query": "코딩",
}

response = requests.post("https://www.youtube.com/youtubei/v1/search", params=params, cookies=cookies, json=json_data)
print(response.text)
