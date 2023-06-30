#%%
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import yfinance as yf
import backtrader as bt
import pyfolio as pf

class TestStrategy(bt.Strategy):

    params = (
        ('maperiod',15),
        )

    def log(self,txt,dt=None):
        '''Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s,%s' % (dt.isoformat(),txt))

    def __init__(self):
        # 創建收盤價序列備用
        self.dataclose = self.datas[0].close
        # 官方範例, 用於追蹤是否有卡住的訂單以及傭金等
        self.order = None
        self.buyprice = None
        self.buycomm = None
        # 官方範例, 新增一個 15ma 的資料序列備用
        self.sma = bt.indicators.SmoothedMovingAverage(
            self.datas[0], period=self.params.maperiod)
        
        

    def notify_order(self,order):
        '''追蹤訂單狀態, 只在訂單完成買入時執行'''
        if order.status in [order.Submitted,order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothin to do
            return
        
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm: %.2f' % 
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
                
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                # Sell
                self.log(
                    'SELL EXECUTED, Price: %.2f, Cost: %.2f,Comm: %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))
            
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        
        self.order = None

    def notify_trade(self,trade):
        if not trade.isclosed:
            return
        
        self.log('OPERATION PROFIT, GROSS: %.2f, NET: %.2f' %
                 (trade.pnl,trade.pnlcomm))

    def next(self):
        
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])
        # Check if an order is pending ... if true, ew cannot send a 2nd one
        if self.order:
            return
        
        # Check if we are in the market
        if not self.position:
            # Not yet .. we MIGHT BUY if ...
            if self.dataclose[0] > self.sma[0]:
                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
            else:
                if self.dataclose[0] < self.sma[0]:
                    # SELL, SELL, SELL!!(with all possible default parameters)
                    self.log('SELL CREATE, %.2f' % self.dataclose[0])
                    # Keep track of the created order to avoid a 2nd order
                    self.order = self.sell()

#%%
if __name__ == '__main__':

    # Create a cerebro entity
    cerebro = bt.Cerebro()
    # Add a strategy
    cerebro.addstrategy(TestStrategy)

    # 因為沒有官方準備好的資料, 所以官方範例中的 modpath 跟 datapath 拿掉,  
# Create Data Feed with YahooFinanceData Function
    data = bt.feeds.PandasData(
        dataname = yf.download('2379.TW',start='2014-01-01',end='2022-12-31'))
    
    # print(yf.download('2379.TW',start='2014-01-01',end='2022-12-31'))
    
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

    strat= results[0]
    pyfoliozer = strat.analyzers.getbyname('pyfolio')
    returns, positions, transactions,gross_lev = pyfoliozer.get_pf_items()

    # pf show time
    pf.create_full_tear_sheet(
        returns,
        positions=positions,
        transactions=transactions,
        live_start_date= '2018-01-01') # This date is sample specific
    

    

    





# %%
