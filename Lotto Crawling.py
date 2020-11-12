from selenium import webdriver
import os
import time
from bs4 import BeautifulSoup
import pandas as pd
from urllib.error import URLError, HTTPError


savepath = '/Users/jaeyoungcho/PycharmProjects/OpenAPI/API/lotto'
try:
    if not os.path.isdir('/Users/jaeyoungcho/PycharmProjects/OpenAPI/API/lotto'):
        os.makedirs('/Users/jaeyoungcho/PycharmProjects/OpenAPI/API/lotto')
except OSError as e:
    print('failed')
else:
    print('폴더를 생성했습니다.')

number = []
bonus_number = []
date = []
cnt = []

try:
    for i in range(1,937):
        brow = webdriver.Chrome('/Users/jaeyoungcho/PycharmProjects/OpenAPI/API/chromedriver')
        # options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        # brow = webdriver.Chrome('/Users/jaeyoungcho/PycharmProjects/OpenAPI/API/chromedriver',options=options)
        time.sleep(3)
        brow.maximize_window()
        url = 'https://www.dhlottery.co.kr/gameResult.do?method=byWin&drwNo={}'.format(i)
        brow.get(url)
        time.sleep(3)
        temp = brow.page_source
        soup = BeautifulSoup(temp, 'html.parser')
        number.append(soup.select('div.win_result div.nums div.num.win p')[0].text)
        date.append(soup.select('div.content_wrap.content_winnum_645 div.win_result p')[0].text)
        bonus_number.append(soup.select('div.nums div.num.bonus p')[0].text)
        cnt.append(i)

        del temp,soup
        brow.close()
except URLError as e:
    print('안 돼잉 {}'.format(e))
except HTTPError as e:
    print('안 돼잉 {}'.format(e))
else:
    lotto = pd.DataFrame({'date':date,'cnt':cnt,'number':number,'bonus_number':bonus_number})
    lotto.to_csv(savepath+'/lotto.csv',sep=',',na_rep='NaN',encoding='CP949')
    print('완료 했어')

