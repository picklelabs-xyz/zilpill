import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import src.CONF as CONF
import os
from dotenv import load_dotenv

load_dotenv()
personal_env = os.getenv(CONF.PERSONAL_ENV_FILE)
load_dotenv(personal_env)

def mail_it(subject, txt_msg, from_name, from_pwd, from_mail, to_mails):
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(from_mail, from_pwd)
    for email in to_mails:
        msg = MIMEMultipart()
        msg['From'] = from_name
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(txt_msg, 'plain'))
        s.send_message(msg)
        del msg
    s.quit()


if __name__ == '__main__':
    e_subject = "SUBJECT"
    e_msg = "MSG"
    e_from_name = "FROM_NAME"
    e_from_mail = os.getenv(CONF.EMAIL_1)
    e_from_pwd = os.getenv(CONF.EMAIL_1_PASSWORD)
    e_to_mails = [os.getenv(CONF.EMAIL_1)]
    mail_it(e_subject, e_msg, e_from_name,
            e_from_pwd, e_from_mail, e_to_mails)
