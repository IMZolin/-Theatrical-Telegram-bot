# -*- coding: cp1251 -*-
# -*- coding: utf-8 -*-
from os import kill
import telebot  # импорт pyTelegramBotAPI
from telebot import types  # также достанем типы
import xlrd  # библиотка чтения экселевских файлов
from xlrd.xldate import xldate_as_datetime

import datetime

from config import TOKEN

bot = telebot.TeleBot(TOKEN)


# Команды
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Привет! Я Театральный Telegram-бот Тиа, и моя задача - помочь тебе быстро и просто выбрать, куда сходить, чтобы весело провести время!")  # Привет! Я Telegram-бот версии 2.0!


@bot.message_handler(commands=['help'])
def send_message_after_help(message):
    bot.send_message(message.chat.id, 'Тут должны быть описания команд')


@bot.message_handler(commands=['buttons'])
def button_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Название")
    item2 = types.KeyboardButton("Рейтинг")
    item3 = types.KeyboardButton("Жанры")
    item4 = types.KeyboardButton("Дата")
    item5 = types.KeyboardButton("Цена")
    item6 = types.KeyboardButton("Театр")
    item7 = types.KeyboardButton("Возраст")
    item = types.KeyboardButton("ИНФО")
    markup.add(item1, item2, item3, item4, item5)
    markup.add(item6, item7)
    markup.add(item)
    bot.send_message(message.chat.id, 'Ты находишься в главном меню! Здесь можно выбрать, какие подборки мне показать.',
                     reply_markup=markup)
    bot.send_message(message.chat.id, 'Если хочешь узнать, какая кнопка за что отвечает, просто нажми "ИНФО"')


@bot.message_handler(content_types='text')
def message_reply(message):
    rb = xlrd.open_workbook("D:/_New/Program vs/bot/ticketland_parsing_2.xlsx")
    rsheet = rb.sheet_by_index(0)

    # Главные команды
    if message.text == "Старт":
        send_welcome(message)
    elif message.text == "Кнопки":
        button_main_menu(message)
    elif (
            message.text == "Хэлп" or message.text == "Хелп" or message.text == "Помоги" or message.text == "Помощь" or message.text == "help" or message.text == "help me"):
        send_message_after_help(message)

    # Главные кнопки
    elif message.text == "Название":
        bot.send_message(message.chat.id,
                         'Хочешь узнать подробнее о представлении? Без проблем! Просто введи его название.')
        bot.register_next_step_handler(message, search_performance_for_name, rsheet)
    elif message.text == "Рейтинг":
        message_answer_rating(message)
    elif message.text == "Жанры":
        message_answer_genre(message)
    elif message.text == "Дата":
        message_answer_date(message)
    elif message.text == "Цена":
        message_answer_prise(message)
    elif message.text == "Театр":
        bot.send_message(message.chat.id, 'Хочешь сходить в какой-то определенный театр?')
        bot.send_message(message.chat.id,
                         'Понимаю, мне тоже не нравится стоять в часовых пробках, или толкаться в метро. Хотя... Может ты хочешь с головой окунуться в волшебную атмосферу театра?')
    elif message.text == "Возраст":
        bot.send_message(message.chat.id, 'Хочешь сходить на спектаклб с учетом возраста?')
    elif message.text == "ИНФО":
        bot.send_message(message.chat.id, 'Здесь должно быть что-нибудь написано, что будет помогать пользователю')

    # Возврат в главное меню
    elif message.text == "Вернуться в главное меню":
        button_main_menu(message)

    # Дополнительные кнопки

    # Рейтинг
    elif message.text == "Рейтинг от":
        bot.send_message(message.chat.id, 'Для того, чтобы я что-нибудь нашла, просто введи число от 1 до 10')
        bot.register_next_step_handler(message, search_for_performance_by_rating_with_price, rsheet)
    elif message.text == "5 спектаклей с самым высоким рейтингом":
        bot.send_message(message.chat.id, 'Вот, что я смогла найти:')
        search_for_performance_by_the_highest_rating_with_price(message, rsheet)

    # Дата
    elif message.text == "Поиск по дате":
        bot.send_message(message.chat.id, 'Хорошо! Сейчас я постараюсь тебе что-нибудь подобрать!')
        bot.send_message(message.chat.id, 'Напиши, какая дата тебя интересует. Например: 17 марта 2022')
        bot.register_next_step_handler(message, input_the_date2, rsheet)
    elif message.text == "Ближайшая дата":
        bot.send_message(message.chat.id, 'Вот, что мне удалось найти!')
        search_for_performances_by_the_nearest_date(message, rsheet)


# Отвечает на сообщение "Рейтинг"
def message_answer_rating(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttongenre1 = types.KeyboardButton("Рейтинг от")
    buttongenre2 = types.KeyboardButton("5 спектаклей с самым высоким рейтингом")
    buttongenre3 = types.KeyboardButton("Вернуться в главное меню")
    markup.add(buttongenre1, buttongenre2)
    markup.add(buttongenre3)
    bot.send_message(message.chat.id,
                     'Ты на вкладке "Рейтинг". Здесь ты можешь выбрать, что мне показать - 5 спектаклей с рейтингом, подходящим под введенный тобой, или 5 спектаклей с самым высоким рейтингом.',
                     reply_markup=markup)
    bot.send_message(message.chat.id,
                     'Ах, да, я постаралась подобрать представления с самой низкой ценой! Надеюсь, тебе что-нибудь приглянётся!')


# Отвечает на сообщение "Жанр"
def message_answer_genre(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttongenre1 = types.KeyboardButton("Драма")
    buttongenre2 = types.KeyboardButton("Комедия")
    buttongenre3 = types.KeyboardButton("Мюзикл")
    buttongenre4 = types.KeyboardButton("Балет")
    buttongenre5 = types.KeyboardButton("Опера")
    buttongenre6 = types.KeyboardButton("Кукольный спектакль")
    buttongenre7 = types.KeyboardButton("Детям")
    buttongenre8 = types.KeyboardButton("Вернуться в главное меню")
    markup.add(buttongenre1, buttongenre2, buttongenre3, buttongenre4)
    markup.add(buttongenre5, buttongenre6, buttongenre7, buttongenre8)
    bot.send_message(message.chat.id,
                     'Ты на вкладке "Жанры". Может быть, ты хочешь пустить слезу, смотря что-то настолько же драматичное, как "Ромео и Джульетта", или же, наоборот, от души посмеяться при просмотре комедии "Женитьба Фигаро"?',
                     reply_markup=markup)


# Отвечает на сообщение "Дата"
def message_answer_date(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttongenre1 = types.KeyboardButton("Ближайшая дата")
    buttongenre2 = types.KeyboardButton("Поиск по дате")
    buttongenre3 = types.KeyboardButton("Вернуться в главное меню")
    markup.add(buttongenre1, buttongenre2)
    markup.add(buttongenre3)
    bot.send_message(message.chat.id,
                     'Ты на вкладке "Дата". Тут я могу подобрать спектакли в ближайшие даты, или же в какую-нибудь определенную!',
                     reply_markup=markup)


# Отвечает на сообщение "Цена"
def message_answer_prise(message):
    markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttonprice1 = types.KeyboardButton("Выбор по цене")
    buttonprice2 = types.KeyboardButton("Узнать цену")
    buttonprice3 = types.KeyboardButton("Вернуться в главное меню")
    markup3.add(buttonprice1, buttonprice2)
    markup3.add(buttonprice3)
    bot.send_message(message.chat.id,
                     'Я изо всех сил постараюсь помочь тебе подобрать интересное театральное представление по идеальной цене!',
                     reply_markup=markup3)


# ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ
# Выводит всю доступную информацию о спектакле
def info_about_performance_one(message, rsheet, rownumber):
    performancentmp = rsheet.row_values(rownumber, 0, 13)
    str1 = ''
    strdescription = ''
    str2 = ''
    if (performancentmp[0] != -1):
        str1 += "Название: " + performancentmp[0] + "\n"
    if (performancentmp[1] != -1):
        strdescription += "Описание: " + performancentmp[1] + "\n"
    if (performancentmp[5] != -1):
        str1 += "Жанр: " + performancentmp[5] + "\n"
    if (performancentmp[6] != '-1'):
        str1 += "Рейтинг: " + str(performancentmp[6]) + "\n"
    if (performancentmp[9] != -1):
        str1 += "Возрастное ограничение: " + performancentmp[9] + "\n"
    if (performancentmp[4] != -1):
        str1 += "Ближайшая дата: " + performancentmp[4] + "\n"
    if (performancentmp[3] != -1):
        str1 += "Время: " + performancentmp[3] + "\n"
    if (performancentmp[11] != -1):
        str1 += "Продолжительность: " + performancentmp[11] + "\n"
    if (performancentmp[2] != -1):
        str1 += "Цена: " + performancentmp[2] + "\n"
    if (performancentmp[7] != -1):
        str1 += "Театр: " + performancentmp[7] + "\n"
    if (performancentmp[10] != -1):
        str1 += "Адрес: " + performancentmp[10] + "\n"
    if (performancentmp[12] != -1):
        str2 += "Другие даты: " + performancentmp[12] + "\n"
    if (performancentmp[8] != -1):
        str2 += "Ссылка: " + performancentmp[8] + "\n"
    bot.send_message(message.chat.id, f"{str1}{strdescription}{str2}")
    # 0 Название.  1 Описание.  2 Цена от.  3 Время начала.
    # 4 Дата словами.  5 Жанр.  6 Рейтинг.  7 Театр.  8 Ссылка.  9 Возрастное ограничение.  10 театр
    # 11 Продолжительность 12 Другие даты и время


# Чтение даты из файла и перевод её в формат - день, месяц, год.
def converting_a_date_string_to_numbers(rsheet, rownumber):
    strdate = rsheet.cell(rownumber, 4).value
    daymonthyearstr = strdate.split(".")
    daymonthyear = [-1, -1, -1]
    daymonthyear[0] = int(daymonthyearstr[0])
    daymonthyear[1] = int(daymonthyearstr[1])
    daymonthyear[2] = int(daymonthyearstr[2]) + 2000
    return daymonthyear


# Считывание данных, введенных пользователем.
# Перевод текстовой даты, введенной пользователем в числа - день, месяц, год
def converting_a_message_string_to_numbers2(message):
    daymonthyearstr = message.text.split()
    daymonthyear = [-1, -1, -1]
    print(len(daymonthyearstr))
    if (len(daymonthyearstr) != 3):
        return daymonthyear
    try:
        daymonthyear[0] = int(daymonthyearstr[0])
        daymonthyear[2] = int(daymonthyearstr[2])
        daymonthyear[1] = converting_a_month_to_numbers(daymonthyearstr[1])
    except ValueError:
        daymonthyear = [-1, -1, -1]
    if (daymonthyear[0] == -1 or daymonthyear[1] == -1 or daymonthyear[2] == -1):
        daymonthyear = [-1, -1, -1]
    else:
        bot.send_message(message.chat.id,
                         f"Была введена такая дата, верно?\n {daymonthyear[0]}.{daymonthyear[1]}.{daymonthyear[2]} ")
    return daymonthyear


# Перевод введенного пользователем месяца в число.
def converting_a_month_to_numbers(strmonth):
    monthnumber = -1
    if ((strmonth == 'января') or (strmonth == 'янв') or (strmonth == '01') or (strmonth == '1')):
        monthnumber = 1
    elif ((strmonth == 'февраля') or (strmonth == 'фев') or (strmonth == '02') or (strmonth == '2')):
        monthnumber = 2
    elif ((strmonth == 'марта') or (strmonth == 'мар') or (strmonth == '03') or (strmonth == '3')):
        monthnumber = 3
    elif ((strmonth == 'апреля') or (strmonth == 'апр') or (strmonth == '04') or (strmonth == '4')):
        monthnumber = 4
    elif ((strmonth == 'мая') or (strmonth == 'май') or (strmonth == '05') or (strmonth == '5')):
        monthnumber = 5
    elif ((strmonth == 'июня') or (strmonth == 'июн') or (strmonth == '06') or (strmonth == '6')):
        monthnumber = 6
    elif ((strmonth == 'июля') or (strmonth == 'июл') or (strmonth == '07') or (strmonth == '7')):
        monthnumber = 7
    elif ((strmonth == 'августа') or (strmonth == 'авг') or (strmonth == '08') or (strmonth == '8')):
        monthnumber = 8
    elif ((strmonth == 'сентября') or (strmonth == 'сен') or (strmonth == '09') or (strmonth == '9')):
        monthnumber = 9
    elif ((strmonth == 'октября') or (strmonth == 'окт') or (strmonth == '10') or (strmonth == '10')):
        monthnumber = 10
    elif ((strmonth == 'ноября') or (strmonth == 'ноя') or (strmonth == '11') or (strmonth == '11')):
        monthnumber = 11
    elif ((strmonth == 'декабря') or (strmonth == 'дек') or (strmonth == '12') or (strmonth == '12')):
        monthnumber = 12
    return monthnumber


s = 0


# Ввод даты от пользователя. Не забыть учесть ситуацию, если бот ничего не нашёл!!
def input_the_date2(message, rsheet):
    daymonthyear = [-1, -1, -1]
    global s
    daymonthyear = converting_a_message_string_to_numbers2(message)
    if daymonthyear[0] != -1:
        s = 1
    if (s == 0):
        # print("HELLO")
        bot.send_message(message.chat.id, 'прости, но я тебя немного не поняла, можешь повторить?')
        bot.register_next_step_handler(message, input_the_date2, rsheet)
        # print("hello2")
    else:
        # print("poisk po date")
        bot.send_message(message.chat.id, 'Вот, что у меня получилось найти!')
        search_for_performances_by_date(message, rsheet, daymonthyear)
    s = 0
    print("end")


# ПОИСК ПО РАЗНЫМ КРИТЕРИЯМ
# РЕЙТИНГ
# рейтинг, удовл условию, затем самые низкие цены
def search_for_performance_by_rating_with_price(message, rsheet):
    numberofperformance = [0, 0, 0, 0, 0]
    number = 0
    for rowcounter in range(1, rsheet.nrows):
        if (float(message.text) <= float(rsheet.cell(rowcounter, 6).value)):
            if (number < 5):
                numberofperformance[number] = rowcounter
                number = number + 1
            else:
                max1 = 0
                for k in range(1, number):
                    if (float(rsheet.cell(numberofperformance[max1], 2).value) < float(
                            rsheet.cell(numberofperformance[k], 2).value)):
                        max1 = k
                if (float(rsheet.cell(rowcounter, 2).value) < float(rsheet.cell(numberofperformance[max1], 2).value)):
                    numberofperformance[max1] = rowcounter
    for k in range(0, number):
        info_about_performance_one(message, rsheet, numberofperformance[k])


# Поиск представлений по рейтингу выше введенного пользователем????
# Сначала выбирается высокий рейтинг, затем самые низкие цены
def search_for_performance_by_rating_with_price2(message, rsheet):
    numberofperformance = [0, 0, 0, 0, 0]
    number = 0
    for rowcounter in range(1, rsheet.nrows):
        if (float(message.text) <= float(rsheet.cell(rowcounter, 6).value)):
            if (number < 5):
                numberofperformance[number] = rowcounter
                number = number + 1
            else:
                minr1 = 0
                for k in range(1, number):
                    # ищем самый низкий рейтинг, если самых низких - 2, то ищем самую высокую цену
                    if (float(rsheet.cell(numberofperformance[minr1], 6).value) >= float(
                            rsheet.cell(numberofperformance[k], 6).value)):
                        # minr1=k
                        if (float(rsheet.cell(numberofperformance[minr1], 6).value) == float(
                                rsheet.cell(numberofperformance[k], 6).value)):
                            if (float(rsheet.cell(numberofperformance[minr1], 2).value) <= float(
                                    rsheet.cell(numberofperformance[k], 2).value)):
                                minr1 = k
                        else:
                            minr1 = k
                if (float(rsheet.cell(rowcounter, 6).value) == float(rsheet.cell(numberofperformance[minr1], 6).value)):
                    if (float(rsheet.cell(rowcounter, 2).value) <= float(
                            rsheet.cell(numberofperformance[minr1], 2).value)):
                        numberofperformance[minr1] = rowcounter
                elif (float(rsheet.cell(rowcounter, 6).value) > float(
                        rsheet.cell(numberofperformance[minr1], 6).value)):
                    numberofperformance[minr1] = rowcounter
    for k in range(0, number):
        info_about_performance_one(message, rsheet, numberofperformance[k])


# Поиск спектаклей с самым высоким рейтингом. Может добавить возможность ввода количества выводимых спектаклей?
def search_for_performance_by_the_highest_rating_with_price(message, rsheet):
    numberofperformance = [0, 0, 0, 0, 0]
    number = 0
    for rowcounter in range(1, rsheet.nrows):
        if (number < 5):
            numberofperformance[number] = rowcounter
            number = number + 1
        else:
            minr1 = 0
            for k in range(1, number):
                # ищем самый низкий рейтинг, если самых низких - 2, то ищем самую высокую цену
                if (float(rsheet.cell(numberofperformance[minr1], 6).value) >= float(
                        rsheet.cell(numberofperformance[k], 6).value)):
                    # minr1=k
                    if (float(rsheet.cell(numberofperformance[minr1], 6).value) == float(
                            rsheet.cell(numberofperformance[k], 6).value)):
                        if (float(rsheet.cell(numberofperformance[minr1], 2).value) <= float(
                                rsheet.cell(numberofperformance[k], 2).value)):
                            minr1 = k
                    else:
                        minr1 = k
            if (float(rsheet.cell(rowcounter, 6).value) == float(rsheet.cell(numberofperformance[minr1], 6).value)):
                if (float(rsheet.cell(rowcounter, 2).value) <= float(rsheet.cell(numberofperformance[minr1], 2).value)):
                    numberofperformance[minr1] = rowcounter
            elif (float(rsheet.cell(rowcounter, 6).value) > float(rsheet.cell(numberofperformance[minr1], 6).value)):
                numberofperformance[minr1] = rowcounter
    for k in range(0, number):
        info_about_performance_one(message, rsheet, numberofperformance[k])


# ДАТА
# Поиск спектаклей по введенной дате, при выборе сначала учитывается цена, а затем - рейтинг
def search_for_performances_by_date(message, rsheet, daymonthyear):
    numberofperformance = [0, 0, 0, 0, 0]
    number = 0
    for rowcounter in range(1, rsheet.nrows):
        daymonthyearexl = converting_a_date_string_to_numbers(rsheet, rowcounter)
        # print(daymonthyearexl)
        if (daymonthyear[1] == daymonthyearexl[1]):
            # if((daymonthyear[2]==daymonthyearexl[2]) and (daymonthyear[1]==daymonthyearexl[1])):
            if (daymonthyear[0] == daymonthyearexl[0]):
                print(daymonthyearexl)
                if (number < 5):
                    numberofperformance[number] = rowcounter
                    number += 1
                else:
                    numberofperformance = selection_first_by_price_then_by_rating(rsheet, number, numberofperformance,
                                                                                  rowcounter)
    for k in range(0, number):
        info_about_performance_one(message, rsheet, numberofperformance[k])


# Поиск ближайших дат втечении недели, но акцент на цену, затем на рейтинг, а даты не смотрятся сааааамые ближайшие
# Не будет работать, если сейчас конец месяа, надо прописать данную ситуаию отдельно + добавить учитывание года
def search_for_performances_by_the_nearest_date(message, rsheet):
    numberofperformance = [0, 0, 0, 0, 0]
    number = 0

    now = datetime.datetime.now()
    daymonthyearnow = [now.day, now.month, now.year]
    print(daymonthyearnow)

    for rowcounter in range(1, rsheet.nrows):
        daymonthyearexl = converting_a_date_string_to_numbers(rsheet, rowcounter)
        if (daymonthyearexl[1] == daymonthyearnow[1]):
            # if((daymonthyear[2]==daymonthyearexl[2]) and (daymonthyear[1]==daymonthyearexl[1])):
            if (((daymonthyearexl[0] - daymonthyearnow[0]) <= 7) and ((daymonthyearexl[0] - daymonthyearnow[0]) >= 0)):
                if (number < 5):
                    numberofperformance[number] = rowcounter
                    number += 1
                else:
                    numberofperformance = selection_first_by_price_then_by_rating(rsheet, number, numberofperformance,
                                                                                  rowcounter)
    for k in range(0, number):
        info_about_performance_one(message, rsheet, numberofperformance[k])


# Отбор по самой низкой цене, затем по самому высокому рейтингу
# Ищет номер строки с наибольшей стоимостью, затем заменяет на текущую строку, которая до этого прошла условия отбора
def selection_first_by_price_then_by_rating(rsheet, number, numberofperformance, rowcounter):
    maxk = 0
    for k in range(1, number):
        if (float(rsheet.cell(numberofperformance[maxk], 2).value) < float(
                rsheet.cell(numberofperformance[k], 2).value)):
            maxk = k
        elif (float(rsheet.cell(numberofperformance[maxk], 2).value) == float(
                rsheet.cell(numberofperformance[k], 2).value)):
            if (float(rsheet.cell(numberofperformance[maxk], 6).value) <= float(
                    rsheet.cell(numberofperformance[k], 6).value)):
                maxk = k
    if (float(rsheet.cell(numberofperformance[maxk], 2).value) > float(rsheet.cell(rowcounter, 2).value)):
        numberofperformance[maxk] = rowcounter
    elif (float(rsheet.cell(numberofperformance[maxk], 2).value) == float(rsheet.cell(rowcounter, 2).value)):
        if (float(rsheet.cell(numberofperformance[maxk], 6).value) <= float(rsheet.cell(rowcounter, 6).value)):
            numberofperformance[maxk] = rowcounter
    return numberofperformance


# НАЗВАНИЕ
# Поиск представления по названию. Ищет самую низкую цену.
def search_performance_for_name(message, rsheet):
    numberofperformancewithminprice = 0
    messagestr = str(message.text)
    count = 0

    for rowcounter in range(1, rsheet.nrows):
        if (messagestr == rsheet.cell(rowcounter, 0).value):
            if (count == 0):
                numberofperformancewithminprice = rowcounter
                count += 1
            else:
                if (float(rsheet.cell(numberofperformancewithminprice, 2).value) > float(
                        rsheet.cell(rowcounter, 2).value)):
                    numberofperformancewithminprice = rowcounter
    if (count != 0):
        bot.send_message(message.chat.id, 'Вот, что у меня получилось найти!')
        info_about_performance_one(message, rsheet, numberofperformancewithminprice)
    else:
        bot.send_message(message.chat.id, 'Прости, но я ничего не знаю об этом спектакле.')


if __name__ == '__main__':
    bot.polling(none_stop=True)
