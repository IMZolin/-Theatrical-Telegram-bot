# -*- coding: utf-8 -*-

import telebot #импорт pyTelegramBotAPI 
from telebot import types #также достанем типы
import xlrd #библиотка чтения экселевских файлов
from xlrd.xldate import xldate_as_datetime

import datetime

from config import TOKEN
bot = telebot.TeleBot(TOKEN)

#Команды
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,"Привет, дорогой театрал🥰! Я Telegram-бот Тиа, и моя задача — помочь тебе быстро и просто выбрать мероприятие для хорошего времяпрепровождения!🎭\n\n 💜Введи команду /help, чтобы узнать о функциях бота💜") #Привет! Я Telegram-бот версии 2.0!
  
@bot.message_handler(commands=['help'])
def send_message_after_help(message):
    bot.send_message(message.chat.id,'🎭/searchbuttons - включает меню для поиска спектаклей по конкретным данным\n🎭/selections - отправляет театральные подборки, составленные экспертами\n🎭/test - викторина по театральному миру')

@bot.message_handler(commands=['searchbuttons'])
def button_main_menu(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Поиск по названию")
    item2=types.KeyboardButton("Поиск по рейтингу")
    item3=types.KeyboardButton("Поиск по жанру")
    item4=types.KeyboardButton("Дата")
    item5=types.KeyboardButton("Поиск по цене")
    item7=types.KeyboardButton("Поиск по возрасту")
    item8=types.KeyboardButton("Возврат к главным командам")
    item=types.KeyboardButton("ИНФО")
    markup.add(item1, item2, item3, item4, item5)
    markup.add(item7)
    markup.add(item8)
    markup.add(item)
    bot.send_message(message.chat.id,'Ты находишься в главном меню! Здесь можно выбрать, какие подборки мне показать.',reply_markup=markup)
    bot.send_message(message.chat.id,'Если хочешь узнать, какая кнопка за что отвечает, просто нажми или отправь "ИНФО" в чат')

@bot.message_handler(commands=['test'])
def test(message):
    rv = xlrd.open_workbook("D:/_New/Program vs/bot/TelegranBot2/Viktorina.xlsx")
    rsheetv = rv.sheet_by_index(0)
    send_message_after_test(message)
    #bot.register_next_step_handler(message, func_start)
    bot.register_next_step_handler(message, func_quiz_start, rsheetv)

    
@bot.message_handler(commands=['selections'])
def send_message_after_selections(message):
    bot.send_message(message.chat.id, 'Данная команда поможет тебе увидеть авторские подборки от театральных экспертов🤓')
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("5 лучших спектаклей для свидания💏")
    item2=types.KeyboardButton("5 спектаклей, чтобы пригласить родителей👫")
    item3=types.KeyboardButton("5 спектаклей для любителей современного театра🎆")
    item4=types.KeyboardButton("5 спектаклей, которые подойдут всем🌟")
    item5=types.KeyboardButton("Вернуться к остальным функциям")
    markup.add(item1, item2)
    markup.add(item3)
    markup.add(item4)
    markup.add(item5)
    bot.send_message(message.chat.id,'Выбери подходящую подборку',reply_markup=markup)

@bot.message_handler(content_types=['text'])
def message_reply(message):
    rb = xlrd.open_workbook("D:/_New/Program vs/bot/TelegranBot2/theatres_table.xlsx")
    rsheet = rb.sheet_by_index(0)
    
    #Главные команды
    if message.text=="Старт":
        send_welcome(message)
    elif message.text=="Кнопки":
        button_main_menu(message)
    elif (message.text=="Хэлп" or message.text=="Хелп" or message.text=="Помоги" or message.text=="Помощь" or message.text=="help" or message.text=="help me"):
        send_message_after_help(message)
    if message.text=="Возврат к главным командам":
        send_message_after_help(message)
    #Главные кнопки
    elif message.text=="Поиск по названию":
        bot.send_message(message.chat.id, 'Хочешь узнать подробнее о представлении? Без проблем! Просто введи его название:')
        bot.register_next_step_handler(message, search_performance_for_name, rsheet)
    elif message.text=="Поиск по рейтингу":
        message_answer_rating(message)
    elif message.text=="Поиск по жанру":
        search_performance_for_genre5(message, rsheet)
    elif message.text=="Дата":
        message_answer_date(message)
    elif message.text=="Поиск по цене":
        main_search_for_performances_by_price(message, rsheet)
    elif message.text=="Поиск по возрасту":
        bot.send_message(message.chat.id,'Хочешь сходить на спектакль с учетом возраста?')
        button_age_search(message)
        bot.register_next_step_handler(message, button_age_search2, rsheet)
    elif message.text=="ИНФО":
        bot.send_message(message.chat.id,'Чтобы увидеть кнопки, нажми на значок в правой части строки:)\n\n«Поиск по названию» позволит тебе узнать информацию о пяти спектаклях с одинаковым названием (дата, время, цена и тд.)\n«Поиск по рейтингу» создаст подборку с самым лучшим рейтингом\n«Поиск по дате» покажет, какие спектакли проходят в данную дату\n«Поиск по цене» подберет самые дешевые спектакли по введённой цене\n«Поиск по возрасту» подскажет спектакли с определённым возрастным ограничением')

    #Возврат в главное меню
    elif message.text=="Вернуться в главное меню":
        button_main_menu(message)
    #Дополнительные кнопки
    
    #Рейтинг
    elif message.text=="Рейтинг от":
        bot.send_message(message.chat.id,'Для того, чтобы я что-нибудь нашла, просто введи число от 1 до 10')
        bot.register_next_step_handler(message, search_for_performance_by_rating_with_price, rsheet)
    elif message.text=="5 спектаклей с самым высоким рейтингом":
        #bot.send_message(message.chat.id,'Вот, что я смогла найти:')
        search_for_performance_by_the_highest_rating_with_price(message, rsheet)
   
    #Дата
    elif message.text=="Поиск по дате":
        bot.send_message(message.chat.id, 'Хорошо! Сейчас я постараюсь тебе что-нибудь подобрать! Просто введи нужное число\nНапример:\n07.05.2022\n07 05 2022\n7 апреля 2022\n7 апр 2022\n')
        bot.register_next_step_handler(message, input_the_date2, rsheet)
    elif message.text=="Ближайшая дата":
        bot.send_message(message.chat.id, 'Вот, что мне удалось найти!')
        search_for_performances_by_the_nearest_date(message, rsheet)
    elif(message.text == "5 лучших спектаклей для свидания💏"):
       bot.send_message(message.chat.id,'Авторcтво - Telegram канал «Театральная вешалка»:\n🎭«Варшавская мелодия» в МДТ-Театре Европы\n🎭«Джульетта» в БДТ\n🎭«Любовные письма» в Мастерской\n🎭«Ромео и Джульетта» в ТЮЗе\n🎭«Квадрат» в Плохом театре"')
    elif(message.text == "5 спектаклей, чтобы пригласить родителей👫"):
         bot.send_message(message.chat.id, text="Авторcтво - Telegram канал «Театральная вешалка»:\n🎭«Слава» в БДТ«Старший сын» в Мастерской\n🎭«Братья и Сёстры» в МДТ-Театре Европы\n🎭«Маскарад» в Александринском театре\n🎭«Мой дедушка был вишней» в БТК")
    elif(message.text == "5 спектаклей для любителей современного театра🎆"):
       bot.send_message(message.chat.id, text="Авторcтво - Telegram канал «Театральная вешалка»:\n🎭«Лир» в Приюте комедианта«Макбет.Кино» в Театре им.Ленсовета\n🎭«Репортаж с петлей на шее» в Театро Ди Капуа\n🎭«Фаза зеркала» в Pop-up театре\n🎭«Фунт мяса» в Каменноостровском Театре")
    elif(message.text == "5 спектаклей, которые подойдут всем🌟"):
          bot.send_message(message.chat.id, text="Авторcтво - Telegram канал «Театральная вешалка»:\n🎭«Вишневый сад» в МДТ-Театре Европы\n🎭«Губернатор» в БДТ\n🎭«Преступление и наказание» в НДТ\n🎭«Ваня» в Karlsson Haus\n🎭«Оптимистическая трагедия» в Александринском театре")
    elif message.text=="Другие подборки":
       send_message_after_selections(message)
    elif message.text=="Вернуться к остальным функциям":
         send_message_after_help(message)

def send_message_after_test(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Начать викторину")
    markup.add(item1)
    bot.send_message(message.chat.id,'Начинаем викторину💡',reply_markup=markup)

def func_quiz(message, number, rsheetv):
    if (message.text == "Ответ" and number < 10):
        bot.send_message(message.chat.id, f'Ответ:\n {rsheetv.cell(number, 1).value}')
        if (number==9):
            bot.send_message(message.chat.id, f'Поздравляю! Ты прошел всю викторину. Нажми кнопку "Выход из викторины"')
    elif (message.text == "Следующий вопрос"):
        if(number<9):
            number=number+1
            bot.send_message(message.chat.id, f'Вопрос номер {number+1}')
            bot.send_message(message.chat.id, f'{rsheetv.cell(number, 0).value}')
        else:
            bot.send_message(message.chat.id, f'Поздравляю! Ты прошел всю викторину. Нажми кнопку "Выход из викторины"')
    elif (message.text == "Выход из викторины"):
        send_message_after_help(message)
    if (message.text != "Выход из викторины"):
        bot.register_next_step_handler(message,  func_quiz, number, rsheetv)

def func_quiz_start(message, rsheetv):
     if(message.text == "Начать викторину"):
        number=0
        bot.send_message(message.chat.id, f'Всего в викторине 10 вопросов. Удачи!')
        mess_after_start_quiz(message, number)
        bot.send_message(message.chat.id, f'{rsheetv.cell(number, 0).value}')
        bot.register_next_step_handler(message,  func_quiz, number, rsheetv)
        #bot.register_next_step_handler(message,  func_quiz_start2, rsheetv, number)

def func_quiz_start2(message, rsheetv, number):
    #bot.send_message(message.chat.id, f'Вопрос:\n {rsheetv.cell(number, 0).value}')
    bot.register_next_step_handler(message,  func_quiz, number, rsheetv)

def mess_after_start(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Следующий вопрос")
    item2=types.KeyboardButton("Ответ")
    item3=types.KeyboardButton("Выход из викторины")
    markup.add(item1, item2)
    markup.add(item3)
    #bot.send_message(message.chat.id,'Вопрос\n',reply_markup=markup)
    bot.send_message(message.chat.id,'\n', reply_markup=markup)

def mess_after_start_quiz(message, number):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Следующий вопрос")
    item2=types.KeyboardButton("Ответ")
    item3=types.KeyboardButton("Выход из викторины")
    markup.add(item1, item2)
    markup.add(item3)
    #bot.send_message(message.chat.id,'Вопрос\n',reply_markup=markup)
    bot.send_message(message.chat.id, f'Вопрос номер {number+1}', reply_markup=markup)

def date_func(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Другие подборки")
    markup.add(item1)
    bot.send_message(message.chat.id,'Авторcтво - Telegram канал «Театральная вешалка»:\n🎭«Варшавская мелодия» в МДТ-Театре Европы\n🎭«Джульетта» в БДТ\n🎭«Любовные письма» в Мастерской\n🎭«Ромео и Джульетта» в ТЮЗе\n🎭«Квадрат» в Плохом театре"',reply_markup=markup)

def parents_func(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Другие подборки")
    markup.add(item1)
    bot.send_message(message.chat.id, text="Авторcтво - Telegram канал «Театральная вешалка»:\n🎭«Слава» в БДТ«Старший сын» в Мастерской\n🎭«Братья и Сёстры» в МДТ-Театре Европы\n🎭«Маскарад» в Александринском театре\n🎭«Мой дедушка был вишней» в БТК", reply_markup=markup)

def modern_func(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Другие подборки")
    markup.add(item1)
    bot.send_message(message.chat.id, text="Авторcтво - Telegram канал «Театральная вешалка»:\n🎭«Лир» в Приюте комедианта«Макбет.Кино» в Театре им.Ленсовета\n🎭«Репортаж с петлей на шее» в Театро Ди Капуа\n🎭«Фаза зеркала» в Pop-up театре\n🎭«Фунт мяса» в Каменноостровском Театре", reply_markup=markup)

def all_func(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Другие подборки")
    markup.add(item1)
    bot.send_message(message.chat.id, text="Авторcтво - Telegram канал «Театральная вешалка»:\n🎭«Вишневый сад» в МДТ-Театре Европы\n🎭«Губернатор» в БДТ\n🎭«Преступление и наказание» в НДТ\n🎭«Ваня» в Karlsson Haus\n🎭«Оптимистическая трагедия» в Александринском театре", reply_markup=markup)


#Отвечает на сообщение "Рейтинг"
def message_answer_rating(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttongenre1=types.KeyboardButton("Рейтинг от")
    buttongenre2=types.KeyboardButton("5 спектаклей с самым высоким рейтингом")
    buttongenre3=types.KeyboardButton("Вернуться в главное меню")
    markup.add(buttongenre1, buttongenre2)
    markup.add(buttongenre3)
    bot.send_message(message.chat.id,'Ты на вкладке "Рейтинг". Здесь ты можешь выбрать, что мне показать - 5 спектаклей с рейтингом, подходящим под введенный тобой, или 5 спектаклей с самым высоким рейтингом.',reply_markup=markup)
    bot.send_message(message.chat.id,'Ах, да, я постаралась подобрать представления с самой низкой ценой! Надеюсь, тебе что-нибудь приглянётся!')
#Отвечает на сообщение "Жанр"
def message_answer_genre(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttongenre1=types.KeyboardButton("Драма")
    buttongenre2=types.KeyboardButton("Комедия")
    buttongenre3=types.KeyboardButton("Мюзикл")
    buttongenre4=types.KeyboardButton("Балет")
    buttongenre5=types.KeyboardButton("Опера")
    buttongenre6=types.KeyboardButton("Кукольный спектакль")
    buttongenre7=types.KeyboardButton("Детям")
    buttongenre8=types.KeyboardButton("Вернуться в главное меню")
    markup.add(buttongenre1, buttongenre2, buttongenre3, buttongenre4)
    markup.add(buttongenre5, buttongenre6, buttongenre7, buttongenre8)
    bot.send_message(message.chat.id,'Ты на вкладке "Жанры". Может быть, ты хочешь пустить слезу, смотря что-то настолько же драматичное, как "Ромео и Джульетта", или же, наоборот, от души посмеяться при просмотре комедии "Женитьба Фигаро"?',reply_markup=markup)
#Отвечает на сообщение "Дата"
def message_answer_date(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttongenre1=types.KeyboardButton("Ближайшая дата")
    buttongenre2=types.KeyboardButton("Поиск по дате")
    buttongenre3=types.KeyboardButton("Вернуться в главное меню")
    markup.add(buttongenre1, buttongenre2)
    markup.add(buttongenre3)
    bot.send_message(message.chat.id,'Ты на вкладке "Дата". Тут я могу подобрать спектакли в ближайшие даты, или же в какую-нибудь определенную!',reply_markup=markup)
#Отвечает на сообщение "Цена"
def message_answer_prise(message):
    markup3=types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttonprice1=types.KeyboardButton("Выбор по цене")
    buttonprice2=types.KeyboardButton("Узнать цену")
    buttonprice3=types.KeyboardButton("Вернуться в главное меню")
    markup3.add(buttonprice1, buttonprice2)
    markup3.add(buttonprice3)
    bot.send_message(message.chat.id,'Я изо всех сил постараюсь помочь тебе подобрать интересное театральное представление по идеальной цене!', reply_markup=markup3)

#ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ
#Выводит всю доступную информацию о спектакле
def info_about_performance_one(message, rsheet, rownumber):
    performancentmp=rsheet.row_values(rownumber, 0, 13)
    str1=''
    strdescription=''
    str2=''
    if(performancentmp[0]!=-1):
        str1+="Название: "+performancentmp[0]+"\n"
    if(performancentmp[1]!=-1):
        strdescription+="Описание: " + performancentmp[1]+"\n"
    if(performancentmp[5]!=-1):
        str1+="Жанр: "+performancentmp[5]+"\n"
    if(performancentmp[6]!='-1' and float(performancentmp[6])!= -1):
        str1+="Рейтинг: "+str(performancentmp[6])+"\n"
    if(performancentmp[9]!=-1):
        str1+="Возрастное ограничение: "+performancentmp[9]+"\n"
    if(performancentmp[4]!=-1):
        daymonthyear=main_converting_a_message_string_to_numbers(performancentmp[4], message)
        str1+="Ближайшая дата: "
        if(daymonthyear[0]<=9):
            str1+="0"+str(daymonthyear[0])+"."
        else:
            str1+=str(daymonthyear[0])+"."
        if(daymonthyear[1]<=9):
            str1+="0"+str(daymonthyear[1])+"."
        else:
            str1+=str(daymonthyear[1])+"."
        if(daymonthyear[2]<=9):
            str1+="0"+str(daymonthyear[2])+"\n"
        else:
            str1+=str(daymonthyear[2])+"\n"
    if(performancentmp[3]!=-1):
        str1+="Время: "+performancentmp[3]+"\n"
    if(performancentmp[11]!=-1 and performancentmp[11]!='-1'):
        str1+="Продолжительность: "+performancentmp[11]+"\n"
    if(performancentmp[2]!=-1):
        str1+="Цена: "+str(int(performancentmp[2]))+"\n"
    if(performancentmp[7]!=-1):
        str1+="Театр: "+performancentmp[7]+"\n"
    if(performancentmp[10]!=-1):
        str1+="Адрес: "+performancentmp[10]+"\n"
    if(performancentmp[12]!=-1):
        str2+="Другие даты: "+performancentmp[12]+"\n"
    if(performancentmp[8]!=-1):
        str2+="Ссылка: "+performancentmp[8]+"\n"
    bot.send_message(message.chat.id, f"{str1}{strdescription}{str2}")
    # 0 Название.  1 Описание.  2 Цена от.  3 Время начала.  
    # 4 Дата словами.  5 Жанр.  6 Рейтинг.  7 Театр.  8 Ссылка.  9 Возрастное ограничение.  10 театр
    # 11 Продолжительность 12 Другие даты и время

#Чтение даты из файла и перевод её в формат - день, месяц, год.
def converting_a_date_string_to_numbers(rsheet, rownumber):
    strdate=rsheet.cell(rownumber, 4).value
    daymonthyearstr=strdate.split(".")
    daymonthyear=[-1,-1,-1]
    daymonthyear[0]=int(daymonthyearstr[0])
    daymonthyear[1]=int(daymonthyearstr[1])
    daymonthyear[2]=int(daymonthyearstr[2])+2000
    return daymonthyear
#Считывание данных, введенных пользователем. 
#Перевод текстовой даты, введенной пользователем в числа - день, месяц, год
def converting_a_message_string_to_numbers2(message):
    daymonthyearstr=message.text.split()
    daymonthyear=[-1, -1, -1]
    print(len(daymonthyearstr))
    if(len(daymonthyearstr)!=3):
        if(len(daymonthyearstr)==1):
            daymonthyearstr=message.text.split('.')
        if(len(daymonthyearstr)!=3):
            return daymonthyear
    try:
        daymonthyear[0]=int(daymonthyearstr[0])
        daymonthyear[2]=int(daymonthyearstr[2])
        daymonthyear[1]=converting_a_month_to_numbers(daymonthyearstr[1])
    except ValueError:
        daymonthyear=[-1, -1, -1]
    if(daymonthyear[0]==-1 or daymonthyear[1]==-1 or daymonthyear[2]==-1):
        daymonthyear=[-1,-1,-1]
    return daymonthyear


def main_converting_a_message_string_to_numbers(date, message):
    daymonthyearstr=date.split()
    daymonthyear=[-1, -1, -1]
    print(len(daymonthyearstr))
    if(len(daymonthyearstr)!=3):
        if(len(daymonthyearstr)==1):
            daymonthyearstr=date.split('.')
        if(len(daymonthyearstr)!=3):
            return daymonthyear
    try:
        daymonthyear[0]=int(daymonthyearstr[0])
        daymonthyear[2]=int(daymonthyearstr[2])
        daymonthyear[1]=converting_a_month_to_numbers(daymonthyearstr[1])
    except ValueError:
        daymonthyear=[-1, -1, -1]
    if(daymonthyear[0]==-1 or daymonthyear[1]==-1 or daymonthyear[2]==-1):
        daymonthyear=[-1,-1,-1]
    return daymonthyear
#Перевод введенного пользователем месяца в число.
def converting_a_month_to_numbers(strmonth):
    monthnumber=-1
    if ((strmonth=='января') or (strmonth=='янв') or (strmonth=='01') or (strmonth=='1')):
        monthnumber=1
    elif ((strmonth=='февраля') or (strmonth=='фев') or (strmonth=='02') or (strmonth=='2')):
        monthnumber=2
    elif ((strmonth=='марта') or (strmonth=='мар') or (strmonth=='03') or (strmonth=='3')):
        monthnumber=3
    elif ((strmonth=='апреля') or (strmonth=='апр') or (strmonth=='04') or (strmonth=='4')):
        monthnumber=4
    elif ((strmonth=='мая') or (strmonth=='май') or (strmonth=='05') or (strmonth=='5')):
        monthnumber=5
    elif ((strmonth=='июня') or (strmonth=='июн') or (strmonth=='06') or (strmonth=='6')):
        monthnumber=6
    elif ((strmonth=='июля') or (strmonth=='июл') or (strmonth=='07') or (strmonth=='7')):
        monthnumber=7
    elif ((strmonth=='августа') or (strmonth=='авг') or (strmonth=='08') or (strmonth=='8')):
        monthnumber=8
    elif ((strmonth=='сентября') or (strmonth=='сен') or (strmonth=='09') or (strmonth=='9')):
        monthnumber=9
    elif ((strmonth=='октября') or (strmonth=='окт') or (strmonth=='10') or (strmonth=='10')):
        monthnumber=10
    elif ((strmonth=='ноября') or (strmonth=='ноя') or (strmonth=='11') or (strmonth=='11')):
        monthnumber=11
    elif ((strmonth=='декабря') or (strmonth=='дек') or (strmonth=='12') or (strmonth=='12')):
        monthnumber=12
    return monthnumber
s=0
#Ввод даты от пользователя. Не забыть учесть ситуацию, если бот ничего не нашёл!!
def input_the_date2(message, rsheet):
    daymonthyear=[-1,-1,-1]
    global s
    daymonthyear=converting_a_message_string_to_numbers2(message)
    if daymonthyear[0]!=-1:
            s=1
    if (s==0):
        bot.send_message(message.chat.id, 'Извини, но я тебя немного не поняла, можешь ввести ещё раз?)')
        bot.register_next_step_handler(message,  input_the_date2, rsheet)
    else:
        bot.send_message(message.chat.id, 'Вот что у меня получилось найти:')
        search_for_performances_by_date(message, rsheet, daymonthyear)
    s=0
    print("end")


#ПОИСК ПО РАЗНЫМ КРИТЕРИЯМ
#РЕЙТИНГ
#рейтинг, удовл условию, затем самые низкие цены
def search_for_performance_by_rating_with_price(message, rsheet):
    numberofperformance=[0,0,0,0,0]
    number=0
    for rowcounter in range(1, rsheet.nrows):
        if(float(message.text)<=float(rsheet.cell(rowcounter, 6).value)):
            if (number<5):
                numberofperformance[number]=rowcounter
                number=number+1
            else:
                max1=0
                for k in range(1,number):
                    if(float(rsheet.cell(numberofperformance[max1], 2).value)<float(rsheet.cell(numberofperformance[k], 2).value)):
                       max1=k
                if(float(rsheet.cell(rowcounter, 2).value)<float(rsheet.cell(numberofperformance[max1], 2).value)):
                    numberofperformance[max1]=rowcounter
    if(number==0):
        bot.send_message(message.chat.id, 'Прости, но я ничего не смогла найти')
    else:
        bot.send_message(message.chat.id, 'Вот, что я смогла найти!')
    for k in range(0,number):
        info_about_performance_one(message, rsheet, numberofperformance[k])

#Поиск спектаклей с самым высоким рейтингом. Может добавить возможность ввода количества выводимых спектаклей?
def search_for_performance_by_the_highest_rating_with_price(message, rsheet):
    numberofperformance=[0,0,0,0,0]
    number=0
    for rowcounter in range(1, rsheet.nrows):
        if (number<5):
            numberofperformance[number]=rowcounter
            number=number+1
        else:
            minr1=0
            for k in range(1,number):
                #ищем самый низкий рейтинг, если самых низких - 2, то ищем самую высокую цену 
                if(float(rsheet.cell(numberofperformance[minr1], 6).value)>=float(rsheet.cell(numberofperformance[k], 6).value)):
                    #minr1=k
                    if(float(rsheet.cell(numberofperformance[minr1], 6).value)==float(rsheet.cell(numberofperformance[k], 6).value)):
                        if(float(rsheet.cell(numberofperformance[minr1], 2).value)<=float(rsheet.cell(numberofperformance[k], 2).value)):
                            minr1=k
                    else:
                        minr1=k
            if(float(rsheet.cell(rowcounter, 6).value)==float(rsheet.cell(numberofperformance[minr1], 6).value)):
                if(float(rsheet.cell(rowcounter, 2).value)<=float(rsheet.cell(numberofperformance[minr1], 2).value)):
                    numberofperformance[minr1]=rowcounter
            elif(float(rsheet.cell(rowcounter, 6).value)>float(rsheet.cell(numberofperformance[minr1], 6).value)):
                numberofperformance[minr1]=rowcounter
    if(number==0):
        bot.send_message(message.chat.id, 'Прости, но я ничего не смогла найти')
    else:
        bot.send_message(message.chat.id, 'Вот, что я смогла найти!')
    for k in range(0,number):
        info_about_performance_one(message, rsheet, numberofperformance[k])

#ДАТА
#Поиск спектаклей по введенной дате, при выборе сначала учитывается цена, а затем - рейтинг
def search_for_performances_by_date(message, rsheet, daymonthyear):
    numberofperformance=[0,0,0,0,0]
    number=0
    for rowcounter in range(1, rsheet.nrows):
        daymonthyearexl=converting_a_date_string_to_numbers(rsheet, rowcounter)
        if(daymonthyear[1]==daymonthyearexl[1]):
            if(daymonthyear[0]==daymonthyearexl[0]):
                print(daymonthyearexl)
                if(number<5):
                    numberofperformance[number]=rowcounter
                    number+=1
                else:
                    numberofperformance = selection_first_by_price_then_by_rating(rsheet, number, numberofperformance, rowcounter)
    if(number==0):
        bot.send_message(message.chat.id, 'Прости, но я ничего не смогла найти')
    else:
        bot.send_message(message.chat.id, 'Вот, что я смогла найти!')
    for k in range(0,number):
        info_about_performance_one(message, rsheet, numberofperformance[k])
#Поиск ближайших дат втечении недели, но акцент на цену, затем на рейтинг, а даты не смотрятся сааааамые ближайшие
#Не будет работать, если сейчас конец месяца, надо прописать данную ситуаию отдельно + добавить учитывание года
def search_for_performances_by_the_nearest_date(message, rsheet):
    numberofperformance=[0,0,0,0,0]
    number=0

    now=datetime.datetime.now()
    daymonthyearnow=[now.day, now.month, now.year]
    print(daymonthyearnow)

    for rowcounter in range(1, rsheet.nrows):
        daymonthyearexl=converting_a_date_string_to_numbers(rsheet, rowcounter)
        if(daymonthyearexl[1]==daymonthyearnow[1]):
            if(((daymonthyearexl[0] - daymonthyearnow[0]) <=7) and ((daymonthyearexl[0] - daymonthyearnow[0]) >=0)):
                if(number<5):
                    numberofperformance[number]=rowcounter
                    number+=1
                else:
                    numberofperformance = selection_first_by_price_then_by_rating(rsheet, number, numberofperformance, rowcounter)
    for k in range(0,number):
        info_about_performance_one(message, rsheet, numberofperformance[k])

#Отбор по самой низкой цене, затем по самому высокому рейтингу
#Ищет номер строки с наибольшей стоимостью, затем заменяет на текущую строку, которая до этого прошла условия отбора
def selection_first_by_price_then_by_rating(rsheet, number, numberofperformance, rowcounter):
    maxk=0
    for k in range(1,number):
        if(float(rsheet.cell(numberofperformance[maxk], 2).value)<float(rsheet.cell(numberofperformance[k], 2).value)):
            maxk=k
        elif(float(rsheet.cell(numberofperformance[maxk], 2).value)==float(rsheet.cell(numberofperformance[k], 2).value)):
            if(float(rsheet.cell(numberofperformance[maxk], 6).value)<=float(rsheet.cell(numberofperformance[k], 6).value)):
                maxk=k
    if(float(rsheet.cell(numberofperformance[maxk], 2).value)>float(rsheet.cell(rowcounter, 2).value)):
        numberofperformance[maxk]=rowcounter
    elif(float(rsheet.cell(numberofperformance[maxk], 2).value)==float(rsheet.cell(rowcounter, 2).value)):
            if(float(rsheet.cell(numberofperformance[maxk], 6).value)<=float(rsheet.cell(rowcounter, 6).value)):
                numberofperformance[maxk]=rowcounter
    return numberofperformance
#НАЗВАНИЕ
#Поиск представления по названию. Ищет самую низкую цену.
def search_performance_for_name(message, rsheet):
    numberofperformancewithminprice=0
    messagestr=str(message.text)
    count=0
    now=datetime.datetime.now()
    daymonthyearnow=[now.day, now.month, now.year]
    for rowcounter in range(1, rsheet.nrows):
        daymonthyearexl=converting_a_date_string_to_numbers(rsheet, rowcounter)
        if(daymonthyearexl[1]<=daymonthyearnow[1]):
            if(daymonthyearexl[1]==daymonthyearnow[1]):
                if(daymonthyearexl[0]<daymonthyearnow[0]):
                    continue
            else:
                continue
        if (messagestr==rsheet.cell(rowcounter, 0).value):
            if(count==0):
                numberofperformancewithminprice=rowcounter
                count+=1
            else:
                if(float(rsheet.cell(numberofperformancewithminprice, 2).value)>float(rsheet.cell(rowcounter, 2).value)):
                    numberofperformancewithminprice=rowcounter
    if(count!=0):
        bot.send_message(message.chat.id, 'Вот, что у меня получилось найти!')
        info_about_performance_one(message, rsheet, numberofperformancewithminprice)
    else:
        bot.send_message(message.chat.id, 'Прости, но я ничего не знаю об этом спектакле.')
    button_main_menu(message)


def search_performance_for_genre5(message, rsheet):
    message_answer_genre(message)
    bot.send_message(message.chat.id,'После выбора жанра, ты можешь выбрать дату, которая тебя интересует!')
    bot.register_next_step_handler(message, search_performance_main0, rsheet)

def message_answer_date_after_genre(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttongenre1=types.KeyboardButton("Ввести")
    buttongenre2=types.KeyboardButton("Ближайшие")
    buttongenre3=types.KeyboardButton("Не важно")
    buttongenre4=types.KeyboardButton("Вернуться в главное меню")
    markup.add(buttongenre1, buttongenre2, buttongenre3, buttongenre4)
    bot.send_message(message.chat.id,'Выбери дату!',reply_markup=markup)

def search_performance_main0(message, rsheet):
    parameters=[-1, -1, -1, -1]
    parameters[0]=message.text
    message_answer_date_after_genre(message)
    if parameters[0]=="Вернуться в главное меню":
        button_main_menu(message)
    else:
        bot.register_next_step_handler(message, message_answer_date_after_genre1, rsheet, parameters)


def message_answer_date_after_genre1(message, rsheet, parameters):
    parameters[1]=message.text

    if parameters[1]=="Ввести":
        bot.send_message(message.chat.id, 'Отлично! Теперь просто введи интересующую тебя дату. Например\n1 апреля 2022\n1 апр 2022\n1 04 2022\n1.04.2022')
        bot.register_next_step_handler(message,  input_the_date3, parameters, rsheet)
    elif parameters[1]=="Ближайшие":
        message_answer_price_after_genre_after_date(message)
        bot.register_next_step_handler(message, message_answer_price_after_genre_after_date2, rsheet, parameters)
    elif parameters[1]=="Не важно":
        message_answer_price_after_genre_after_date(message)
        bot.register_next_step_handler(message, message_answer_price_after_genre_after_date3, rsheet, parameters)
    elif parameters[1]=="Вернуться в главное меню":
        button_main_menu(message)

def message_answer_price_after_genre_after_date(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttongenre1=types.KeyboardButton("По цене")
    buttongenre2=types.KeyboardButton("По рейтингу")
    buttongenre4=types.KeyboardButton("Вернуться в главное меню")
    markup.add(buttongenre1, buttongenre2)
    markup.add(buttongenre4)
    bot.send_message(message.chat.id,'Давай я объясню поподробнее!\nПриоритет по цене - поиск самой низкой цены, а затем уже поиск по рейтингу\nПриоритет по рейтингу - я нахожу представления с самым высоким рейтингом и самыми низкими ценами в этом рейтинге',reply_markup=markup)

def message_answer_price_after_genre_after_date2(message, rsheet, parameters):
    parameters[2]=message.text
    if parameters[2]=="Вернуться в главное меню":
        button_main_menu(message)
        return
    numberofperformance=[0,0,0,0,0]
    number=0

    now=datetime.datetime.now()
    daymonthyearnow=[now.day, now.month, now.year]
    print(daymonthyearnow)

    for rowcounter in range(1, rsheet.nrows):
        daymonthyearexl=converting_a_date_string_to_numbers(rsheet, rowcounter)
        if(parameters[0]!=-1):
            if(parameters[0]!=rsheet.cell(rowcounter, 5).value):
                continue
        if(daymonthyearexl[1]==daymonthyearnow[1]):
            if(((daymonthyearexl[0] - daymonthyearnow[0]) > 7) or ((daymonthyearexl[0] - daymonthyearnow[0]) < 0)):
                continue
        else:
            if(daymonthyearexl[1] - daymonthyearnow[1]!=1):
                continue
            else:
                if(31-daymonthyearnow[0]+daymonthyearexl[0]>7):
                    continue
        
        if(number<5):
            numberofperformance[number]=rowcounter
            number+=1
        else:
            if(parameters[2]=="По цене"):
                numberofperformance = selection_first_by_price_then_by_rating(rsheet, number, numberofperformance, rowcounter)
            elif(parameters[2]=="По рейтингу"):
                numberofperformance = selection_first_by_rating_then_by_price(rsheet, number, numberofperformance, rowcounter)
    if(number==0):
        bot.send_message(message.chat.id, 'Прости, но я ничего не смогла найти')
    else:
        bot.send_message(message.chat.id, 'Вот, что я смогла найти!')
    for k in range(0,number):
        info_about_performance_one(message, rsheet, numberofperformance[k])
    button_main_menu(message)

def message_answer_price_after_genre_after_date3(message, rsheet, parameters):
    parameters[2]=message.text
    if parameters[2]=="Вернуться в главное меню":
        button_main_menu(message)
        return
    numberofperformance=[0,0,0,0,0]
    number=0

    now=datetime.datetime.now()
    daymonthyearnow=[now.day, now.month, now.year]
    print(daymonthyearnow)

    for rowcounter in range(1, rsheet.nrows):
        daymonthyearexl=converting_a_date_string_to_numbers(rsheet, rowcounter)
        if(parameters[0]!=-1):
            if(parameters[0]!=rsheet.cell(rowcounter, 5).value):
                continue
        if(daymonthyearexl[1]<=daymonthyearnow[1]):
            if(daymonthyearexl[1]==daymonthyearnow[1]):
                if(daymonthyearexl[0]<daymonthyearnow[0]):
                    continue
            else:
                continue
        if(number<5):
            numberofperformance[number]=rowcounter
            number+=1
        else:
            if(parameters[2]=="По цене"):
                numberofperformance = selection_first_by_price_then_by_rating(rsheet, number, numberofperformance, rowcounter)
            elif(parameters[2]=="По рейтингу"):
                numberofperformance = selection_first_by_rating_then_by_price(rsheet, number, numberofperformance, rowcounter)
    if(number==0):
        bot.send_message(message.chat.id, 'Прости, но я ничего не смогла найти')
    else:
        bot.send_message(message.chat.id, 'Вот, что я смогла найти!')
    for k in range(0,number):
        info_about_performance_one(message, rsheet, numberofperformance[k])
    button_main_menu(message)

def selection_first_by_rating_then_by_price(rsheet, number, numberofperformance, rowcounter):
    maxk=0
    for k in range(1,number):
        if(float(rsheet.cell(numberofperformance[maxk], 6).value)<float(rsheet.cell(numberofperformance[k], 6).value)):
            continue
        if(float(rsheet.cell(numberofperformance[maxk], 2).value)<float(rsheet.cell(numberofperformance[k], 2).value)):
            maxk=k
    if(float(rsheet.cell(numberofperformance[maxk], 6).value)<float(rsheet.cell(rowcounter, 6).value)):
        numberofperformance[maxk]=rowcounter
    elif(float(rsheet.cell(numberofperformance[maxk], 6).value)==float(rsheet.cell(rowcounter, 6).value)):
        if(float(rsheet.cell(numberofperformance[maxk], 2).value)>=float(rsheet.cell(rowcounter, 2).value)):
            numberofperformance[maxk]=rowcounter
    return numberofperformance

s1=0
#Ввод даты от пользователя. Не забыть учесть ситуацию, если бот ничего не нашёл!!
def input_the_date3(message, parameters, rsheet):
    daymonthyear=[-1,-1,-1]
    global s1
    daymonthyear=converting_a_message_string_to_numbers2(message)
    if daymonthyear[0]!=-1:
            s1=1
    if (s1==0):
        bot.send_message(message.chat.id, 'Извини, но я тебя немного не поняла, можешь ввести ещё раз?)')
        bot.register_next_step_handler(message,  input_the_date3, parameters, rsheet)
    else:
        bot.send_message(message.chat.id, 'Теперь выбери, по каким критериям мне показать представления!')
        message_answer_price_after_genre_after_date(message)
        bot.register_next_step_handler(message,  search_for_performances_by_date3, rsheet, daymonthyear, parameters)
    s1=0
    print("end")


#Поиск спектаклей по введенной дате, при выборе сначала учитывается цена, а затем - рейтинг
def search_for_performances_by_date3(message, rsheet, daymonthyear, parameters):
    parameters[2]=message.text
    if parameters[2]=="Вернуться в главное меню":
        button_main_menu(message)
        return
    numberofperformance=[0,0,0,0,0]
    number=0
    for rowcounter in range(1, rsheet.nrows):
        if(parameters[0]!=-1):
            if(rsheet.cell(rowcounter, 5).value!=parameters[0]):
                continue
        daymonthyearexl=converting_a_date_string_to_numbers(rsheet, rowcounter)
        if(daymonthyear[1]==daymonthyearexl[1]):
            if(daymonthyear[0]==daymonthyearexl[0]):
                print(daymonthyearexl)
                if(number<5):
                    numberofperformance[number]=rowcounter
                    number+=1
                else:
                    if(parameters[2]=="По цене"):
                        numberofperformance = selection_first_by_price_then_by_rating(rsheet, number, numberofperformance, rowcounter)
                    elif(parameters[2]=="По рейтингу"):
                        numberofperformance = selection_first_by_rating_then_by_price(rsheet, number, numberofperformance, rowcounter)
    if(number==0):
        bot.send_message(message.chat.id, 'Прости, но я ничего не смогла найти')
    else:
        bot.send_message(message.chat.id, 'Вот, что я смогла найти!')
    for k in range(0,number):
        info_about_performance_one(message, rsheet, numberofperformance[k])
    button_main_menu(message)

#0-жанр 1-дата 2-введенная дата 3-цена/рейтинг 4-введенная цена
def main_selection_first_by_price_then_by_rating(rsheet, number, numberofperformance, rowcounter, filters):
    maxk=0
    for k in range(1,number):
        if(filters[4]!=-1 and float(rsheet.cell(numberofperformance[k], 2).value) > filters[4]):
           continue
        if(float(rsheet.cell(numberofperformance[maxk], 2).value)<float(rsheet.cell(numberofperformance[k], 2).value)):
            maxk=k
        elif(float(rsheet.cell(numberofperformance[maxk], 2).value)==float(rsheet.cell(numberofperformance[k], 2).value)):
            if(float(rsheet.cell(numberofperformance[maxk], 6).value)<=float(rsheet.cell(numberofperformance[k], 6).value)):
                maxk=k
    if(float(rsheet.cell(numberofperformance[maxk], 2).value)>float(rsheet.cell(rowcounter, 2).value)):
        numberofperformance[maxk]=rowcounter
    elif(float(rsheet.cell(numberofperformance[maxk], 2).value)==float(rsheet.cell(rowcounter, 2).value)):
            if(float(rsheet.cell(numberofperformance[maxk], 6).value)<=float(rsheet.cell(rowcounter, 6).value)):
                numberofperformance[maxk]=rowcounter
    return numberofperformance
def main_input_the_maximum_price(message, rsheet, filters):
    try:
        print("success")
        filters[4]=int(message.text)
        main_message_answer_price_1(message, rsheet, filters)
    except ValueError:
        bot.send_message(message.chat.id, 'Прости, но я немного не поняла, можешь заново ввести максимальную цену')
        bot.register_next_step_handler(message,  main_input_the_maximum_price, rsheet,  filters)

def main_search_for_performances_by_price2(message, rsheet, filters):
    if(message.text=="Вернуться в главное меню"):
        button_main_menu(message)
    elif(message.text=="Выбор по цене"):
        bot.register_next_step_handler(message,  main_input_the_maximum_price, rsheet,  filters)
        bot.send_message(message.chat.id, 'Введи максимальную цену. Пожалуйста, обрати внимание, что тебе нужно ввести только число.\nНапример: 500')
    elif(message.text=="Узнать цену"):
        button_main_menu(message)
        bot.send_message(message.chat.id, 'Хочешь узнать подробнее о цене для какого-то представлении? Без проблем! Просто введи его название:')
        bot.register_next_step_handler(message, search_performance_for_name, rsheet)

def main_search_for_performances_by_price(message, rsheet):
    message_answer_prise(message)
    filters=[-1, -1, -1, -1, -1]
    bot.register_next_step_handler(message,  main_search_for_performances_by_price2, rsheet, filters)

def main_message_answer_price_1(message, rsheet, parameters):
    numberofperformance=[0,0,0,0,0]
    number=0

    now=datetime.datetime.now()
    daymonthyearnow=[now.day, now.month, now.year]

    for rowcounter in range(1, rsheet.nrows):
        daymonthyearexl=converting_a_date_string_to_numbers(rsheet, rowcounter)
        if(parameters[0]!=-1):
            if(parameters[0]!=rsheet.cell(rowcounter, 5).value):
                continue
        if(parameters[4]!=-1):
            if(parameters[4]<int(rsheet.cell(rowcounter, 2).value)):
                continue
        if(daymonthyearexl[1]<=daymonthyearnow[1]):
            if(daymonthyearexl[1]==daymonthyearnow[1]):
                if(daymonthyearexl[0]<daymonthyearnow[0]):
                    continue
            else:
                continue
        if(number<5):
            numberofperformance[number]=rowcounter
            number+=1
        else:
            numberofperformance=main_selection_first_by_price_then_by_rating(rsheet, number, numberofperformance, rowcounter, parameters)
    if(number==0):
        bot.send_message(message.chat.id, 'Прости, но я ничего не смогла найти')
    else:
        bot.send_message(message.chat.id, 'Вот, что я смогла найти!')
    for k in range(0,number):
        info_about_performance_one(message, rsheet, numberofperformance[k])
    button_main_menu(message)

def button_age_search(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("0+")
    item2=types.KeyboardButton("6+")
    item3=types.KeyboardButton("12+")
    item4=types.KeyboardButton("16+")
    item5=types.KeyboardButton("18+")
    item6=types.KeyboardButton("Вернуться в главное меню")
    markup.add(item1, item2, item3, item4, item5)
    markup.add(item6)
    bot.send_message(message.chat.id,'Ты находишься на вкладке "возраст"! Здесь можно выбрать, какие подборки мне показать.',reply_markup=markup)

def button_age_search2(message, rsheet):
    if(message.text=="Вернуться в главное меню"):
        button_main_menu(message)
    else:
        number=0
        now=datetime.datetime.now()
        daymonthyearnow=[now.day, now.month, now.year]
        for rowcounter in range(1, rsheet.nrows):
            daymonthyearexl=converting_a_date_string_to_numbers(rsheet, rowcounter)
            if(daymonthyearexl[1]<=daymonthyearnow[1]):
                if(daymonthyearexl[1]==daymonthyearnow[1]):
                    if(daymonthyearexl[0]<daymonthyearnow[0]):
                        continue
                else:
                    continue
            if(number<5):
                if(message.text==rsheet.cell(rowcounter, 9).value):
                    info_about_performance_one(message, rsheet, rowcounter)
                    number+=1
        button_main_menu(message)

if __name__ == '__main__':
    bot.polling(none_stop=True)