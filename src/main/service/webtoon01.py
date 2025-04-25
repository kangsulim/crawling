from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep




def run():

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://naver.com")
    # driver.maximize_window()
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
            value="div > a > span > span"
        )

        webtoonItemTitleText = webtoonItemTitle.get_attribute("textContent")

        print(webtoonItemTitleText, end="\t")



        # 2개 구조가 다르면 좀 잘 보이게 했어야지;;;;;;;
        try:
            # 구조 1: div > a
            webtoonItemWriter = webtoonItem.find_element(
                by=By.CSS_SELECTOR,
                value="div.ContentList__info_area--bXx7h > a.ContentAuthor__author--CTAAP"
            )
        except:
            try:
                # 구조 2: div > div > a
                webtoonItemWriter = webtoonItem.find_element(
                    by=By.CSS_SELECTOR,
                    value="div.ContentList__info_area--bXx7h > div > a.ContentAuthor__author--CTAAP"
                )
            except:
                webtoonItemWriter = None  # 못 찾은 경우

        webtoonItemWriterText = webtoonItemWriter.get_attribute("textContent")
        print(webtoonItemWriterText, end="\t")

        webtoonItemRating = webtoonItem.find_element(
            by=By.CSS_SELECTOR,
            value="div > div.rating_area > span > span"
        )

        webtoonItemRatingText = webtoonItemRating.get_attribute("textContent")
        print(webtoonItemRatingText)


#content > div:nth-child(1) > ul > li:nth-child(1) > div > div.rating_area > span > span