import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}


class Stock():

    def __init__(self,headers,stock_id):

        self.headers = headers
        self.stock_id = stock_id

    def price(self):

        data = requests.get(f'https://finance.yahoo.com/quote/{self.stock_id}?p={self.stock_id}',headers=self.headers) 

        soup = BeautifulSoup(data.text)

        price = soup.find("fin-streamer",{"data-test":"qsp-price"})
        # <fin-streamer class="Fw(b) Fz(36px) Mb(-4px) D(ib)" data-symbol="2330.TW" data-test="qsp-price" data-field="regularMarketPrice" data-trend="none" data-pricehint="2" value="505" active="">505.00</fin-streamer>

        print(price.text)
if __name__ == '__main__':

    a =  Stock(headers,'2330.TW')
    a.price()
    