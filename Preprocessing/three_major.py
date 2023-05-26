import requests
import pandas as pd
from datetime import datetime,timedelta

class TMC():
    def __init__(self):
        self.date = datetime.now()
        self.select_type = 'ALLBUT0999'

    def daily_report(self,set_date=None,choose_type=None) -> None:
        '''
        e.g.
        set_date: '20230526'

        '''
        if set_date:
            r_date = set_date
        else:
            r_date = datetime.strftime(self.date-timedelta(days=1),'%Y%m%d')

        if choose_type:
            r_type = choose_type
        else:
            r_type = self.select_type

        res = requests.get(f'https://www.twse.com.tw/rwd/zh/fund/T86?response=json&date={r_date}&selectType={r_type}&_=1685065571229')
        results = res.json()

        df = pd.DataFrame(results['data'],columns=results['fields'])

        print(df)

        df.to_csv(f'TMC_{r_type}_{r_date}.csv')


if __name__ == '__main__':
    
    a = TMC()
    a.daily_report()