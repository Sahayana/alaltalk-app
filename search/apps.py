import os

from django.apps import AppConfig
from selenium import webdriver


class SearchConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"

    # 현재 폴더 + chromedriver 경로 붙이기
    webdriver_path = os.getcwd() + '\search\chromedriver.exe'

    print(webdriver_path)

    name = "search"

    # webdriver option 설정 - 창 안 보이기, 시크릿 모드
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument('--incognito')
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")
    # chrome webdriver 실행

    driver = webdriver.Chrome(executable_path=webdriver_path, options=options)

    # 쿠기 삭제
    driver.delete_all_cookies()
