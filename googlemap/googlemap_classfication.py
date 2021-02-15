import pandas as pd

data_list = []

data=pd.read_csv('대저생태공원1819.csv', index_col=False)
data_list.append(data)
df_set=pd.concat(data_list)
df_set.duplicated(["게시글"])
df = df_set.drop_duplicates(["게시글"], keep="first")
del df["Unnamed: 0"]

df2019=df.loc[df_set['게시 날짜'].str.contains('2019', na=False)]
df2018=df.loc[df_set['게시 날짜'].str.contains('2018', na=False)]

df2019.to_csv('instagram_daejeo_2019.csv', mode='wt', encoding='utf-8-sig', index=False)  # csv 파일로 저장
df2018.to_csv('instagram_daejeo_2018.csv', mode='wt', encoding='utf-8-sig', index=False)  # csv 파일로 저장

df2019.index=df2019.index+1
df2018.index=df2018.index+1