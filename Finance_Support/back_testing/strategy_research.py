#%%
import pyfolio as pf
import yfinance as yf
import ta
import pandas as pd
import matplotlib.pyplot as plt

stock = yf.Ticker(f'0056.TW')
return_ser = stock.history(start='2012-01-01',end='2023-06-12')

# 利用pandas 的 pct_change 顯示報酬率變化
pf.create_returns_tear_sheet(return_ser['Close'].pct_change())
# %%
