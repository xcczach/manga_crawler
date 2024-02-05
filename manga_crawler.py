import requests
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

URL_1KKK = "https://www.1kkk.com"

chrome_options = Options()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(options=chrome_options)

def quit():
    browser.quit()

def start():
    global browser
    browser = webdriver.Chrome(options=chrome_options)


def get_catelog_url_1kkk(manga_name):
    browser.get(URL_1KKK)
    wait = WebDriverWait(browser, 100)
    search_input = browser.find_element(By.ID, "txtKeywords")
    search_button = browser.find_element(By.ID, "btnSearch")
    original_search_url = search_button.get_attribute("href")
    search_input.send_keys(manga_name)
    wait.until(lambda driver: driver.find_element(By.ID, "btnSearch").get_attribute("href") != original_search_url)
    browser.get(browser.find_element(By.ID, "btnSearch").get_attribute("href"))
    try:
        title_link = browser.find_element(By.CLASS_NAME, "mt70").find_element(By.CLASS_NAME, "title").find_element(By.TAG_NAME, "a")
        manga_url = "/"+title_link.get_attribute("href").split("/")[-2]+"/"
    except NoSuchElementException:
        manga_url = None
    return manga_url

def get_catelog_1kkk(catelog_url):
    catelog_url = f"{URL_1KKK}{catelog_url}"
    catelog_response = requests.get(catelog_url)
    catelog_soup = bs4.BeautifulSoup(catelog_response.text, "html.parser")
    chapter_list = catelog_soup.find("ul", id="detail-list-select-1")
    chapter_lis = chapter_list.find_all("li")
    chapter_as = [chapter_li.find("a") for chapter_li in chapter_lis]
    chapter_content = [{"title": chapter_a.text.split("  ")[0], "url": chapter_a["href"]} for chapter_a in chapter_as]
    return chapter_content


def get_chapter_1kkk(chapter_url, img_prefix):
    def chapter_wait_img_strategy(driver):
        return driver.find_element(By.ID, "imgloading").get_attribute("style").find("display: none;") != -1

    def chapter_wait_all_imgs_strategy(driver):
        return driver.find_element(By.ID, "imgloading").get_attribute("style").find("display: none;") != -1
    
    chapter_url = f"{URL_1KKK}{chapter_url}"
    browser.set_window_size(9999, 999900)
    browser.get(chapter_url)
    chapter_wait = WebDriverWait(browser, 100)
    try:
        last_page_button = browser.find_element(By.XPATH,"//div[@id='chapterpager']/*[last()]")
    except NoSuchElementException:
        last_page_button = None
    if last_page_button:
        page_count = int(last_page_button.text)
        page_index = 1
        while page_index <= page_count:
            chapter_wait.until(chapter_wait_img_strategy)
            chapter_img = browser.find_element(By.ID, "cp_image")
            chapter_img.screenshot(f"{img_prefix}{page_index}.png")
            next_page_button = browser.find_element(By.XPATH,"//a[text()='下一页']")
            try:
                next_page_button.click()
            except ElementClickInterceptedException:
                # avoid ad
                ad_close_button = browser.find_element(By.CLASS_NAME, "lb-win-con").find_element(By.TAG_NAME, "a").find_element(By.TAG_NAME, "img")
                ad_close_button.click()
                if page_index == 1:
                    chapter_img.screenshot(f"{img_prefix}{page_index}.png")
                next_page_button.click()
            page_index += 1
    else:
        chapter_wait.until(chapter_wait_all_imgs_strategy)
        chapter_img_container = browser.find_element(By.ID, "barChapter")
        chapter_imgs = chapter_img_container.find_elements(By.TAG_NAME, "img")
        img_index = 1
        try:
            # avoid ad
            ad_close_button = browser.find_element(By.CLASS_NAME, "lb-win-con").find_element(By.TAG_NAME, "a").find_element(By.TAG_NAME, "img")
            ad_close_button.click()
        except NoSuchElementException:
            pass
        for chapter_img in chapter_imgs:
            if(chapter_img.rect["width"] == 0):
                continue
            chapter_img.screenshot(f"{img_prefix}{img_index}.png")
            img_index += 1