from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt

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
        '''追蹤訂單狀態'''
        pass

    def notify_trade(self,trade):
        pass

    def next(self):
        pass
    
