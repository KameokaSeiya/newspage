import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from bs4 import BeautifulSoup
import requests
import json 
import schedule
import time

def create_message(from_addr, to_addr, bcc_addrs, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Bcc'] = bcc_addrs
    msg['Date'] = formatdate()
    return msg

def send(from_addr, to_addrs, msg, my_password):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587) # GmailのSMTPサーバーへ
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(from_addr, my_password)
    smtpobj.sendmail(from_addr, to_addrs, msg.as_string())
    smtpobj.close()
    

def job():
    
    with open('secret.json') as f:
        info = json.load(f)
        
    FROM_ADDRESS = info['email']
    MY_PASSWORD = info['password']
    
    TO_ADDRESS = 's.kameoka.227@ms.saitama-u.ac.jp '
    BCC = ''
    SUBJECT = 'webpage 更新'
    BODY = '変化なし'
    msg = create_message(FROM_ADDRESS, TO_ADDRESS, BCC, SUBJECT, BODY)
    send(FROM_ADDRESS, TO_ADDRESS, msg, MY_PASSWORD)
    
def detect_update():
    url='http://www.saitama-u.ac.jp/'
    res=requests.get(url)

    soup=BeautifulSoup(res.text,'html.parser')
    new_elem=str(soup.select('.mtx.line.news'))

    try:
        with open('old_elem.txt')as f:
            old_elem=f.read()
    except:
        old_elem=''

    if new_elem==old_elem:
        print('変化なし')
        job()
        return False
    else:
        with open('old_elem.txt','w')as f:
            f.write(new_elem)
        print('webページが更新された') 
        return True
    
def main():
    schedule.every(10).seconds.do(detect_update)
    print('処理を開始')
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    #job()
   main()