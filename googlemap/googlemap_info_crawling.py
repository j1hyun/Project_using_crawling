from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver import ActionChains

driver = webdriver.Chrome('C:/Users/USER/Downloads/chromedriver_win32/chromedriver.exe')

url = 'https://www.google.com/maps/place/%EC%82%BC%EB%9D%BD%EC%83%9D%ED%83%9C%EA%B3%B5%EC%9B%90/@35.1686363,128.9745201,19z/data=!4m8!1m2!2m1!1z7IK865297IOd7YOc6rO17JuQ!3m4!1s0x3568c1cf64bb0055:0x550b45d4a67c2c54!8m2!3d35.1687484!4d128.9735403'

driver.get(url)
driver.implicitly_wait(5)

result_list = []
timelist = []
list_a = []
info_list = []

for n in range(24):
    a = driver.find_elements_by_class_name('section-popular-times-bar')
    conv = a[n].get_attribute('aria-label')
    time = conv[:6].split('에')[0]
    timelist.append(time)

info = driver.find_elements_by_class_name('section-popular-times-bar')
for i in range(len(info)):
    conv = info[i].get_attribute('aria-label')
    print(conv)
    if(len(conv)>20):
        convinfo=conv[-5:-1].split(' ')[1]
    else:
     convinfo=conv[-5:].split(' ')[1]
    info_list.append(convinfo)

list_a = timelist + info_list

n = 24
result = [list_a[i * n:(i + 1) * n] for i in range((len(list_a) + n - 1) // n)]  # 리스트 쪼개기
print(info_list)

for i in range(24):
    result_list.append((
                       result[0][i], result[1][i], result[2][i], result[3][i], result[4][i], result[5][i], result[6][i],
                       result[7][i]))

csvfile = pd.DataFrame(result_list, columns=['시간','일요일', '월요일', '화요일', '수요일', '목요일', '금요일', '토요일'])

csvfile.index += 1
csvfile.to_csv('googlemap_samrak_info.csv', mode='wt', encoding='utf-8-sig', header=True, index=False)

print(driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[29]/div/div[2]/button').text)
'''
star = driver.find_elements_by_class_name('jqnFjrOWMVU__histogram')
star_list = []

for i in range(len(star)):
    star_info=star[i].get_attribute('aria-label').split(',')
    star_rank=star_info[0]
    star_count=star_info[1][3:]
    if(star_rank=='5성급'): star_rank='★★★★★'
    elif (star_rank=='4성급'): star_rank='★★★★'
    elif (star_rank == '3성급'): star_rank = '★★★'
    elif (star_rank == '2성급'): star_rank = '★★'
    elif (star_rank == '1성급'): star_rank = '★'
    star_list.append((star_rank, star_count))

csvfile=pd.DataFrame(star_list, columns=['별점', '리뷰 개수'])
csvfile.to_csv('googlemap_daejeo_info.csv', mode='a', encoding='utf-8-sig', header=True, index=False)
'''
