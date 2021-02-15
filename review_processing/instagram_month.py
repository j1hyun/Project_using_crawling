import pandas as pd
from collections import Counter
import re
from konlpy.tag import Okt
from konlpy.tag import Kkma
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

okt=Okt()
kkma=Kkma()

def common_words(df):
    new_list = []
    for row in df["게시글"]:
        if (row != ''):
            new = re.sub('[^#A-Za-z0-9ㄱ-ㅣ가-힣]+', ' ', str(row))
            new = re.sub('원문|번역|google|제공', '', str(row))  # 번역 리뷰에 뜨는 문구 제거
        if (new == ''):
            del new
        else:

            morph = okt.pos(new)
            new_list.append(morph)

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
    common_list = []
    for i in range(100):
        m = okt.pos(words[i][0])
        common_list.append((words[i][0], m[0][1], words[i][1], hashtags[i][0], hashtags[i][1]))
    return common_list


data_list=[]
data=pd.read_csv('instagram_daejeo_2019.csv', encoding='utf-8-sig',index_col=False)
data_list.append(data)
df=pd.concat(data_list)

df1=df.loc[df['게시 날짜'].str.contains('-01-|-02-|-03-|-04-|-05-|-06-', na=False)]
df2=df.loc[df['게시 날짜'].str.contains('-07-|-08-|-09-|-10-|-11-|-12-', na=False)]
common_list=common_words(df1)
print('\n\n')
common_words(df2)

word_count = pd.DataFrame(common_list, columns=['단어', '품사', '빈도수', '해시태그', '개수'])

font_name = mpl.font_manager.FontProperties(fname='C:\Windows\Fonts\MALGUNBD.TTF').get_name()
mpl.rc('font', family=font_name)
plt.title("daejeo park most common words(2019 상반기)")
plt.xlabel('단어')
plt.ylabel('개수')

xpos = np.arange(len(word_count['단어']))
xtext = list(word_count["단어"])

plt.yticks(xpos, xtext)
plt.ylim([0,10])
plt.barh(word_count['단어'], word_count['빈도수'], color='green', height=0.7)
plt.show()
