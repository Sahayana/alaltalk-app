from django.apps import AppConfig
from selenium import webdriver


class SearchConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "search"
    # chrome webdriver 실행
    options = webdriver.ChromeOptions()

    # webdriver option 설정 - 창 안 보이기, 시크릿 모드
    options.add_argument("headless")
    options.add_argument('--incognito')
    webdriver = driver = webdriver.Chrome(executable_path="search/chromedriver.exe",options=options)

    # 쿠기 삭제
    driver.delete_all_cookies()
