from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from models import *

SMTP_HOST="localhost"                #setting up the smtp config
SMTP_PORT= 1025
SENDER_EMAIL="admin@email.com"
SENDER_PASSWORD=""




def send_email(to,subject,content_body):  #this is just for sending the mail 
    msg = MIMEMultipart()
    msg["to"]=to
    msg["Subject"]=subject
    msg["from"]=SENDER_EMAIL
    msg.attach(MIMEText(content_body,'html'))
    client=SMTP(host=SMTP_HOST,port=SMTP_PORT)
    client.send_message(msg=msg)
    client.quit()

