
from stock import Stock
from datetime import datetime

tsmc = Stock('2330.TW')

tsmc.supervise_price(end_time=datetime(2023,6,5,13,30))