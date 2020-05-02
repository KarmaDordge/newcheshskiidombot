import telebot

import word
import time
import sqlite3
import ema

bot = telebot.TeleBot(token='1117846624:AAGTxBpQMOWCHAP3Uk-CX6a3i9yPqoy-3Rg', threaded=False)


conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()
filedb =[]
sql = "SELECT File_id,text FROM image"



for i in cursor.execute(sql):
    filedb.append(i)

keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('О нас \U0001F3EC', 'Ассортимент \U0001F6CD', 'Оставить заявку \U0001F4C3', 'Новинки \U0001F195', 'Помощь \U00002753')
keyboard2 = telebot.types.ReplyKeyboardMarkup(True)
keyboard2.row('Узнать стоимость', 'Оформить заказ', 'Отмена')
keyboard3 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard3.row('Доставка', 'Самовывоз')
@bot.message_handler(commands=["start"])
def start(message):
    
    bot.send_video(message.chat.id, 'BAACAgIAAxkBAAMWXqpfvebl-4zMxT0sirHi5r6vJZUAAtgGAAIj4FBJhqiVxulPW0AZBA')
    bot.send_message(message.chat.id, word.about, reply_markup=keyboard1)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'о нас \U0001F3EC':
        markup = telebot.types.InlineKeyboardMarkup()
        yamap= telebot.types.InlineKeyboardButton(text='Яндекс-карта', url='https://yandex.ru/maps/-/CSaORAML')
        gglmap= telebot.types.InlineKeyboardButton(text='Google карты', url='https://maps.app.goo.gl/7s9Mm9j31xTeiS749')
        markup.add(yamap, gglmap)
        bot.send_message(message.chat.id, word.adress, reply_markup=markup)
    elif message.text.lower() == 'помощь \U00002753':
        bot.send_message(message.chat.id, word.faq) 
    elif message.text.lower() == 'ассортимент \U0001F6CD':
        media=[]
        for i in range(0,5):
            media.append(telebot.types.InputMediaPhoto(filedb[i][0], filedb[i][1] ))
        bot.send_media_group(message.chat.id, media) 
        bot.send_message(message.chat.id, 'Пожалуйста, выберете нужное:',reply_markup=keyboard2)
        bot.register_next_step_handler(message, get_neworder)
    elif message.text.lower() == 'новинки \U0001F195':
        media=[]
        for i in range(5,10):
            media.append(telebot.types.InputMediaPhoto(filedb[i][0], filedb[i][1] ))
        bot.send_media_group(message.chat.id, media)
        bot.send_message(message.chat.id, 'Пожалуйста, выберете нужное:',reply_markup=keyboard2)
        bot.register_next_step_handler(message, get_neworder)
    elif message.text.lower() == 'оставить заявку \U0001F4C3':
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.row('Физическое лицо', 'Организация')
        bot.send_message(message.chat.id, 'Пожалуйста, выберете нужное:', reply_markup=keyboard)
        bot.register_next_step_handler(message, get_status)




def get_neworder(message):
    if message.text.lower() == 'оформить заказ':
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.row('Физическое лицо', 'Организация')
        bot.send_message(message.chat.id, 'Пожалуйста, выберете нужное:', reply_markup=keyboard)
        bot.register_next_step_handler(message, get_status)
    elif  message.text.lower() == 'отмена':
        bot.send_message(message.chat.id, 'главное мэню', reply_markup=keyboard1)
    else:
        bot.send_document(message.chat.id, open('1.xlsx','rb'), reply_markup=keyboard1)

def get_status(message):
    global status
    status = message.text
    if status == 'Физическое лицо':
        bot.send_message(message.chat.id, 'Пожалуйста напишите Ваше Имя и Фамилию:')
        bot.register_next_step_handler(message, get_name)
    elif status == 'Организация':
        bot.send_message(message.chat.id, 'Пожалуйста, напишите название организации:')
        bot.register_next_step_handler(message, get_name_organization)

def get_name_organization(message):
    global name_organization
    name_organization = message.text
    bot.send_message(message.chat.id, 'Пожалуйста, напишите ИНН покупателя:')
    bot.register_next_step_handler(message, get_inn)

def get_inn(message):
    global inn
    inn = message.text
    bot.send_message(message.chat.id, 'Спасибо! Напишите, пожалуйста, ФИО получателя товара:')
    bot.register_next_step_handler(message, get_name2)

def get_name2(message):
    global name
    global patronymic
    global surname
    name, patronymic, surname = message.text.split()
    bot.send_message(message.chat.id, 'Отлично! Напишите, пожалуйста, ИНН получателя товара:')
    bot.register_next_step_handler(message, get_inn2)

def get_inn2(message):
    global inn2
    inn2 = message.text
    bot.send_message(message.chat.id, 'Теперь, пожалуйста, телефон получателя товара:')
    bot.register_next_step_handler(message, get_phone)


def get_name(message):
    global name
    global surname
    s = message.text
    name, surname = s.split()   
    bot.send_message(message.chat.id, 'Выберите способ получения товара:', reply_markup=keyboard3)
    bot.register_next_step_handler(message, get_delivery)

def get_delivery(message):
    global delivery
    delivery = message.text
    if message.text.lower() == 'доставка':
        bot.send_message(message.chat.id, name + ', очень приятно. Напишите мне, пожалуйста, адрес доставки в формате: ГОРОД, УЛИЦА, ДОМ')
        bot.register_next_step_handler(message, get_addres)
    elif message.text == 'Самовывоз':
        bot.send_message(message.chat.id, name + ', напишите Ваш номер телефона,☎️ пожалуйста:')
        bot.register_next_step_handler(message, get_phone)

def get_addres(message):
    global city
    global street
    global house
    if delivery == 'Доставка' and status == 'Физическое лицо':
        city, street, house = message.text.split(',')
        bot.send_message(message.chat.id, name + ', напишите Ваш номер телефона,☎️ пожалуйста:')
        bot.register_next_step_handler(message, get_phone)
    elif status == 'Организация':
        bot.send_message(message.chat.id, 'Напишите пожалуйста количество товара и наименование товара:')
        bot.register_next_step_handler(message, get_order)



def get_phone(message):
    global phone
    phone = message.text
    if status == 'Организация':
        bot.send_message(message.chat.id, 'Выберите способ получения товара:', reply_markup=keyboard3)
        bot.register_next_step_handler(message, get_delivery)
    else:
        bot.send_message(message.chat.id, 'Напишите пожалуйста количество товара и наименование товара:')
        bot.register_next_step_handler(message, get_order)

def get_order(message):
    global order
    order = message.text
    if delivery == 'Доставка':
        bot.send_message(message.chat.id, 'Осталось совсем немного. Напишите дату и время доставки в любой форме, пожалуйста:')
        bot.register_next_step_handler(message, get_time)
    else:
        bot.send_message(message.chat.id, 'Осталось совсем немного. Напишите дату и время когда Вы хотите забрать товар, в любой форме,пожалуйста:')
        bot.register_next_step_handler(message, get_finish)


def get_time(message):
    global time
    time = message.text
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('Пропустить комментарий')
    bot.send_message(message.chat.id, 'Укажите особенности заезда или комментарии', reply_markup=keyboard)
    bot.register_next_step_handler(message, get_comment)

def get_comment(message):
    global comment
    if message.text == 'Пропустить комментарий':
        comment = None
    else:
        comment = message.text
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.row('Отправить','Отменить')
    bot.send_message(message.chat.id, 'Подтверждение заказа', reply_markup=keyboard)
    bot.register_next_step_handler(message, get_finish)

def get_finish(message):
    global timenot
    if message.text == 'Отправить':
        ema.elecmail(delivery, city, street, house, phone, order, time, comment, name, surname)
        bot.send_message(message.chat.id, 'Заказ подтвержден', reply_markup=keyboard1)
    elif message.text == 'Отменить':
        bot.send_message(message.chat.id, 'Заказ отменен', reply_markup=keyboard1)
    elif delivery == 'Самовывоз':
        timenot = message.text
        bot.send_message(message.chat.id, 'Заказ подтвержден', reply_markup=keyboard1)




while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=123)
    except Exception as E:
        print(E.args)

       