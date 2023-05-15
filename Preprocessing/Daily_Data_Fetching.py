import requests
import pandas as pd
from io import StringIO
import os
import time
from datetime import datetime, timedelta

class Daily_Data():

    def __init__(self,headers,date):

        self.headers = headers
        self.date = date

    def crawl_price(self):
    
        # 將 date 變成字串 舉例：'20180525' 
        datestr = datetime.strftime(self.date,'%Y%m%d')
        
        

        # 從網站上依照 datestr 將指定日期的股價抓下來
        r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALLBUT0999',headers=self.headers)
        
        if r.status_code == 200:
            # 將抓下來的資料（r.text），其中的等號給刪除
            content = r.text.replace('=', '')
            
            # 將 column 數量小於等於 10 的行數都刪除
            lines = content.split('\n')
            lines = list(filter(lambda l:len(l.split('",')) > 10, lines))
            
            # 將每一行再合成同一行，並用肉眼看不到的換行符號'\n'分開
            content = "\n".join(lines)
            
            # 假如沒下載到，則回傳None（代表抓不到資料）
            if content == '':
                print(f'{self.date.year}-{self.date.month}-{self.date.day} no data')
                return None
            
            # 將content變成檔案：StringIO，並且用pd.read_csv將表格讀取進來
            df = pd.read_csv(StringIO(content))
            
            # 將表格中的元素都換成字串，並把其中的逗號刪除
            df = df.astype(str)
            df = df.apply(lambda s: s.str.replace(',', ''))
            
            # 將爬取的日期存入 dataframe
            df['date'] = pd.to_datetime(self.date)
            
            # 將「證券代號」的欄位改名成「stock_id」
            df = df.rename(columns={'證券代號':'stock_id'})
            
            # 將 「stock_id」與「date」設定成index 
            df = df.set_index(['stock_id', 'date'])
            
            # 將所有的表格元素都轉換成數字，error='coerce'的意思是說，假如無法轉成數字，則用 NaN 取代
            df = df.apply(lambda s:pd.to_numeric(s, errors='coerce'))
            
            # 刪除不必要的欄位
            df = df[df.columns[df.isnull().all() == False]]
            
            if not os.path.isdir(f'./data/{self.date.year}'):
                os.mkdir(f'./data/{self.date.year}')
                
            if not os.path.isdir(f'./data/{self.date.year}/M{self.date.month}'):
                os.mkdir(f'./data/{self.date.year}/M{self.date.month}')
            
            df.to_csv(f'./data/{self.date.year}/M{self.date.month}/D{self.date.day}.csv') 

            return df
        
        else:
            print(f'Fetch {self.date.year}-{self.date.month}-{self.date.day} Failed, Status_Code: {r.status_code}')
