import ta
import yfinance as yf

stock = yf.Ticker('2330.TW')

df  = stock.history(start='2017-01-01',end='2023-02-02')

# add_all_ta_features 即可呼叫出所有技術指標
data = ta.add_all_ta_features(df,"Open","High","Low","Close","Volume",fillna=True)

print(data)

# ta移動平均 產生單一指標, 以移動平均為例

ma = ta.trend.SMAIndicator(df['Close'],10,fillna=True)
ma = ma.sma_indicator()

print(ma)

# ta 布林通道

indicator_bb = ta.volatility.BollingerBands(close=df['Close'],window=20,window_dev=2,fillna=True)

# 布林中線
bb_bbm = indicator_bb.bollinger_mavg()
print(bb_bbm)

# 布林上線
bb_bbh = indicator_bb.bollinger_hband()
print(bb_bbh)

# 布林下線
bb_bbl = indicator_bb.bollinger_lband()
print(bb_bbl)

# 回傳 Close 是否大於布林上軌, 是為 1 , 否則為 0
bb_bbhi = indicator_bb.bollinger_hband_indicator()
print(bb_bbhi)

# 回傳 Close 是否小於布林下軌, 是為 1 , 否則為 0
bb_bbli = indicator_bb.bollinger_lband_indicator()
print(bb_bbli)

# 布林帶寬
bb_bbw = indicator_bb.bollinger_wband()
print(bb_bbw)

# 布林%b 指標( %b值 = (收盤價 布林帶下軌值) / (布林帶上軌值 布林帶下軌值))
bb_bbp = indicator_bb.bollinger_pband()
print(bb_bbp)



