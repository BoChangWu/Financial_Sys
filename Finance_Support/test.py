import sys 
import os
import argparse
from Finance_Support.strategy.normal.follow_corp import follow_corp

from Finance_Support.data_fetching.market_data import Market_Data
from Finance_Support.data_fetching.stock import Stock

# follow_corp()

# with_dividend()

# with_devidend_price()
# with_price_fall()

# a = Market_Data()
# stocks = a.read_stock_list()

# for s in stocks:
#     print(s)
#     stock = Stock(str(s)+'.TW')
#     stock.save_history('2014-01-01','2023-06-27')

argParser = argparse.ArgumentParser()
argParser.add_argument('-s','--strategy',help='strategy name')


args = argParser.parse_args()
print('args=%s' % args)
try:
    print('args.strategy=%s' % args.strategy)
    print(type(args.strategy))
except:
    print('dont have this arg')