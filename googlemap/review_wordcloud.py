import pandas as pd
from konlpy.tag import Okt
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

okt = Okt()

def insta_morph(data):
    data_list = []
    data_list.append(data)
    df_set = pd.concat(data_list)
    df_set.duplicated(["게시글"])
    df = df_set.drop_duplicates(["게시글"], keep="first")

    new_list = []
    for row in df["게시글"]:
        if (row != ''):
            new = re.sub('[^#A-Za-z0-9ㄱ-ㅣ가-힣]+', ' ', str(row))
        if (new == ''):
            del new
        else:
            morph = okt.pos(new)
            new_list.append(morph)

    return new_list

def googlemap_morph(data):
    data_list = []
    data_list.append(data)
    df_set = pd.concat(data_list)
    df_set.duplicated(["review_text"])
    df = df_set.drop_duplicates(["review_text"], keep="first")

    new_list=[]
    for row in df["review_text"]:
        if(row !=''):
            new = re.sub('[^#A-Za-z0-9ㄱ-ㅣ가-힣]+', ' ',str(row))
            new = re.sub('원문|번역|google|제공', '', str(row)) #번역 리뷰에 뜨는 문구 제거
        if (new==''):
            del new
        else:

            morph = okt.pos(new)
            new_list.append(morph)

    return new_list

def insta_list(new_list):
    count_list1 = []
    count_list2 = []
    for sentence in new_list:
        for word, tag in sentence:
            if (tag in ['Noun', 'Adjective'] and len(word) > 1):  # 동사가 아니고 두 글자 이상일 때
                count_list1.append((word))
            if tag in 'Hashtag' and len(word) > 1:
                count_list2.append((word))

    counts1 = Counter(count_list1)
    counts2 = Counter(count_list2)
    words = counts1.most_common(100)
    hashtags = counts2.most_common(100)

    common_list=[]

    for i in range(100):
        m = okt.pos(words[i][0])
        common_list.append((words[i][0], m[0][1], words[i][1], hashtags[i][0], hashtags[i][1]))
    return words, hashtags, common_list

def googlemap_list(new_list): #구글맵 리뷰
    count_list1 = []
    for sentence in new_list:
        for word, tag in sentence:
            if (tag in ['Noun', 'Adjective'] and len(word) > 1):  # 동사가 아니고 두 글자 이상일 때
                count_list1.append((word))

    counts1 = Counter(count_list1)
    words = counts1.most_common(100)
    common_list = []

    for i in range(100):
        m = okt.pos(words[i][0])
        common_list.append((words[i][0], words[i][1], m[0][1]))
    return words, common_list

def wordcloud(words):
    wc = WordCloud(
        font_path='C:\Windows\Fonts\MALGUNBD.TTF',
        width=800,
        colormap='Accent_r',
        height=800,
        background_color="White")

    wc.generate_from_frequencies(dict(words))
    return wc

def save_insta_file(key,year, wc, common_list):
    wc.to_file('wordcloud_insta_' + key + '_' + year + '.png')
    word_count = pd.DataFrame(common_list, columns=['단어', '품사', '빈도수', '해시태그', '개수'])
    word_count.to_csv('instagram_' + key + '_' + year + '_most_common.csv', mode='wt', encoding='utf-8-sig',
                      header=True, index=False)
    xpos = np.arange(len(word_count['해시태그']))
    xtext = list(word_count["해시태그"])
    return word_count, xpos, xtext

def save_googlemap_file(key,year, wc, common_list):
    wc.to_file('wordcloud_googlemap_'+key+'_'+year+'.png')
    word_count=pd.DataFrame(common_list, columns=['단어', '빈도수', '품사'])
    word_count.to_csv('googlemap_'+key+'_'+year+'_most_common.csv', mode='wt', encoding='utf-8-sig', header=True, index=False)
    xpos = np.arange(len(word_count['단어']))
    xtext = list(word_count["단어"])
    return word_count,xpos,xtext

def draw_googlemap_graph(word_count, xpos, xtext, key, year):

    plt.title(year+ '년 ' + key+ "park most common words(googlemap)")
    plt.xlabel('단어')
    plt.ylabel('빈도수')
    plt.yticks(xpos, xtext)
    plt.ylim(0, 10)
    plt.barh(word_count['단어'], word_count['빈도수'], color='green', height=0.7)
    plt.tight_layout()
    plt.savefig('bar_googlemap_' + key + '_' + year + '.png')
    return
def draw_insta_graph(word_count, xpos, xtext, key, year):
    plt.title(year + '년 ' + key + "park most common words(instagram)")
    plt.xlabel('해시태그')
    plt.ylabel('개수')
    plt.yticks(xpos, xtext)
    plt.ylim(0, 10)
    plt.barh(word_count['해시태그'], word_count['개수'], color='green', height=0.7)
    plt.tight_layout()
    plt.savefig('bar_instagram_' + key + '_' + year + '.png')

key=['daejeo','samrak']
year=['2018','2019']

googlemap_data=[pd.read_csv('googlemap_daejeo_2018.csv', index_col=False),
        pd.read_csv('googlemap_daejeo_2019.csv', index_col=False),
         pd.read_csv('googlemap_samrak_2018.csv', index_col=False),
          pd.read_csv('googlemap_samrak_2019.csv', index_col=False)]

insta_data=[pd.read_csv('instagram_daejeo_2018.csv', index_col=False),
            pd.read_csv('instagram_daejeo_2019.csv', index_col=False),
            pd.read_csv('instagram_samrak_2018.csv', index_col=False),
            pd.read_csv('instagram_samrak_2019.csv', index_col=False)]

font_name = mpl.font_manager.FontProperties(fname='C:\Windows\Fonts\MALGUNBD.TTF').get_name()
mpl.rc('font', family=font_name)

k=0
for i in range (len(key)):
    for j in range(len(year)):
        googlemap_review = googlemap_morph(googlemap_data[k])
        common_words, common_list = googlemap_list(googlemap_review)
        wc=wordcloud(common_words)
        word_count, xpos, xtext = save_googlemap_file(key[i], year[j], wc, common_list)
        draw_googlemap_graph(word_count, xpos, xtext, key[i], year[j])
        plt.cla()
        k=k+1

p=0
for i in range (len(key)):
    for j in range(len(year)):
        insta_review = insta_morph(insta_data[p])
        common_words, common_tag, common_list = insta_list(insta_review)
        wc=wordcloud(common_words)
        word_count, xpos, xtext = save_insta_file(key[i], year[j], wc, common_list)
        draw_insta_graph(word_count, xpos, xtext, key[i], year[j])
        plt.cla()
        p=p+1



