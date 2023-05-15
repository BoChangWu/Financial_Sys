import requests
import pandas as pd
from io import StringIO
import os
import time

# 為了讓目標server 將腳本視為瀏覽器
headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }

res = requests.get("https://isin.twse.com.tw/isin/C_public.jsp?strMode=2",headers=headers)

# 將 
data = pd.read_html(res.text)

data = data[0]

print(data)
# 指定 df 的欄位為第一列
data.columns = data.iloc[0,:]

# 拿掉本來的那一列以及都是股票的那一列
data = data.iloc[1:,:]
print(data)

# 將股票名稱與代號分割開
data['代號'] = data['有價證券代號及名稱'].apply(lambda x: x.split()[0])

data['股票名稱'] = data['有價證券代號及名稱'].apply(lambda x: x.split()[-1])

# 利用 to_datetime 把無法轉成datetime 的資料化為Nan
data['上市日'] = pd.to_datetime(data['上市日'], errors='coerce')

# 再把上市日 = Nan 的資料去掉篩選掉非股票的雜質
# data = data.dropna(sebset = ['上市日'])
data.dropna(subset=['上市日'])

data.dropna(subset=['產業別'])
# 去掉不需要的欄位
print(data.columns)

data = data.drop(['有價證券代號及名稱','國際證券辨識號碼(ISIN Code)','CFICode','備註'], axis=1)

# 更換剩餘欄位順序
data = data[['代號','股票名稱','上市日','市場別','產業別']]

data = data[data['代號'].str.isdigit()]

print(data)
data.to_csv('./stock_list.csv')
