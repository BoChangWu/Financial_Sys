import pandas as pd
import yfinance as yf

# yfinance 產出台積電股價資料
stock = yf.Ticker('2330.TW')

# 獲取 2017-01-01 ~ 2023-04-30
df = stock.history(start='2017-01-01',end='2023-04-30')

# rolling 以 6 為單位位移並取最大值
Highest_high = df['High'].rolling(6).max()

# rolling 以 6 為單位位移並取最小值
Lowest_low = df['Low'].rolling(6).min()

df.to_csv('rolling_high_low.csv')

# 用 6根作為 rolling 並且設計計算函數第一個值減去最後一個值
O_C_high = df['High'].rolling(6).apply(lambda x: x[0]-x[-1])

df['OCHIGH'] = O_C_high
df.to_csv('rolling_final.csv')
