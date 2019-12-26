from selenium import webdriver
from scripts.settings import CHROMEDRIVER_ADDED_TO_PATH, PATH_TO_CHROMEDRIVER

browser = ''


def init():
    global browser
    if CHROMEDRIVER_ADDED_TO_PATH:
        browser = webdriver.Chrome()
    else:
        browser = webdriver.Chrome(PATH_TO_CHROMEDRIVER)
    browser.implicitly_wait(5)


def get_browser():
    global browser
    return browser


def close_browser():
    global browser
    browser.quit()
