import yfinance as yf
import pandas as pd
import numpy as np
import traceback
import time
from datetime import date
from Finance_Support.utility.system_save import save_csv
from Finance_Support.utility.email_notify import smtp
from Finance_Support.utility.settings import mail_writer,mail_group 

def with_dividend():
    try:
        # 讀取台股列表
        stock_list = pd.read_csv('./data/market/stocks/stock_list.csv')

        # 獲取所有的股票代號並儲存成array 或list
        all_stock = stock_list['代號'].values

        # 儲存每支股票的殖利率
        dividend_store = []
        stock_store = []


        # loop 每一支股票
        for i,s in enumerate(all_stock):
            
                #計算每一筆處理的時間, 在開頭紀錄一個時間點
                start = time.time()
                
                
                # yfinance 呼叫 Ticker
                stock = yf.Ticker(f'{s}.TW')
                
                try:
                    if stock.info['dividendYield'] != None:

                        # info 中具備殖利率資訊, 這邊紀錄的是 Forward dividend yield, 指的是第一季的配息來預估整年度的可能配息
                        d_y = stock.info['dividendYield']
                        # 有時候yfinance 回傳的資料有異常需做排除, 如果值不是0 且大於 0.05 才儲存
                        if d_y >= 0.05:
                            stock_store.append(s)
                            dividend_store.append(d_y)
                    else:
                        d_y = None

                    # 紀錄結束時間
                    end = time.time()
            
                    #print進度
                    print(f'Dealing: {i+1} | All: {all_stock} | Cost TIme: {end-start}s')

                except:
                    print(f"Error Stock ! Dealing: {i} | All: {len(all_stock)} | Stock: {s}")

        data = pd.DataFrame()
        data['代號'] = stock_store
        data['殖利率'] = dividend_store
        save_csv(data,'market/dividend/dividend_list.csv')

        dividend_info = np.array(dividend_store)

        # 平均數
        print(f'Mean:{np.mean(dividend_info)}')

        # 最大
        print(f'Max:{np.max(dividend_info)}')

        # 最小
        print(f'Min:{np.min(dividend_info)}')

        # 標準差
        print(f'Std:{np.std(dividend_info)}')

        # 第50分位數
        print(f'50%:{np.percentile(dividend_info,50)}')

        # 第70分位數
        print(f'70%:{np.percentile(dividend_info,70)}')

        # 第90分位數
        print(f'90%:{np.percentile(dividend_info,90)}')

    except SystemExit:
         print('It is OK')

    except:
        today = date.today()

        subject = f'{today} 高配息名單篩選異常'
        body = traceback.format_exc()

        smtp(mail_writer,mail_group,subject,body)