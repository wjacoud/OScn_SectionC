from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, os.path, sys
import pandas as pd

class TimeOutException(Exception):
    pass

op = webdriver.ChromeOptions()
p = {'download.default_directory':'/Users/wilsonjacoud/VSCProjects/OddsScanner'}
op.add_experimental_option('prefs', p)

driver = webdriver.Chrome('/usr/local/lib/python3.9/site-packages/chromedriver', options=op)
driver.get('https://finance.yahoo.com/quote/BTC-EUR/history/')
driver.find_element_by_name('agree').click()
driver.get('https://query1.finance.yahoo.com/v7/finance/download/BTC-EUR?period1=1603737390&period2=1635269790&interval=1d&events=history&includeAdjustedClose=true')

curTime = 0
while not os.path.exists('BTC-EUR.csv'):
    time.sleep(1)
    curTime += 1
    if curTime > 30:
        print("TimeOut Error!")
        raise TimeOutException()

contents = pd.read_csv('BTC-EUR.csv', nrows=10)
contents.columns = ['Date', 'Open', 'High', 'Low', 'BTC Closing Value', 'Adj Close', 'Volume']
contents.to_csv('eur_btc_rates.csv', columns=['Date','BTC Closing Value'], index=False)