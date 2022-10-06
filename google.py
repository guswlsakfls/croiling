from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import urllib.request
import os

title = input("수집할 이미지 : ")
url = "https://www.google.co.kr/imghp?hl=ko&ogbl"

print("----------접속중----------")
# driver = webdriver.Chrome('./chromedriver')
# driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl")
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get(url)
elem = driver.find_element_by_name("q")
elem.send_keys(title)
elem.send_keys(Keys.RETURN)

print("----------스크롤 내리는 중----------")
SCROLL_PAUSE_TIME = 1

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        try:
            driver.find_element_by_css_selector(".mye4qd").click()
        except:
            break
    last_height = new_height

# outpath = "./{0}/".format(title)
outpath = "../../img/{0}/".format(title)

if not os.path.isdir(outpath):
    print("----------폴더 생성----------")
    os.mkdir(outpath)

print("----------이미지 다운로드 중----------")
images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
count = 1
for image in images:
    if count == 51:
        break
    try:
        image.click()
        time.sleep(2)
        imgUrl = driver.find_element_by_xpath('/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img').get_attribute("src")

        urllib.request.urlretrieve(imgUrl, outpath + str(count) + ".jpg")
        print(count)
        count += 1
    except:
        pass

driver.close()
print("----------이미지 다운로드 완료----------")