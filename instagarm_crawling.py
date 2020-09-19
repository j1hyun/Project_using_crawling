#2018~2019년 인스타그램에서 #대저생태공원을 검색해 추출한 데이터 크롤링
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


# 키워드 검색
def insta_keyword(word):
    url = 'https://www.instagram.com/explore/tags/' + word
    return url

def keyword_crawling():
    driver.find_element_by_css_selector('div.v1Nh3.kIKUG._bz0w').click()  # 첫번째 게시물 클릭
    try:
        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[4]/div[2]/div/article/div[3]/div[1]/ul/div/li/div/div/div[2]'))) #게시글 뜰 때까지 기다림
    except:
        print('nont found')
        driver.find_element_by_class_name('_65Bje.coreSpriteRightPaginationArrow').click() #게시글이 뜨지 않으면 옆 피드로 이동
    print('크롤링시작')

    while True: #게시글 수만큼 반복

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "_9AhH0")))  # 게시글 뜰 때까지 기다림

            date = driver.find_element_by_css_selector("time._1o9PC.Nzb55")
            year_info = date.get_attribute('datetime')[:4]  # 년도만 추출
            year = int(year_info)
            month_info = date.get_attribute('datetime')[5:7]
            month = int(month_info)
            day = date.get_attribute('datetime')[:10]  # 게시 날짜 추출

            add = driver.find_element_by_css_selector("a.c-Yi7")
            address = add.get_attribute('href')  # 게시글주소

            if (year == 2018):

                txt = driver.find_element_by_css_selector('div.C4VMK > span').text
                time.sleep(1)
                text_list.append((day, txt, address))

            elif year < 2017: #최신순 정렬이므로 2018년 전으로 넘어가면 반복문 중지
                driver.find_element_by_css_selector(
                    'a._65Bje.coreSpriteRightPaginationArrow').click()  # 오른쪽으로 피드 한 칸 이동
                date = driver.find_element_by_css_selector("time._1o9PC.Nzb55")
                year_info = date.get_attribute('datetime')[:4]  # 년도만 추출
                year = int(year_info)
                if year < 2017:
                    WebDriverWait(driver, 60).until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR,
                         'a._65Bje.coreSpriteRightPaginationArrow')))  # 버튼 뜰 때까지 기다림
                    driver.find_element_by_css_selector(
                        'a._65Bje.coreSpriteRightPaginationArrow').click()  # 오른쪽으로 피드 한 칸 이동
                    date = driver.find_element_by_css_selector("time._1o9PC.Nzb55")
                    year_info = date.get_attribute('datetime')[:4]  # 년도만 추출
                    year = int(year_info)
                    if year < 2017:
                        WebDriverWait(driver, 60).until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR,
                             'a._65Bje.coreSpriteRightPaginationArrow')))  # 버튼 뜰 때까지 기다림
                        driver.find_element_by_css_selector(
                            'a._65Bje.coreSpriteRightPaginationArrow').click()  # 오른쪽으로 피드 한 칸 이동
                        date = driver.find_element_by_css_selector("time._1o9PC.Nzb55")
                        year_info = date.get_attribute('datetime')[:4]  # 년도만 추출
                        year = int(year_info)
                        if year < 2017:
                            WebDriverWait(driver, 60).until(EC.presence_of_element_located(
                                (By.CSS_SELECTOR,
                                 'a._65Bje.coreSpriteRightPaginationArrow')))  # 버튼 뜰 때까지 기다림
                            driver.find_element_by_css_selector(
                                'a._65Bje.coreSpriteRightPaginationArrow').click()  # 오른쪽으로 피드 한 칸 이동
                            date = driver.find_element_by_css_selector("time._1o9PC.Nzb55")
                            year_info = date.get_attribute('datetime')[:4]  # 년도만 추출
                            year = int(year_info)
                            if year < 2017:
                                print('2018년까지 끝')
                                break


                else:
                    pass


            WebDriverWait(driver, 60).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                 'a._65Bje.coreSpriteRightPaginationArrow')))  # 버튼 뜰 때까지 기다림
            driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow').click()  # 오른쪽으로 피드 한 칸 이동

        except:
            print("loading error!!")

            try:
                WebDriverWait(driver, 60).until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR,
                     'a._65Bje.coreSpriteRightPaginationArrow')))  # 버튼 뜰 때까지 기다림
                driver.find_element_by_css_selector('a._65Bje.coreSpriteRightPaginationArrow').click()  # 오른쪽으로 피드 한 칸 이동
            except:
                break

driver = webdriver.Chrome('C:/Users/USER/Downloads/chromedriver_win32/chromedriver.exe')

loginUrl = 'http://www.instgram.com/accounts/login/'

driver.implicitly_wait(2)
driver.get(loginUrl)  # 인스타 로그인 화면 접속

username = 'userid'
userpw = 'userpassword'

# 로그인
driver.find_element_by_name('username').send_keys(username)
driver.find_element_by_name('password').send_keys(userpw)
driver.implicitly_wait(5)

driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click()
driver.implicitly_wait(3)

driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
driver.implicitly_wait(3)

driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
driver.implicitly_wait(3)

text_list = []

key = '대저생태공원'

searchUrl = insta_keyword(key)
driver.get(searchUrl)
time.sleep(2)

keyword_crawling()

csvfile1 = pd.DataFrame(text_list, columns=['게시 날짜', '게시글', '링크'])
csvfile1.to_csv(key + '18_file.csv', mode='wt', encoding='utf-8-sig', header=True, index=True)  # csv 파일로 저장, key 크롤링 끝
