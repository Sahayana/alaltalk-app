import os

from django.apps import AppConfig
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import shutil
import selenium


class SearchConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"

    # 현재 폴더 + chromedriver 경로 붙이기
    webdriver_path = os.getcwd() + '\search\chromedriver.exe'
    webdriver_path_for_mac = '/usr/local/bin/chromedriver'
    print(webdriver_path)
    name = "search"

    # webdriver option 설정 - 창 안 보이기, 시크릿 모드
    options = webdriver.ChromeOptions()
    # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    options.add_argument("headless")
    options.add_argument("--incognito")

    # try:
    driver = webdriver.Chrome(executable_path=webdriver_path_for_mac, options=options)
    # except Exception:
    #     driver = webdriver.Chrome(executable_path=webdriver_path, options=options)

    # 쿠기 삭제
    driver.delete_all_cookies()
