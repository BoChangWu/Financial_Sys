import pandas as pd
import os 

def save_csv(data:pd.DataFrame,urls:str) -> bool:

    dir_list = urls.split('/')
    dir_list.pop()
    root = './data' 
    url = './data'
    
    for dir in dir_list:

        url = url+ '/'+dir

        if not os.path.isdir(url):
            os.mkdir(url)

    try:
        data.to_csv(root+'/'+urls)
    
    except Exception as e:
        print(str(e))
        return False
     
    return True




