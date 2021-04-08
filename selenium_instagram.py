
import os
import json
import glob
import time
import configparser
import urllib.parse
from urllib.request import Request, urlopen
import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver

pathlink = "./InstagramHashtagSentimentAnalysisProject/data/csv/"

def checkCsv(search):
    if os.path.exists(pathlink + search + ".csv"):
        os.remove(pathlink + search + ".csv")

def saveCsv(data, search):
    config = configparser.ConfigParser()
    # CSV파일 생성
    if len(glob.glob(pathlink + search + ".csv")) == 1:
        cnt = len(pd.read_csv(pathlink + search + ".csv", index_col=0).index)
        time_pd = pd.DataFrame(data, index=[cnt])
        time_pd.to_csv(pathlink + search + ".csv", mode='a', encoding='utf-8-sig')
    else:
        cnt = 0
        time_pd = pd.DataFrame(data, index=[cnt])
        time_pd.to_csv(pathlink + search + ".csv", mode='a', encoding='utf-8-sig')

def driverOption():
    option = webdriver.ChromeOptions()

    option.add_argument("disable-gpu")  # 가속 사용안한다
    option.add_argument("lang=ko_KR")  # 가짜 플러그인 탑재
    option.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')  # user-agent 이름 설정

def driverStart():
    driver = webdriver.Chrome('chromedriver.exe')
    # 웹페이지 안보이게 하기
    # driver = webdriver.PhantomJS('phantomjs.exe')

    return driver

def driverEnd(driver):
    driver.quit()

def instagramLogin(driver):
    with open("instagramId.json",'r', encoding="utf8") as f:
        data = json.loads(f.read())  # string 타입
    driver.implicitly_wait(3)

    username = data["INSTAGRAM_USERNAME"]
    password = data["INSTAGRAM_PASSWORD"]

    element_id = driver.find_element_by_name('username')
    element_id.send_keys(username)
    element_password = driver.find_element_by_name('password')
    element_password.send_keys(password)

    driver.implicitly_wait(1)

    driver.find_element_by_css_selector('.sqdOP.L3NKy.y3zKF').click()

    driver.implicitly_wait(3)

    driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/div/button').click()


def searchInstagram(driver, instagramId):
    # @ 제거
    if instagramId[0] == "@":
        instagramId = instagramId[1:]
    url = 'https://www.instagram.com/' + str(instagramId) + '/'

    driver.get(url)
    driver.implicitly_wait(1.5)

def scrollInstagram(driver, instagramId):
    SCROLL_PAUSE_TIME = 1.0  # 인스타게시물 스크롤 속도 조절 ( 1.0 ~ 2.0까지 사양에 맞게 조절 )
    reallink = []

    flag = True;

    if driver.current_url == "https://www.instagram.com/accounts/login/":
        instagramLogin(driver)
        searchInstagram(driver, instagramId)

    while True:  # 반복문 시작
        pageString = driver.page_source
        bs = BeautifulSoup(pageString, "lxml")

        # 게시물 정보
        for link1 in bs.find_all(name="div", attrs={"class": "Nnq7C weEfm"}):
            for i in range(0, 3):
                try:
                    title = link1.select('a')[i]
                    real = title.attrs['href']
                    reallink.append(real)
                except:
                    print("탈출")
                    pass


        # 페이지 스크롤
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        new_height = driver.execute_script("return document.body.scrollHeight")

        # ++ 게시물 더보기 버튼 클릭
        # 한번 클릭하면 다시 안눌러도 된다
        i = 1
        while flag:
            driver.implicitly_wait(1)
            i_str = str(i)
            xpath = "/html/body/div[1]/section/main/div/div[" + i_str + "]/div[1]/div/button"
            i = i+1
            try:
                driver.find_element_by_xpath(xpath).click()
                print("클릭하자" + i_str)
                flag = False
            except:
                if i == 5:
                    flag = False
                print("더보기버튼 없음" + i_str)

        if new_height == last_height:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                return reallink
                break

            else:
                last_height = new_height
                continue

def getHashtags(driver, reallink, id):
    hashtags2 = []

    reallinknum = len(reallink)
    print("총" + str(reallinknum) + "개의 데이터.")
    try:  # 반복문 시작 ( print 명령어로 원하는 문자열인지 하나씩 확인해보시길 바랍니다.
        for i in range(0, reallinknum):
            hashtags2.append([])
            req = 'https://www.instagram.com/p' + reallink[i]
            driver.get(req)

            if driver.current_url == "https://www.instagram.com/accounts/login/":
                instagramLogin(driver)
                driver.get(req)

            webpage = driver.page_source
            soup = BeautifulSoup(webpage, "html.parser")

            # soup1 = str(soup.find_all(attrs={'class': 'e1e1d'}))
            # user_id = soup1.split('href="/')[1].split('/">')[0]

            soup1 = str(soup.find_all(attrs={'class': 'Nm9Fw'}))
            subValue = 'span'

            if (soup1 == "[]"):  # 좋아요가 0개, 1개, n개 일경우 모두 소스가 다르다.
                likes = '0'
            elif (soup1.find(subValue) == -1):
                likes = soup1.split('좋아요 ')[1].split('개')[0]
            elif (soup1.find(subValue) != -1):
                likes = soup1.split('<span>')[1].split('</span>')[0]

            soup1 = str(soup.find_all(attrs={'class': 'xil3i'}))
            if (soup1 == "[]"):
                pass
            else:
                soup2 = soup1.split(',')
                soup2num = len(soup2)
                for j in range(0, soup2num):
                    hashtags = soup2[j].split('#')[1].split('</a>')[0]

                    insert_data = {"user_id": id,
                                   "좋아요": likes,
                                   "hashtags": hashtags}
                    saveCsv(insert_data, id)

    except:
        print("오류발생" + str(i + 1) + "개의 데이터를 저장합니다.")
        saveCsv(insert_data, id)
        # to_csv(insert_data, search)  # insert_data에 저장한 데이터를 pandas_csv.py로 보냅니다.

    print("저장성공")

def SeleniumInstagramCrawler(id):
    id = str(id)

    checkCsv(id) #같은이름으로 csv파일이 있으면 삭제

    driverOption() # 구글 크롬 드라이브 옵션설정
    driver = driverStart() # 구글 크롬 드라이브 셀레니움으로 시작

    searchInstagram(driver, id)
    reallink = scrollInstagram(driver, id) # 인스타 아이디에 있는 게시글 긁어오기

    getHashtags(driver, reallink, id) # 해시태그 csv 저장하기

    driverEnd(driver)

if __name__ == '__main__':
    id = input("Instagram ID : ")
    SeleniumInstagramCrawler(id)