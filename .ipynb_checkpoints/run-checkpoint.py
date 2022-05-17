import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
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
    SUBJECT = '自動実行環境構築練習'
    BODY = 'これは練習です。'
    msg = create_message(FROM_ADDRESS, TO_ADDRESS, BCC, SUBJECT, BODY)
    send(FROM_ADDRESS, TO_ADDRESS, msg, MY_PASSWORD)
    
    
def main():
    schedule.every(5).seconds.do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()