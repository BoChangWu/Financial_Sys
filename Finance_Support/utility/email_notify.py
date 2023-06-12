import sys
sys.path.append('./')
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from Finance_Support.utility.AES_Encryption.encrype_process import *

from Finance_Support.utility.settings import key_path,config_path

#決定金鑰跟config檔位置


def smtp(send_from:str,to_list:list,subject:str,body:str,mode='text',file_path=None,file_name=None) -> None:

    # 檢查相關路徑
    if not os.path.isdir('./data/auth'):
        os.mkdir('./data/auth')
    if not os.path.isdir(key_path):
        os.mkdir(key_path)
    if not os.path.isdir(config_path):
        os.mkdir(config_path)

    # 引用加解密的主要程式 check_encrype
    user_id,pwd = check_encrype('gmail',key_path,config_path)


    msg = MIMEMultipart()

    #對它傳入三個基本資訊: 寄件者(From)、收件者(To)、標題(Subject)
    msg['From'] = user_id
    # 'j2223334555@gmail.com'
    # 寄件名單轉成list
    # msg['To'] = 'jasonfubon0411@gmail.com'
    
    msg['To'] = ",".join(to_list)

    msg['Subject'] = subject

    msg.attach(MIMEText(body,mode))

    
    if file_path:
    # 讀取圖片檔為byte
        with open(file_path,'rb') as opened:
            openfile = opened.read()

            # 呼叫 MIMEApplication 並放入byte 類型
            attached_file = MIMEApplication(openfile)

            attached_file.add_header('content-disposition','attachment',filename=file_name)

            # 跟上面attach 信件內容一樣, 把附檔資訊也attach 進去
            msg.attach(attached_file)

    # 設定smtp server, 以gmail 為例 需與官方資訊一模一樣
    server = smtplib.SMTP('smtp.gmail.com',587)

    # 需要先連線
    server.connect('smtp.gmail.com',587)
    # TLS 安全傳輸設定
    server.starttls()

    # 登入gmail帳號
    # server.login('j2223334555@gmail.com',my_gmail_pwd)

    server.login(user_id,pwd)
    # msg 是 MIMEMultipart class 將它轉為send mail 可接受的字串
    text= msg.as_string()

    # 指定寄件者與收件者, 還有剛剛加的信件內容, 標題, 附檔等資訊
    server.sendmail(send_from,to_list,text)

    # 斷線
    server.quit()