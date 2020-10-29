import datetime
import telebot
import time
from validate_email import validate_email
from telebot import types
import smtplib
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import math
bot = telebot.TeleBot('')# your token


db_file = 'db.db'
db = sqlite3.connect(db_file)

now = datetime.datetime.now()
a = str(now.day) + str(now.month)+str(now.year) +str(0)+str(0)
b= int(a)
d = b
f = open('text.txt', 'r+')
s = int(float(str(f.read()))) # current id
if b <= s:
    b=s
    b+=1
c=str(b)
f.seek(0)
f.write(str(c))
f.truncate()

inc_type = []  
nm_type = [] 
cli_num = []  
cli_mail = []  
hello_count = [] 
ms_det=[]
name = []

@bot.message_handler(commands=['start'])
def statup(message):
    if len(hello_count) == 0:
        bot.send_message(message.chat.id, 'Hi I am your bot.\n To use me type /services')
    hello_count.insert(1, 1)
@bot.message_handler(commands=['info'])
def statup1(message):
    bot.send_message(message.chat.id, 'Please contact me for full information. @wittles')
@bot.message_handler(commands=['services'])
def mark(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.add('Проектирование')
    keyboard.add('Промышленная кибербезопасность')
    keyboard.add('Поставки')
    keyboard.add('Сборка под заказ')
    keyboard.add('Монтаж и пуско-наладка')
    keyboard.add('Техническое обслуживание')
    keyboard.add('Управляемые услуги')
    keyboard.one_time_keyboard = True
    bot.send_message(message.chat.id,'Выберите услугу', reply_markup=keyboard)
    bot.register_next_step_handler(message, name_check)

def name_check(message):
    bot.send_message(message.chat.id, 'Please type your full name ⤵')
    bot.register_next_step_handler(message, mail_check)
    nm_type.append(message.text)

def mail_check(message):  # Функция ввода почты
    bot.send_message(message.chat.id, 'Please type your e-mail  ⤵')
    bot.register_next_step_handler(message, mail_check2)
    name.append(message.text)


def mail_check2(message):  # Проверка потчы на валидность
    is_valid = validate_email(message.text)
    if is_valid:
        bot.send_message(message.chat.id, "Your e-mail is correct.")
        cli_mail.append(message.text)  # Записываем полученную почту
        bot.send_message(message.chat.id, 'Please type your phone number, so we can contact you. Here an example\n 87478884488')
        bot.register_next_step_handler(message, phone_check)
    else:
        bot.send_message(message.chat.id, "Your e-mail is not correct.")
        mail_check(message)

def phone_check1(message):
    bot.send_message(message.chat.id, 'Please type your phone number')
    bot.register_next_step_handler(message, phone_check)

def phone_check(message):
    if len(message.text) == 11:
        bot.send_message(message.chat.id, "Your number is correct.")
        cli_num.append(message.text)
        details(message)
    else:
        bot.send_message(message.chat.id, "Your number is not correct.")
        phone_check1(message)

def details(message):
    bot.send_message(message.chat.id, "Give some details for project")
    ms_det.append(message.text)

    bot.register_next_step_handler(message, res)
f.close
det ="" #detali producta
def res(message):
    det = message.text
    bot.send_message(message.chat.id, "Your application is accepted and will be number №{0}. \nДо скорых встреч!".format(b))
    add_db(db, message.from_user.id, det)

# det = detali, name = ФИО, cli_mail = почта, cli_num = номер, nm_type = услуга, b = номер заказа

def add_db(db, user_id, det):
    with sqlite3.connect("db.db") as con:
        info = (user_id, nm_type[-1], name[-1], cli_mail[-1], cli_num[-1], det, b)
        sql = """ INSERT INTO  Zakazy(user_id, usluga, FIO, mail, cli_number, details, id_zakaz) 
        VALUES(?,?,?,?,?,?,?) """
        cur = con.cursor()
        cur.execute(sql, info)
        return cur.lastrowid



while True:  # Запускаем бота
    try:
        bot.polling(none_stop=True)
    except OSError:
        bot.polling(none_stop=True)