import time
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header

import schedule
from bs4 import BeautifulSoup


def get_url():
    url = 'https://yzb.bupt.edu.cn/list/list.php?p=2_1_1'
    r = requests.get(url=url)
    soup = BeautifulSoup(r.text, 'lxml')
    links = soup.find_all('a', class_="lh28 h28")
    main_url = 'https://yzb.bupt.edu.cn'
    url_list = []
    for link in links:
        a = link['href']
        url_list.append(main_url + a)
    return url_list


def get_content():
    title_list = []
    for url in get_url():
        r = requests.get(url=url)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'lxml')
        title = soup.find('title').text
        pub_data = soup.find('div', class_="time").text[5:15]
        # print(pub_data)
        preciseTime = soup.find("div", class_="time").text
        info_text = soup.find("div", class_="aticle pad10").text
        current_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        # current_time = time.strftime('2021-04-23', time.localtime(time.time()))
        if pub_data == current_time:
            # print(preciseTime)
            title_list.append("详情点击： " + url + "\n  " + info_text)

    if len(title_list) == 0:
        sent_email(mail_body='今天没有通知哦。')
    else:
        for title in title_list:
            sent_email(mail_body=title)
    title_list.clear()


def sent_email(mail_body):
    sender = 'hds_2020@163.com'
    receiver = 'hds_2020@163.com'
    smtpServer = 'smtp.163.com'
    username = 'hds_2020@163.com'
    password = 'LEZJTVWLYBDZBRQI'
    mail_title = '北邮通知公告'
    mail_body = mail_body

    message = MIMEText(mail_body, 'plain', 'utf-8')
    message["Accept-Language"] = "zh-CN"
    message["Accept-Charset"] = "ISO-8859-1,utf-8"
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = Header(mail_title, 'utf-8')

    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtpServer)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver, message.as_string())
        print('邮件发送成功')
        smtp.quit()
    except smtplib.SMTPException:
        print("邮件发送失败！！！")


get_content()

# schedule.every().days.at("22:00").do(get_content)
# while True:
#     schedule.run_pending()
#     time.sleep(1)

