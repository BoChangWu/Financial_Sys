import yfinance as yf
import pandas as pd
from datetime import date,timedelta,datetime
import os
from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

from utility.system_save import save_csv

yesterday = date.strftime(date.today()-timedelta(days=1),'%Y-%m-%d')

class Stock():

    def __init__(self,stock_id:str):
        
        self.stock_id = stock_id
        self.stock = yf.Ticker(stock_id)
        self.price  = self.stock.info['currentPrice']
        self.day_price_trend = {'date': date.strftime(date.today(),'%Y-%m-%d'),'trend':pd.DataFrame()}
        
    def supervise_price(self,end_time:datetime,interval=2) -> None:
        
        update_times = []
        prices = []                                                                                                                                                                                    
        t = datetime.now()
        
        # 如果沒有超過
        print('Supervicing..')
        while t <= end_time:

            t= datetime.now()
            
            self.price = yf.Ticker(self.stock_id).info['currentPrice']
            prices.append(self.price)
            update_times.append(datetime.strftime(t,'%H:%M:%S'))
            print(f'{self.price}..')
            sleep(interval)

        print('end supervicing..')
        self.day_price_trend['trend']['Price'] = prices
        self.day_price_trend['trend']['Time'] = update_times

    def news(self) -> None:
        
        headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        }
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")
        options.add_argument("--disable-popup-blocking ")

        driver = webdriver.Chrome(options=options)
        titles = []
        urls = []
        dates = []
        df = pd.DataFrame()
        
        # Crawl
        # Visit
        driver.get(f'https://tw.stock.yahoo.com/quote/{self.stock_id}')

        # Scroll
        innerHeightOfWindow = 0
        totalOffset = 0
        
        while totalOffset <= innerHeightOfWindow:
            totalOffset += 300
            js_scroll = '''(
                function (){{
                    window.scrollTo({{
                        top:{}, 
                        behavior: 'smooth' 
                    }});
                }})();'''.format(totalOffset)
            
            driver.execute_script(js_scroll)
            
            sleep(1)
            
            innerHeightOfWindow = driver.execute_script(
                'return window.document.documentElement.scrollHeight;'
            )
            
            sleep(1)
            
            print("innerHeightOfWindow: {}, totalOffset: {}".format(innerHeightOfWindow, totalOffset))
        
        # Get url
        news_div = driver.find_elements(
        By.CSS_SELECTOR,"div.Cf")

        for element in news_div:
            print("="*30)
            
            # print(element.text)
            news = element.find_elements(By.TAG_NAME,"h3")
            
            
            for n in news:
                link = n.find_element(By.TAG_NAME,"a")
                a = link.get_attribute('href')
                
                
                if  'beap.gemini' not in a:
                    print(a)
                    urls.append(a) 

        # Get title,date
        for url in urls:
            res = requests.get(url,headers=headers)

            soup = BeautifulSoup(res.text)

            title = soup.find("h1",{"data-test-locator":"headline"})
            titles.append(title.text)
            date_data = soup.find("div",{"class":"caas-attr-time-style"})
            date_time = date_data.find("time")
            date = date_time.attrs['datetime'].split('T')[0]
            dates.append(date)    
        
        # To DataFrame
        df['title'] = titles
        df['url'] = urls
        df['date'] = dates
    
        # Save CSV 
        df.to_csv(f'{self.stock_id[:4]+self.stock_id[5:]}_news.csv')
    
        # Close driver
        driver.quit()

        