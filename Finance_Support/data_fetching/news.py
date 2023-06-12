import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

'''
在這邊不用Selenium , 嘗試用bs4 因為 yahoo 也有分頁的新聞列表
'''



def get_yahoo_news(stock:str,target_page:int) -> pd.DataFrame:

    '''
    stock : 目標股價
    target_page : 要抓取的頁數
    '''

    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
    try:
        data = requests.get(f"https://tw.stock.yahoo.com/q/h?s={stock}",headers=headers)

        # 使用bs 解析
        soup = BeautifulSoup(data.text)

        # find 找到的共幾頁元素
        page = soup.find('span',{'class':'mtext'})

        #建立一個空字串
        x= ''

        # 迴圈處理page 元素, 符合的加起來
        for i in page.text:
            if i.isdigit():
                x+=i
        
        x = int(x)

        # 如果目標頁數比 x 小, 那拿來帶入的 x 就可以直接替換成目標頁數
        x = target_page if target_page < x else x

        # 準備儲存變數的list 
        title, url, date_store = [],[],[]
        # 準備儲存所有資料的空df
        result = pd.DataFrame()

        for i in range(1,x+1):
            #為求穩定, 加入time.sleep()
            time.sleep(2)
            data= requests.get(f"https://tw.stock.yahoo.com/q/h?s={stock}&pg={str(i)}",headers=headers)
            soup = BeautifulSoup(data.text)

            #find_all() 獲取所有都是td 且屬性為 height: 37 的 tag
            article = soup.find_all('td',{'height': '37'})
            # 一樣用 BS 物件來尋找定位, 獲取 td tage 且屬性為 height: 29
            date_data = soup.find_all('td',{'height':'29'})

            for x,y in zip(article,date_data):
                
                # 把三個資訊都append 到 list 中
                title.append(x.text)
                url.append('https://tw.stock.yahoo.com'+ x.find('a')['href'])
                date_store.append((y.text.split()[0])[1:])

        result['title'] = title
        result['url'] = url
        result['date'] = date_store
    except:
        result = pd.DataFrame()
        result['title'] = ['Error']
        result['url'] = ['Error']
        result['date'] = ['Error']
    
    return result

