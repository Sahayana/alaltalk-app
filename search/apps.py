from django.apps import AppConfig
from selenium import webdriver
import os


class SearchConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"

    # 현재 폴더 + chromedriver 경로 붙이기
    webdriver_path = os.getcwd() + '\search\chromedriver.exe'
    print(webdriver_path)
    name = "search"
    # chrome webdriver 실행
    options = webdriver.ChromeOptions()

    # webdriver option 설정 - 창 안 보이기, 시크릿 모드
    options.add_argument("headless")
    options.add_argument('--incognito')

    driver = webdriver.Chrome(executable_path=webdriver_path, options=options)

    # 쿠기 삭제
    driver.delete_all_cookies()
