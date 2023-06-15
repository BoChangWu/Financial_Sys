from Finance_Support.utility.deal_holiday import Holiday_Detect
from Finance_Support.utility.email_notify import smtp
from Finance_Support.utility.settings import mail_writer,mail_group
import pandas as pd
import yfinance as yf
import numpy as np
from datetime import date,timedelta
import traceback

'''
每個人都有自己決定目標股價的方法, 如操作短線的投資人會透過演算法來決定,
以下是透過統計小於過去一年內的最高價的 70% 來決定
'''

def with_devidend_price():
    #讀取高配息清單
    data = pd.read_csv('./data/market/dividend/dividend_list.csv')


    # 獲取代號
    target_stock = data['代號'].to_list()

    # 獲取今天日期
    today = date.today()

    # 判斷是否營業日
    detect = Holiday_Detect()
    if not detect.is_open(now_date= today):
        
        subject = '高配息低股價, 每日價格比對 - 今日休市'
        body = ''

        smtp(mail_writer,mail_group,subject,body)
        exit()

    # 獲取過去一年的日期, 以365天來估算
    date_start = today + timedelta(days=-365)
    # 轉為 str格式準備傳入 yf 的 history 獲取歷史股價
    date_start = date.strftime(date_start,'%Y-%m-%d')
    # 獲取 T+1日, 因為 yf 的 end 日期是 T-1
    date_end = today + timedelta(days=1)
    # 轉為 str 格式等一下準備傳入 yf 的 history 獲取歷史股價
    date_end = date.strftime(date_end,'%Y-%m-%d')

    # 創建空list備用
    target_store = []
    highest_store = []
    now_price_store = []

    # loop 處理每一支目標股票
    for target in target_stock:

        #獲取目標股票的 Ticker
        stock = yf.Ticker(f'{target}.TW')
        # 傳入start 跟 end 獲取歷史股價
        df = stock.history(start=date_start,end=date_end)
        # 轉為 array 並使用 np.max 獲取最大值
        highest = np.max(df['High'].values)
        # 取最後一筆的 Close 價格作為目標
        now_price = df['Close'].values[-1]
        
        #如果目標小於一年內最高價的70% 則執行以下動作
        if now_price < highest*0.7:

            #儲存股票代號
            target_store.append(target)
            # 儲存一年內最高價
            highest_store.append(highest)
            # 儲存最近的收盤價
            now_price_store.append(now_price)

            print(f'Stock: {target} | high 70%: { highest*0.7} | now: {now_price} | Status: Get!' )

    # 用 html 來寄信
    # 讀取所有股票清單
    all_stock_list = pd.read_csv('./data/market/stocks/stock_list.csv')
    # 創建空 list 備用
    stock_name_store = []
    # loop 符合我們目標的股票

    for st in target_store:
        # dataframe 的篩選, 選出目標股價
        select_data = all_stock_list[(all_stock_list[u'代號']==st)]
        # 取得後取股票平稱後轉values 再取裡面的元素
        target = select_data['股票名稱'].values[0]
        # append 進 list
        stock_name_store.append(target) 

    # 準備寄信
    empty_df = pd.DataFrame()
    empty_df['日期'] = len(target_store)*[today]
    empty_df['股票代號'] = target_store
    empty_df['股票名稱'] = stock_name_store
    empty_df['最近收盤'] = now_price_store
    empty_df['一年內最高'] = highest_store

    # 將 df 轉為 HTML 格式
    empty_df = empty_df.to_html(index=False)
    print(empty_df)

    subject = f'{today} 高配息低股價 - 每日價格比對'

    body = f'''<html>
                <font face="微軟正黑體"></font>
                <body>
                    <h2>
                    下表股票配息高且股價相對低
                    </h2>
                    <h4>{empty_df}</h4>
                </body>
            </html>'''
    
    smtp(mail_writer,mail_group,subject,body,mode='html')

if __name__ == '__main__':

    with_devidend_price()