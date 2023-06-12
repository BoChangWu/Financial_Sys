import pandas as pd
from datetime import datetime ,date
import os
'''
年度開休市檔案下載網址: https://www.twse.com.tw/zh/trading/holiday.html 
需要下載後轉換
'''

class Holiday_Detect():

    def __init__(self):
        # 加上年分
        self.convert_today = date.today().strftime('%Y')

    def deal_holiday(self):

        # 讀取下載的csv檔案, skiprows 如果是[0,4] 則跳過指定的列, 若 = 6 代表跳過 0-6列 
        # utf-8 無法讀檔, 因此使用big5
        print(os.path.isfile('./data/holiday/112.csv'))
        x = pd.read_csv(f'./data/holiday/holidaySchedule_{int(self.convert_today)-1911}.csv',encoding='big5',skiprows=[0])

        # 修改 '                日期' 欄位變成 '日期'
        x.rename(columns={'                日期': '日期'},inplace=True)
        print(x)
        # 針對日期apply 將年分加入原先的日期
        x['日期'] = x['日期'].apply(lambda x : self.convert_today+'年'+x)
        print(x)
        # 把年月日修改成 '/'
        x['日期'] = x['日期'].apply(lambda x: x.replace('年','/'))
        x['日期'] = x['日期'].apply(lambda x: x.replace('月','/'))
        x['日期'] = x['日期'].apply(lambda x: x.replace(' ',''))
        x['日期'] = x['日期'].apply(lambda x: x.replace('"',''))
        x['日期'] = x['日期'].apply(lambda x: x.replace('日',''))
        x['日期'] = x['日期'].apply(lambda x: x[:-2])
        x['日期'] = x['日期'].apply(lambda x: x.replace('(',''))

        # 儲存成excel
        x['日期'].to_csv(f'./data/holiday/holiday_{self.convert_today}.csv',columns=['日期'])

    def is_open(self,now_date:date) -> bool:
        # 規定格式, 年月日間不能有符號

        # 讀取剛剛的休市日期檔
        try:
            hd = pd.read_csv(f'./data/holiday/holiday_{self.convert_today}.csv')
        except:
            self.deal_holiday()
            hd = pd.read_csv(f'./data/holiday/holiday_{self.convert_today}.csv')

        # 轉換為list 備用
        hd_date = pd.to_datetime(hd['日期']).to_list()

        

        # 將日期轉成字串
        str_date = now_date.strftime('%Y%m%d')

        # 使用 weekday 函數判斷星期幾
        day = now_date.weekday()

        if day == 5 or day == 6:
            return False
            

        # Loop 國定假日的 List

        for i in hd_date:
            # 將 Timestamp 類轉為目標日期同樣字串
            i = i.strftime('%Y%m%d')
            # 檢查是否有國定假日跟目標日期一樣, 

        if str_date in hd_date:
            return False

        # 'Y' 代表不符合六日也非國定假日,
        else:
            return True