import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager, rc
from pytrends.request import TrendReq
from bs4 import BeautifulSoup
import requests

def sample_collector(word):
    url = requests.get('https://en.oxforddictionaries.com/definition/' + word, allow_redirects=True)
    web_data = requests.get(url.url)
    soup = BeautifulSoup(web_data.text, 'lxml')
    title = word
    sample = soup.select('.exg .ex em')[0].get_text()   
    synonym = soup.select('.synonyms .exg .exs strong')[0].get_text()

    print(title + ':\n' + sample)
    return synonym


word = input('input your word：')

synonym = sample_collector(word)
sample_collector(synonym)

plt.rcParams['axes.unicode_minus'] = False
f_path = 'C:/Windows/Fonts/malgun.ttf'
font_name = font_manager.FontProperties(fname=f_path).get_name()
rc('font', family=font_name)

pytrends = TrendReq(hl='en-US', tz=360)
kw_list = []

kw_list.append(word)
kw_list.append(synonym)

timeframe='2017-10-30 2018-10-30'
pytrends.build_payload(kw_list, cat = 0, timeframe=timeframe)
col_names = kw_list
df=pytrends.interest_over_time()
del(df.index.name)
df.drop('isPartial', 1, inplace=True)


plt.figure(figsize=(10,10))
for i in kw_list :
    plt.plot(df[i], data = df[i], label = i)

name = ''
for i in kw_list :
    if i == kw_list[-1] :
        name = name  + " " + i
        break
    name = name + " " + i + " &"

plt.title(name+' '+timeframe)
plt.legend()
plt.show()



