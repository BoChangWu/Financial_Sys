import yfinance as yf

# 指定股票代號
stock = yf.Ticker('2330.TW')

# 獲取指定區間的歷史報價
df = stock.history(start='2023-01-01',end='2023-05-25')

print(type(df))
print(df)
# 獲取其擁有的所有區間的歷史報價
df = stock.history(period='max')
print(type(df))
print(df)

# 股票基本資訊
df_info = stock.info

print(df_info)

# 內部人士與機構法人持有比例
major_holders = stock.major_holders
print(major_holders)

# 主要持有的機構法人
ins_holders = stock.institutional_holders
print(ins_holders)

# 取得損益表
fin_data = stock.financials
print(fin_data)

# 取得資產負債表
balance_data = stock.balance_sheet
print(balance_data)

# 現金流量表 
# 現金流量表讀取又問題, 需嘗試用爬蟲解決或查詢此問題修正方法
cf_data = stock.cash_flow
print(cf_data)

# 分析師推薦
recommands = stock.recommendations

