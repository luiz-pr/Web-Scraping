import json
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


url = "https://www.nba.com/stats/players/traditional/?sort=PTS&dir=-1"
top10ranking = {}

rankings = {
    '3points': {'field': 'FG3M,', 'label': '3PM'},
    'points': {'field': 'PTS,', 'label': 'PTS'},
    'assinantes': {'field': 'AST,', 'label': 'AST'},
    'rebounds': {'field': 'REB,', 'label': 'REB'},
    'steals': {'field': 'STL,', 'label': 'STL'},
    'blocks': {'field': 'BLK,', 'label': 'BLK'}
}

option = Options()
option.headless = True
driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')


driver.get(url)
time.sleep(4)


driver.find_element_by_xpath('//div[@class="nba-stat-table"]//table//thead//tr//th[@data-field="PTS"]').click()


element = driver.find_element_by_xpath('//div[@class="nba-stat-table"]//table')
html_content = element.get_attribute('outerHTML')


soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name='table')


df_full = pd.read_html(str(table))[0].head(10)
df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', 'PTS']]
df.columns = ['pos', 'player', 'team', 'total']


top10ranking['points'] =df.to_dict('records')


driver.quit()


js = json.dumps(top10ranking)
fp = open('ranking.txt', 'w')
fp.write(js)
fp.close()