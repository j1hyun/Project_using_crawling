import pandas as pd
from bs4 import BeautifulSoup

df = pd.read_json("review_daejeo.json", encoding='UTF-8')


def parser(body): #대저생태공원
    bs = BeautifulSoup(body, 'html.parser')
    user_name = bs.find('span', jstcache='368').text
    date = bs.find('span', jstcache='218').text
    ratingtemp = str(bs).split('개 \" ')[0]
    ratingtemp = ratingtemp.split('별표 ')[1]
    review_text = bs.find('span', jstcache='221').text

    return user_name, date, ratingtemp, review_text
'''
def parser(body): #삼락생태공원
    bs = BeautifulSoup(body, 'html.parser')
    user_name = bs.find('span', jstcache='1390').text
    date = bs.find('span', jstcache='1240').text
    ratingorg = bs.find('span', class_='section-review-stars').text
    ratingtemp = str(bs).split('개 \" ')[0]
    ratingtemp = ratingtemp.split('별표 ')[1]
    review_text = bs.find('span', jstcache='1243').text

    return user_name, date, ratingtemp, review_text
'''
df['user_name'], df['date'], df['rating'], df['review_text'] = zip(*df['body'].map(parser))
del df["body"]
df = df.applymap(lambda x: x.replace('\U0001f44d', '').replace('\U0001f618', ''))

df.to_csv('googlemap_daejeo_review.csv', encoding='utf-8-sig')