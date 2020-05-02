
import smtplib
from asyncio import coroutine
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

@coroutine
def elecmail(delivery, city, street, house, phone, order, time, comment, name, surname):
    fromaddr = "cheshskiy.dom@bk.ru"
    toaddr = "cheshskiy.dom@bk.ru"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Test Subject"
    body = ((
    "ФИО %s" % name + ' ' + surname,
    "Способ доставки: %s" % delivery ,
    "Адрес доставки: %s" % city + ' ,' + street + ' ,'+ house,
    "Телефон: %s" % phone,
    "Заказ: %s" % order,
    "Время доставки: %s" % time,
    "Коментарий: %s" % comment,
    ))
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP_SSL('smtp.mail.ru:465')
    server.set_debuglevel
    server.login(fromaddr, "product2020")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

if __name__ == '__main__':
    LOOP = get_event_loop()
    result = LOOP.run_until_complete(elecmail())
    print(result)

