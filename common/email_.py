#email_.py
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header

with open('config.json', 'r') as f:
    config = json.load(f)
from_addr = config['sAccount']
from_pw = config['sPassword']
to_addr = config['rAccount']
smtp_server = 'smtp-mail.outlook.com'
smtp_port = 25

def send_email(html, subject):
    print('发送邮件中 ...')
    msg = MIMEText(html, 'html', 'utf-8')
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = Header(subject, 'utf-8').encode()
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(from_addr, from_pw)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
        print('邮件发送成功!')
        return True
    except:
        print('邮件发送失败...')
        return False
