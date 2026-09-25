from playwright.sync_api import sync_playwright, Playwright
from time import sleep
import json

specialText = ""
activityTypesLookup={
    1:"First video",
    2:"Special message"
}

text1 = '''What type of share to do:
1 - First video on FYP (WILL NOT mark all videos in dialog as seen)
2 - Special messege (WILL mark all videos in dialog as seen)
Write a number: '''
text2 = '''What is your special messege: '''
text3 = '''Amount of dialogs to mantain: '''

def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://tiktok.com",
              timeout=60000,)

    sleep(300)

    cookies = context.cookies()
    with open("./TikTokCookies.json", "w") as cookiesFile:
        cookiesFile.write(json.dumps(cookies))
    browser.close()


print(text1, end="")
activityType = int(input())

if activityType==2:
    print(text2, end="")
    specialText=input()

print(text3, end="")
friendsN = int(input())


settings = {
    "activityType":activityTypesLookup[activityType],
    "friendsN":friendsN,
    "specialText":specialText
}
with open("./config.json", "w") as config:
    config.write(json.dumps(settings))

with sync_playwright() as playwright:
    run(playwright)