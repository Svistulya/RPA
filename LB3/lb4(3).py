'''
Г, А, Б, В, Г
Вариант Г: Mail.ru (через SMTP/IMAP)
Вариант А: Простое текстовое письмо
Вариант Б: Чтение данных из CSV-файла
Вариант В: Поиск писей с вложениями
Вариант Г: Переслать письмо другому адресату

'''
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import os
from datetime import datetime

EMAIL = "vhbuc@mail.ru"          
APP_PASSWORD = "y7vohzPx6N3bYHjuxKlg"  
IMAP_SERVER = "imap.mail.ru"
SMTP_SERVER = "smtp.mail.ru"
SMTP_PORT = 587

TARGET_EMAIL = "vhbuc@mail.ru"  
CSV_FILE = "получатели.csv"              


def send_simple_email(to_email, subject="Тестовое письмо", body="hjkhjhjkjkhjkhkj"):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, APP_PASSWORD)
            server.sendmail(EMAIL, to_email, msg.as_string())
        
    except Exception as e:
        print("Ошибка")


def read_emails_from_csv(filename):
    try:
        df = pd.read_csv(filename, encoding="utf-8")
        emails = df["Email"].dropna().tolist()
        return emails
    except Exception as e:
        return []

def find_emails_with_attachments():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, APP_PASSWORD)
        mail.select("INBOX")

        
        status, messages = mail.search(None, 'HEADER Content-Disposition attachment')
        if status != "OK":
            print("Нет писем с вложениями")
            return []

        email_ids = messages[0].split()
        return email_ids[-5:]
    except Exception as e:
        print("Ошибка")
        return []
    finally:
        try:
            mail.logout()
        except:
            pass

def forward_email(email_id, to_email):
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, APP_PASSWORD)
        mail.select("INBOX")

        status, msg_data = mail.fetch(email_id, "(RFC822)")
        if status != "OK":
            return

        raw_email = msg_data[0][1]
        original_msg = email.message_from_bytes(raw_email)

      
        forwarded = MIMEMultipart()
        forwarded["Subject"] = "Fwd: " + (original_msg["Subject"] or "Без темы")
        forwarded["From"] = EMAIL
        forwarded["To"] = to_email

       
        body = MIMEText("Пересланное письмо:\n\n", "plain", "utf-8")
        forwarded.attach(body)

        forwarded.attach(MIMEText(original_msg.as_string(), "plain", "utf-8"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, APP_PASSWORD)
            server.sendmail(EMAIL, to_email, forwarded.as_string())
    finally:
        try:
            mail.logout()
        except:
            pass


if __name__ == "__main__":
    emails = read_emails_from_csv(CSV_FILE)
    for addr in emails[:2]:  
        send_simple_email(addr)
    attachment_emails = find_emails_with_attachments()

    if attachment_emails:
        forward_email(attachment_emails[0], TARGET_EMAIL)
