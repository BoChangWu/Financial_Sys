from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import yfinance as yf
import backtrader as bt
import pyfolio as pf



class Highest(bt.Strategy):
    '''
    追高進場與加碼, 固定停損停利
    '''
    params = (
        
    )

    def log(self,txt,dt=None):
        '''Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        # print('%s,%s' % (dt.isoformat(),txt))

    def __init__(self):

        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

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
        
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        
        self.order = None

    def notify_trade(self,trade):
        if not trade.isclosed:
            return
        
        self.log('OPERATION PROFIT, GROSS: %.2f, NET: %.2f' %
                 (trade.pnl,trade.pnlcomm))
        
    def next(self):
        pass

    # for real trading
    def run(self):
        pass

class MAStrategy(bt.Strategy):

    params = (
        ('fast_period',5),
        ('slow_period',10)
    )

    def log(self,txt,dt=None):
        '''Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        # print('%s,%s' % (dt.isoformat(),txt))

    def __init__(self):
        # 創建收盤價序列備用
        self.dataclose = self.datas[0].close
        # 用於追蹤是否有卡住的訂單以及傭金等
        self.order = None
        self.buyprice = None
        self.buycomm = None
        # 定義5ma 與 60ma
        self.sma1 = bt.ind.SimpleMovingAverage(
            self.datas[0].close, period=self.params.fast_period)
        self.sma2 = bt.ind.SimpleMovingAverage(
            self.datas[0].close, period=self.params.slow_period)
        #使用 bt.ind.CrossOver 方法判斷兩條線的穿越關係
        self.crossover = bt.ind.CrossOver(self.sma1,self.sma2)

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

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        
        self.order = None

    def notify_trade(self,trade):
        if not trade.isclosed:
            return
        
        self.log('OPERATION PROFIT, GROSS: %.2f, NET: %.2f' %
                 (trade.pnl,trade.pnlcomm))

    def next(self):
        
        # Check if an order is pending ... if true, ew cannot send a 2nd one
        if self.order:
            return
        
        # Check if we are in the market
        if not self.position:
            # cross over > 0 意味著向上穿越
            if self.crossover > 0:
                #紀錄買單提交
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                #買進
                self.order = self.buy()
                
        else:
            if self.crossover < 0:
                # 紀錄賣單提交
                    
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                # 賣出
                self.order = self.sell()

    def stop(self):
        print(f'Fast MA: {self.params.fast_period} | Slow MA: {self.params.slow_period} | End Value: {self.broker.getvalue()}')

    def run(self):
        pass

class MAInOut(bt.Strategy):
    '''
    1-5ma 穿越 60ma 進場, 跌破 60ma出場
    '''
    params = (
        
    )

    def log(self,txt,dt=None):
        '''Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        # print('%s,%s' % (dt.isoformat(),txt))

    def __init__(self):

        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

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
        
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        
        self.order = None

    def notify_trade(self,trade):
        if not trade.isclosed:
            return
        
        self.log('OPERATION PROFIT, GROSS: %.2f, NET: %.2f' %
                 (trade.pnl,trade.pnlcomm))
        
    def next(self):
        pass

    # for real trading
    def run(self):
        pass

class MACDMA(bt.Strategy):

    '''
    macd翻紅、ma齊上揚多條件進場
    '''

    params = (
        
    )

    def log(self,txt,dt=None):
        '''Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        # print('%s,%s' % (dt.isoformat(),txt))

    def __init__(self):

        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None

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
        
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        
        self.order = None

    def notify_trade(self,trade):
        if not trade.isclosed:
            return
        
        self.log('OPERATION PROFIT, GROSS: %.2f, NET: %.2f' %
                 (trade.pnl,trade.pnlcomm))
        
    def next(self):
        pass

    # for real trading
    def run(self):
        pass

StrategyBook = {
    'Highest': Highest,
    'MAStrategy': MAStrategy,
    'MAInOut': MAInOut,
    'MACDMA': MACDMA
} 
