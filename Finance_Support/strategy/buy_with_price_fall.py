import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date,timedelta
import time
from Finance_Support.utility.deal_holiday import Holiday_Detect
from Finance_Support.utility.email_notify import smtp
from Finance_Support.utility.settings import mail_group,mail_writer
from Finance_Support.data_fetching.news import get_yahoo_news
from Finance_Support.utility.system_save import save_csv
def with_price_fall():

    data = pd.read_csv('./data/market/stocks/stock_list.csv')

    # 讀取股票清單
    target_stock = data['代號'].to_list()

    # 獲取今日
    today = date.today()

    # 判斷營業日
    holiday = Holiday_Detect()

    if not holiday.is_open(now_date=today):

        subject = '高配息低股價, 每日價格比對 - 今日休市'
        body = ''

        smtp(mail_writer,mail_group,subject,body)
        exit()

    # 獲取過去10天的收盤價 , 抓20日以防沒有成功抓足夠 20個營業日
    date_start = today + timedelta(days=-20)
    #轉為str 以準備獲取歷史資料
    date_start = date_start.strftime('%Y-%m-%d')
    # 獲取T+1日當作最後一天, 因為yf 的 end 日期是 T-1
    date_end = today+ timedelta(days=1)
    # 轉為str 格式準備獲取歷史資料
    date_end =date_end.strftime('%Y-%m-%d')

    # 創建空list 備用
    stock_store = []
    today_store = []
    today_fall = []
    count = 0

    # loop處理每一支股票
    for target in target_stock:

        count+= 1 
        # yf 還是屬於requests , 因為請求次數很高, 為了維持品質需要 time.sleep
        time.sleep(1)
        # 獲取目標股票 Ticker

        stock = yf.Ticker(f'{target}.TW')

        # 傳入start 跟 end 獲取歷史股價
        df = stock.history(start=date_start,end=date_end)

        #做一點基本檢核, 防止資料回傳 0 或 1 筆
        if len(df) >=5:
            # 將收盤價轉為 array 並且取最後一筆, 得到今天的收盤
            today_price = df['Close'].values[-1]
            # 將收盤價轉為 array 並且取倒數第二筆, 得到昨天的收盤價
            yes_price = df['Close'].values[-2]
            # 將收盤價轉為 array 並且取倒數第三筆, 得到前天的收盤價
            be_yes_price = df['Close'].values[-3]

            '''
            漲跌幅公式:

                漲跌幅 = (現價 - 上一交易日的收盤價) / 上一交易日的收盤價 X 100%
            '''

            # 根據公式取得今日漲跌幅
            change_today = ((today_price-yes_price)/yes_price) *100
            # 根據公式取得昨日漲跌幅
            change_yesterday = ((yes_price-be_yes_price)/yes_price) *100

            # 兩個漲跌幅皆小於-5 則是我們的目標, 儲存起來
            if change_today <=-5 and change_yesterday <=-5:
                today_store.append(today_price)
                today_fall.append(change_today)
                stock_store.append(target)
            
            # print處理進度
            print(f'Dealing Stock: {target} | All Stock: {len(target_stock)} | Now: {count}')

    control = 0

    # Loop 剛剛篩選的結果
 
    for t in stock_store:
        #求穩定
        time.sleep(1)
        # 將目標股票的新聞連接在一起, 

        if control == 0:
            # 使用新聞函數獲取新聞, 並且先獲取主要的df, 其他股票的就連接在後念
            main_df = get_yahoo_news(t,1)
            # 多一個欄位叫做stock 儲存這篇新聞屬於哪一支股票
            main_df['stock'] = len(main_df)*[t]
            
            control+=1

        else:
            #新的變數獲取新聞
            merge_df = get_yahoo_news(t,1)
            # 取得的新聞所屬的股票
            merge_df['stock'] = len(merge_df)*[t]
            # 接在最一開始的df 後面
            main_df = main_df.append(merge_df)
    
    save_csv(main_df,'market/news/fall_stocks.csv')

    empty_df = pd.DataFrame()
    empty_df['股票代號'] = stock_store
    empty_df['今日價格'] = today_store
    empty_df['今日漲跌幅%'] = today_fall
    # 轉為html 作為表格備用
    empty_df = empty_df.to_html(index=False)

    subject = f'{today} 暴跌股票 - 今日暴跌股票'

    body = f'''<html>
                <font face="微軟正黑體"></font>
                <body>
                    <h2>
                    下表暴跌股票列表
                    </h2>
                    <h4>{empty_df}</h4>
                </body>
            </html>'''
    
    smtp(mail_writer,mail_group,subject,body,mode='html')
    