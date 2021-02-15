import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def get_info(url):
    html = requests.get(url).text

    soup = BeautifulSoup(html,'html.parser')

    month_list=[]
    temp_list1=[]
    day_list=[]
    caption=soup.select('#content_weather > table > caption')[0].text
    table=soup.findAll('th', class_='top_line')

    for j in range(len(table)):
        month=table[j].text
        if(j>0):
            month_list.append(month)

    t=soup.find('tbody')
    ta=t.find_all('td') #tobdy 아래의 모든 td 정보

    for i in range(len(ta)):
        temp = ta[i].text
        if(i==0 or i%13==0):
            day_list.append(temp)
        else:
            temp_list1.append(temp)

    result = [temp_list1[i * 12:(i + 1) * 12] for i in range((len(temp_list1) + 11) // 12 )]
    return caption,result, month_list, day_list

def get_wind(url):
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.findAll('th', class_='top_line')
    month_list=[]
    day_list=[]
    wind_list=[]

    if(url[68:72]=="2018"):
        df = pd.read_json("2018_wind_info.json", encoding='UTF-8')
    elif(url[68:72]=="2019"):
        df = pd.read_json("2019_wind_info.json", encoding='UTF-8')
    for j in range(len(table)):
        month=table[j].text
        if(j>0):
            month_list.append(month)

    info_list=df.values.tolist()
    for i in range(len(info_list)):
        if(i==0 or i%13==0):
            split_word=str(info_list[i]).split(">")[1]
            day_list.append(split_word[:-4])
        else:
            split_word = str(info_list[i]).split(">")[3]
            wind_list.append(split_word[:-4])


    result = [wind_list[i * 12:(i + 1) * 12] for i in range((len(wind_list) + 11) // 12)]
    temptable = pd.DataFrame(result, columns=month_list, index=day_list)
    if (url[68:72] == "2018"):
        temptable.to_csv('2018년 부산 기후-풍속.csv', encoding='utf-8-sig')
    elif (url[68:72] == "2019"):
        temptable.to_csv('2019년 부산 기후-풍속.csv', encoding='utf-8-sig')

wind_url=["https://www.weather.go.kr/weather/climate/past_table.jsp?stn=108&yy=2018&obs=06&x=29&y=13",
        "https://www.weather.go.kr/weather/climate/past_table.jsp?stn=108&yy=2019&obs=06&x=29&y=13"]

for j in range(len(wind_url)):
    get_wind(wind_url[j])

url=["https://www.weather.go.kr/weather/climate/past_table.jsp?stn=159&yy=2019&obs=10&x=15&y=11",
     "https://www.weather.go.kr/weather/climate/past_table.jsp?stn=159&yy=2019&obs=10&x=14&y=11",
     "https://www.weather.go.kr/weather/climate/past_table.jsp?stn=159&yy=2019&obs=08&x=23&y=10",
     "https://www.weather.go.kr/weather/climate/past_table.jsp?stn=159&yy=2019&obs=21&x=24&y=17",
     "https://www.weather.go.kr/weather/climate/past_table.jsp?stn=159&yy=2019&obs=12&x=5&y=15",
     "https://www.weather.go.kr/weather/climate/past_table.jsp?stn=159&yy=2019&obs=35&x=3&y=0",
     "https://www.weather.go.kr/weather/climate/past_table.jsp?stn=159&yy=2019&obs=59&x=12&y=6",
     "https://www.weather.go.kr/weather/climate/past_table.jsp?stn=159&yy=2019&obs=90&x=20&y=9",
     "https://www.weather.go.kr/weather/climate/past_table.jsp?stn=159&yy=2018&obs=10&x=15&y=11",
     "https://www.weather.go.kr/weather/climate/past_table.jsp?stn=159&yy=2018&obs=10&x=14&y=11",
     "https://www.weather.go.kr/weather/climate/past_table.jsp?stn=159&yy=2018&obs=08&x=23&y=10",
     "https://www.weather.go.kr/weather/climate/past_table.jsp?stn=159&yy=2018&obs=21&x=24&y=17",
     "https://www.weather.go.kr/weather/climate/past_table.jsp?stn=159&yy=2018&obs=12&x=5&y=15",
     "https://www.weather.go.kr/weather/climate/past_table.jsp?stn=159&yy=2018&obs=35&x=3&y=0",
     "https://www.weather.go.kr/weather/climate/past_table.jsp?stn=159&yy=2018&obs=59&x=12&y=6",
     "https://www.weather.go.kr/weather/climate/past_table.jsp?stn=159&yy=2018&obs=90&x=20&y=9"]

for i in range(len(url)):
    caption,result, month_list, day_list =get_info(url[i])

    temptable = pd.DataFrame(result, columns=month_list, index=day_list)
    if(url[i][68:72]=="2018"):
        temptable.to_csv('2018년 부산 기후-'+caption+'.csv', encoding='utf-8-sig')
    elif(url[i][68:72]=="2019"):
        temptable.to_csv('2019년 부산 기후-' + caption + '.csv', encoding='utf-8-sig')

