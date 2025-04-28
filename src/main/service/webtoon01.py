from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep




def run1():

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://naver.com")
    driver.maximize_window()
    sleep(0.5)
    print(driver.current_url)

    webtoonHomeLink = driver.find_element(
        by=By.CSS_SELECTOR,
        value='#shortcutArea > ul > li:nth-child(9) > a')
    webtoonHomeUrl = webtoonHomeLink.get_attribute("href")
    driver.get(webtoonHomeUrl)
    sleep(0.5)
    print(driver.current_url)

    webtoonLink = driver.find_element(
        by=By.CSS_SELECTOR,
        value='#menu > li:nth-child(2) > a'
    )
    webtoonLink.click()
    sleep(0.5)

    dayOfWeeks = driver.find_elements(
        by=By.CSS_SELECTOR,
        value='#wrap > header > div.SubNavigationBar__snb_wrap--A5gfM > nav > ul > li > a'
    )

    for dayOfWeek in dayOfWeeks[1:8]:
        dayOfWeek.click()
        sleep(1)

        webtoonDict = {
            "dayOfWeek": dayOfWeek.text,
            "webtoonItems" : []
        }

        webtoonList = []

        webtoonItems = driver.find_elements(
            by=By.CSS_SELECTOR,
            value='#content > div:nth-child(1) > ul > li'
        )

        for webtoonItem in webtoonItems:
            driver.execute_script("arguments[0].scrollIntoView(true)", webtoonItem)
            webtoonItemImg = webtoonItem.find_element(
                by=By.CSS_SELECTOR,
                value="a > div > img"
            )
            webtoonItemImgSrc = webtoonItemImg.get_attribute("src")
            print(webtoonItemImgSrc)


            webtoonItemTitle = webtoonItem.find_element(
                by=By.CSS_SELECTOR,
                # value="div > a:nth-of-type(1) > span > span"  # 이렇게 작성해도 되지만 이미 요소를 특정했으므로 더 들어갈 필요가 없다
                value="div > a:nth-of-type(1) > span"
            )
            # webtoonItemTitleText = webtoonItemTitle.get_attribute("textContent")
            webtoonItemTitleText = webtoonItemTitle.text  # .get_attribute("textContent")과 같은 내용
            print(webtoonItemTitleText)



            # # 2개 구조가 다르면 좀 잘 보이게 했어야지;;;;;;; 설계 쓰레기같이 했네
            # try:
            #     # 구조 1: div > a
            #     webtoonItemAuthor = webtoonItem.find_element(
            #         by=By.CSS_SELECTOR,
            #         value="div.ContentList__info_area--bXx7h > a.ContentAuthor__author--CTAAP"
            #     )
            # except:
            #     try:
            #         # 구조 2: div > div > a
            #         webtoonItemAuthor = webtoonItem.find_element(
            #             by=By.CSS_SELECTOR,
            #             value="div.ContentList__info_area--bXx7h > div > a.ContentAuthor__author--CTAAP"
            #         )
            #     except:
            #         webtoonItemAuthor = None  # 못 찾은 경우

            webtoonItemAuthor = webtoonItem.find_element(
                by=By.CSS_SELECTOR,
                value="div .ContentAuthor__author--CTAAP"  # 위에 적은 try-except와 달리 div의 하위 요소(자식, 손자 등) 중
            )                                              # 해당 class를 가지는 요소의 text를 가져오도록 했다.

            # webtoonItemAuthorText = webtoonItemAuthor.get_attribute("textContent")
            webtoonItemAuthorText = webtoonItemAuthor.text
            print(webtoonItemAuthorText)


            webtoonItemRating = webtoonItem.find_element(
                by=By.CSS_SELECTOR,
                value="div > div.rating_area > span > span"
            )
            webtoonItemRatingText = webtoonItemRating.get_attribute("textContent")
            print(webtoonItemRatingText)


            webtoonItemDict = {
                "img": webtoonItemImgSrc,
                "title": webtoonItemTitleText,
                "author": webtoonItemAuthorText,
                "rating": webtoonItemRatingText
            }

            webtoonDict["webtoonItems"].append(webtoonItemDict)

        webtoonList.append(webtoonDict)
    print(webtoonList)
    for i in webtoonList:
        for j in i:
            print(j)

