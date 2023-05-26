from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import json
import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--incognito")
options.add_argument("--disable-popup-blocking ")

class Stock_News():
    def __init__(self,stock_id):
        self.stock_id = stock_id

        self.driver = webdriver.Chrome(options=options)
        self.titles = []
        self.urls = []
        self.dates = []
        self.df = pd.DataFrame()
        
    def crawl(self):
        # Visit
        self.driver.get(f'https://tw.stock.yahoo.com/quote/{self.stock_id}')

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
            
            self.driver.execute_script(js_scroll)
            
            sleep(1)
            
            innerHeightOfWindow = self.driver.execute_script(
                'return window.document.documentElement.scrollHeight;'
            )
            
            sleep(1)
            
            print("innerHeightOfWindow: {}, totalOffset: {}".format(innerHeightOfWindow, totalOffset))
        
        # Get url
        news_div = self.driver.find_elements(
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
                    self.urls.append(a) 

        # Get title,date
        for url in self.urls:
            res = requests.get(url,headers=headers)

            soup = BeautifulSoup(res.text)

            title = soup.find("h1",{"data-test-locator":"headline"})
            self.titles.append(title.text)
            date_data = soup.find("div",{"class":"caas-attr-time-style"})
            date_time = date_data.find("time")
            date = date_time.attrs['datetime'].split('T')[0]
            self.dates.append(date)    
        
        # To DataFrame
        
        self.df['title'] = self.titles
        self.df['url'] = self.urls
        self.df['date'] = self.dates
    
    # Save CSV 
    def save(self):
        self.df.to_csv(f'{self.stock_id[:4]+self.stock_id[5:]}_news.csv')
    
    # Close driver
    def close(self):
        self.driver.quit()
    
        


    
if __name__ == '__main__':
    stock_id = '2330.TW'
    n = Stock_News(stock_id)
    n.crawl()
    n.save()
    n.close()