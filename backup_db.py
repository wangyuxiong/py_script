#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import os
import subprocess
import smtplib, mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

#fileName = ""

def db_bakeup():
    #利用mysqldump 将整个数据库进行备份
    os.chdir("/home/workspace/")
    fileName = "myblog_" + str(time.time())
    cmd = "mysqldump -u metaboy -h 127.0.0.1 -ppasswd  myblog > " + fileName + ".sql"
    subPrjRun = subprocess.Popen(cmd, shell=True)
    while True:
        subPrjRun.poll()
        if subPrjRun.returncode == 0:
            break
    return fileName

def send_mail(fileName):
    msg = MIMEMultipart()
    msg['From'] = "234123806@qq.com"
    msg['To'] = 'yxiong.wang@gmail.com'
    msg['Subject'] = 'email for backup'
    #添加邮件内容  
    txt = MIMEText("这是邮件内容~~")
    msg.attach(txt)

    #添加二进制附件  
    ctype, encoding = mimetypes.guess_type(fileName)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    att1 = MIMEImage((lambda f: (f.read(), f.close()))(open(fileName, 'rb'))[0], _subtype = subtype)
    att1.add_header('Content-Disposition', 'attachment', filename = fileName)
    msg.attach(att1)

     #发送邮件  ，QQ邮箱必须得开通SMTP
    smtp = smtplib.SMTP()
    smtp.connect('smtp.qq.com:25')
    smtp.login('QQ号', '密码')
    smtp.sendmail('234123806@qq.com', 'yxiong.wang@gmail.com', msg.as_string())
    smtp.quit()
    print '邮件发送成功'


if __name__ == "__main__":
    fileName = db_bakeup()
    print fileName
    os.chdir("/home/workspace/")
    tar_cmd = "tar -cvf" + fileName + ".tar " + fileName+".sql"
    print tar_cmd
    os.system(tar_cmd)
    tar_file = fileName + ".tar"
    send_mail(tar_file)
