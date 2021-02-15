import pandas as pd
import matplotlib.pyplot as plt


data_list=[]
time=[]
data=pd.read_csv('googlemap_daejeo_info.csv', index_col=False)
data_list.append(data)
df_set=pd.concat(data_list)
df_set=df_set.loc[df_set['시간'].str.contains('시', na=False)] #밑의 별점 제거
df=df_set.apply(lambda x: x.str.strip('%'), axis=1) #데이터프레임 전체에 대해 % 제거
print(df)
df[['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']]=df[['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']].apply(pd.to_numeric)
df.set_index(df['시간'], inplace=True)
df.drop('시간', axis=1, inplace=True)
print(df)
time=str(df.index.tolist())
print(type(time))
plt.rc('font', family='Malgun Gothic', size=7)

ax=df.plot(title='daejeopark popular times', figsize=(12,4), legend=True, fontsize=8)
ax.set_xlabel('시간', fontsize=10)
ax.set_ylabel('상대적 혼잡도', fontsize=10)

plt.legend()
plt.show()
