from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import argparse
# Import the backtrader platform
import yfinance as yf
import backtrader as bt
import pyfolio as pf

from Finance_Support.strategy.technical_indicators import *

# 讀取 指令所給的參數
argParser = argparse.ArgumentParser()
argParser.add_argument('-s','--strategy',help='strategy name')


args = argParser.parse_args()
print('args=%s' % args)
try:
    my_strategy = args.strategy
    print('args.strategy=%s' % my_strategy)
# 若沒有給 strategy 則離開
except:
    print('dont have this arg')
    exit()


# Create a cerebro entity
cerebro = bt.Cerebro()
# Add a strategy
cerebro.addstrategy(StrategyBook[my_strategy])

# 因為沒有官方準備好的資料, 所以官方範例中的 modpath 跟 datapath 拿掉,  
# Create Data Feed with YahooFinanceData Function
data = bt.feeds.PandasData(
    dataname = yf.download('2379.TW',start='2014-01-01',end='2022-12-31'))



# Add the Data Feed to Cerebro | 
#傳入 data feed
cerebro.adddata(data)
# Set our deired cash start | 設置初始資金
cerebro.broker.setcash(1000000.0)
# Add a FixSize sizer according to the stake | 每一次下單的股數
cerebro.addsizer(bt.sizers.FixedSize,stake=1000)

# Set the commission
cerebro.broker.setcommission(commission=0.0015)
cerebro.addanalyzer(bt.analyzers.PyFolio,_name='pyfolio')
# Print out the starting conditions
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
# Run over everthing
results = cerebro.run()


# Print out the final result
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

## 以下是分析工具, 需要 Run Cell 才可執行, 需另尋方法
# strat= results[0]
# pyfoliozer = strat.analyzers.getbyname('pyfolio')
# returns, positions, transactions,gross_lev = pyfoliozer.get_pf_items()


# pf show time
# pf.create_full_tear_sheet(
#     returns,
#     positions=positions,
#     transactions=transactions,
#     live_start_date= '2018-01-01') # This date is sample specific


    

    

