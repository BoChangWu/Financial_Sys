import sys
sys.path.append('..')
'''
run 這個無法跑起來因為 attempted relative import beyond top-level package
解法在這: https://stackoverflow.com/questions/6323860/sibling-package-imports
'''
from Finance_Support.data_fetching.market_data import Three_Major
from Finance_Support.utility.email_notify import smtp
from Finance_Support.utility.deal_holiday import Holiday_Detect

from datetime import date,timedelta
import os
import pandas as pd
from Finance_Support.utility.settings import mail_group,mail_writer


today = date.today()

def follow_corp():
    # 傳入判斷
    is_trade = Holiday_Detect.is_open(today)

    if not is_trade:

        # 標題為三大法人篩選, 今日休市
        subject = f'{today} 三大法人篩選- 今日休市'
        # 信件內容為空
        body = ''
        # 寄信
        smtp(mail_writer,mail_group,subject,body)



    # 如果沒有三天營業日, 則回推
    # 創建空的 result
    result = []

    # 用 control 來控制獲得了幾個有開市的資料
    control = 0

    # 迴圈搜尋 x 次, 這邊代入10

    for i in range(10):
        # 如果control 比 2 還小 , 則展開搜尋
        
        if control <= 2:
            
            date_target = today+ timedelta(days=-int(i))
            
            is_trade =Holiday_Detect.is_open(date_target) 

            if not is_trade:
                continue

            #有開盤則control +1, 並且進行三大法人買賣超處理
            else:

                convert_date = date_target.strftime('%Y%m%d')
                data = Three_Major.daily_report(convert_date)
                print(data)
                
                control +=1
                exit()

        #如果 control 比2 大 , 代表已經蒐集到足夠的資料, break 結束迴圈
        else:
            break