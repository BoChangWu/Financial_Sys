import pandas as pd
import yfinance as yf
import ta
import mpl_finance as mpf
import matplotlib.pyplot as plt
from datetime import datetime

'''
通常實際作圖都是使用 Power BI 或 Tableu , python 做資料分析後再將資料給他們作圖
'''

# yfinance 產出台積電股價資料
stock = yf.Ticker('2330.TW')

# 獲取 2017-01-01 ~ 2023-05-01
df  = stock.history(start='2017-01-01',end='2023-05-01')


indicator_bb = indicator_bb = ta.volatility.BollingerBands(close=df['Close'],window=20,window_dev=2)

# 布林中線
df['bbm'] = indicator_bb.bollinger_mavg()

# 布林上線
df['bbh'] = indicator_bb.bollinger_hband()

# 布林下線
df['bbl'] = indicator_bb.bollinger_lband()

# 創建畫布, 其中figsize 代表畫布大小, 有預設值
fig = plt.figure(figsize=(24,8))

# 定義模板大小 3*20
grid = plt.GridSpec(3,20)

# # add_subplot(x,y,z) x 代表橫向切割區塊數, y 代表直向切割區塊數, z 代表切割後區塊的index
# ax = fig.add_subplot(1,1,1)
# 區塊一畫主圖, 給兩個空間並左方保留一格 -> K線
ax = fig.add_subplot(grid[0:2,1:])
# 區塊二畫子圖, 給一個空間並左方保留一格 -> 成交量
ax2= fig.add_subplot(grid[2,1:])


# 使用 mpl_finance 的 candlestick2_ochl 函數, 傳入畫布加上OCHL值
mpf.candlestick2_ochl(ax,df['Open'],df['Close'],df['High'],df['Low'],width=0.6,colorup='r',colordown='g',alpha=0.75)

# 使用 mpl.volume_overlay 畫出成交的量
mpf.volume_overlay(ax2,df['Open'],df['Close'],df['Volume'],colorup='r',colordown='g')

# 將原本的時間美化, 每個30天一個刻度 + 小函數轉換日期
convert_date = pd.DataFrame(df.index[::30])['Date'].apply(lambda x: x.strftime('%Y/%m/%d'))
# 設置ax 區塊刻度
ax.set_xticks(range(0,len(df.index),30)) # range第三個參數為間隔
# 設置ax中的刻度的值
ax.set_xticklabels(convert_date,rotation=45,fontsize=6)

# ax 區塊加上布林上中下線
ax.plot(df['bbm'].values, color='b',label='bbm',linewidth=1.0)
ax.plot(df['bbh'].values,color='g',label='bbh',linewidth=1.0)
ax.plot(df['bbl'].values,color='r',label='bbl',linewidth=1.0)

# 設置ax2 的刻度
ax2.set_xticks(range(0,len(df.index),30))
# 設置 ax2 刻度的值
ax2.set_xticklabels(convert_date,rotation=45,fontsize=6)

# 設置ax圖片標題
ax.set_title(f'2330 Stock Price')

# 設置x軸名稱為Date
ax.set_xlabel('Date')
# 設置y軸名稱為 Price
ax.set_ylabel('Price')

# 防止重疊
fig.tight_layout()

# 設置legend 才會有label 跑出來
plt.legend(loc='best')
# 存成png
plt.savefig('test.png')
plt.show()


