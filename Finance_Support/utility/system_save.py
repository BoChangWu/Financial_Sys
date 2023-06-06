import pandas as pd
import os 

def save_csv(data:pd.DataFrame,urls:str) -> bool:

    dir_list = urls.split('/')
    dir_list.pop()
    url = '../data'
    
    for dir in dir_list:

        url += dir

        if not os.path.isdir(url):
            os.mkdir(url)

    try:
        data.to_csv(urls)
    
    except:
        return False
     
    return True




