from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

from src.main.repository.webtoon_repository import WebtoonRepository    # 내가 정의한 class 임포트


def run2():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://naver.com")
    driver.maximize_window()
    sleep(0.5)

    webtoonHomeLink = driver.find_element(
        by=By.CSS_SELECTOR,
        value="#shortcutArea > ul > li:nth-child(9) > a")
    webtoonHomeUrl = webtoonHomeLink.get_attribute("href")
    driver.get(webtoonHomeUrl)
    sleep(0.5)
    print(driver.current_url)

    webtoonLink = driver.find_element(
        by=By.CSS_SELECTOR,
        value="#menu > li:nth-child(2) > a")
    webtoonLink.click()
    sleep(0.5)
    print(driver.current_url)

    dayOfWeeks = driver.find_elements(
        by=By.CSS_SELECTOR,
        value="#wrap > header > div.SubNavigationBar__snb_wrap--A5gfM > nav > ul > li > a")

    webtoonList = []

    for dayOfWeek in dayOfWeeks[1:8]:
        dayOfWeek.click()
        sleep(0.5)

        webtoonDict = {
            "dayOfWeek": dayOfWeek.text,
            "webtoonItems": []
        }

        webtoonItems = driver.find_elements(
            by=By.CSS_SELECTOR,
            value="#content > div:nth-child(1) > ul > li")

        for webtoonItem in webtoonItems[:4]:
            driver.execute_script("arguments[0].scrollIntoView(true)", webtoonItem)
            webtoonItemImg = webtoonItem.find_element(by=By.CSS_SELECTOR, value="a > div > img")
            webtoonItemImgSrc = webtoonItemImg.get_attribute("src")
            print(webtoonItemImgSrc)
            webtoonItemTitle = webtoonItem.find_element(
                by=By.CSS_SELECTOR,
                value="div > a:nth-of-type(1) > span")
            webtoonItemTitleText = webtoonItemTitle.text
            print(webtoonItemTitleText)
            webtoonItemAuthor = webtoonItem.find_element(
                by=By.CSS_SELECTOR,
                value="div .ContentAuthor__author--CTAAP")
            webtoonItemAuthorText = webtoonItemAuthor.text
            print(webtoonItemAuthorText)
            webtoonItemRating = webtoonItem.find_element(
                by=By.CSS_SELECTOR,
                value="div > div:nth-last-of-type(1) > span > span")
            webtoonItemRatingText = webtoonItemRating.text
            print(webtoonItemRatingText)

            webtoonItemDict = {
                "img": webtoonItemImgSrc,
                "title": webtoonItemTitleText,
                "author": webtoonItemAuthorText,
                "rating": webtoonItemRatingText
            }

            webtoonDict["webtoonItems"].append(webtoonItemDict)

            sleep(0.1)

        webtoonList.append(webtoonDict)
    print(webtoonList)
    print()             # 여기까지 4/27에 한 거

    insertSql = list(map(lambda webtoonDict: list(map(lambda item: f"(default, \'{webtoonDict['dayOfWeek']}\', \'{item['title']}\', \'{item['author']}\', \'{item['rating']}\', \'{item['img']}\')", webtoonDict["webtoonItems"])), webtoonList))  # webtoonList로부터 각각의 요소들을 가져 와서 item 안에 튜플로 담는다
                                                                        # webtoonDict 내에 있는 webtoonItems list로 item 문자열을 만들었다.
    print(insertSql)
    print()

    extendInsertSql = []

    for sql in insertSql:   # insertSql list 넣어서 반복하면
        extendInsertSql.extend(sql) # insertSql 의 구조 상 list 내에 list가 있으니까

    print(extendInsertSql)      # 86~96 라인 강사님 githun 참조 code1218

    sql = f"""
    insert into webtoon_tb
    values
        {','.join(extendInsertSql)}
    """

    print(sql)

    convertedWebtoonList =  list(map(lambda webtoon:
                                list(map(lambda item:
                                    (webtoon['dayOfWeek'], item['title'], item['author'], item['rating'], item['img']), webtoon['webtoonItems'])),
                                webtoonList))

    webtoons = []
    for webtoon in convertedWebtoonList:
        webtoons.extend(webtoon)

    WebtoonRepository.insertMany(webtoons)
    print("Crawling Done!")

