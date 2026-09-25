from playwright.sync_api import sync_playwright, Playwright
from time import sleep
import random
import json


SHARE_BTN = (1035, 600)
SHARE_CONFIRM = (820, 500)
SHARE_CHAT = lambda n : (550+(90*n), 300)
MESSAGES_BTN = (100, 400)
MESSAGES_CHAT = lambda n : (115, 100+(n*75))


def sleepAround(time, range=0.25):
    sleep(time + range*random.random())

def run(playwright: Playwright, config):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    context = browser.new_context()

    with open("./TikTokCookies.json", "r") as cookiesFile:
        cookies = json.loads(cookiesFile.read())
        context.add_cookies(cookies)

    
    page = context.new_page()
    page.goto("http://tiktok.com",
              timeout=60000,)

    #sleep(300)
    activityType = config["activityType"]
    n = config["friendsN"]
    specialText = config["specialText"]
    sleepAround(3)
    match activityType:
        case "First video":
            ShareFirst(page, n)
        case "Special message":
            WriteToEveryone(page, n, specialText)
        case _:
            raise Exception("Config have invalid type of activity. Please run setup.py again")
    browser.close()


def WriteToEveryone(page, n, text):
    page.mouse.click(*MESSAGES_BTN)
    sleepAround(1)
    for chatNum in range(n):
        page.mouse.click(*MESSAGES_CHAT(n-1))
        sleepAround(0.25, 0.2)
        page.keyboard.type(text)
        page.keyboard.press("Enter")
        sleepAround(1)



def ShareFirst(page:Page, n:int):
    page.mouse.click(*SHARE_BTN)
    sleepAround(1)
    for chatNum in range(n):
        page.mouse.click(*SHARE_CHAT(chatNum))
        sleepAround(0.25, 0.2)
    page.mouse.click(*SHARE_CONFIRM)
    sleep(2)


config = None
with open ("./config.json", "r") as configFile:
    config = json.loads(configFile.read())

with sync_playwright() as playwright:
    run(playwright, config)