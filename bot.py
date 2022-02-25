# -*- coding: cp1251 -*-
# -*- coding: utf-8 -*-
import telebot  # импорт pyTelegramBotAPI
from telebot import types  # также достанем типы
import random  # рандом обязательно
import xlrd  # библиотка чтения экселевских файлов

# import pandas as pn
from xlrd.xldate import xldate_as_datetime
import time
import datetime

from config import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Привет! Я Театральный Telegram-бот Тиа, и моя задача - помочь тебе быстро и просто выбрать, куда сходить, чтобы весело провести время!")  # Привет! Я Telegram-бот версии 2.0!


@bot.message_handler(commands=['button'])
def button_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Жанры")
    item2 = types.KeyboardButton("Режиссура")
    item3 = types.KeyboardButton("Театр")
    item4 = types.KeyboardButton("Цены")
    item5 = types.KeyboardButton("Описание")
    item = types.KeyboardButton("ИНФО")
    markup.add(item1, item2, item3, item4, item5)
    markup.add(item)
    bot.send_message(message.chat.id, 'Ты находишься в главном меню! Здесь можно выбрать, какие подборки мне показать.',
                     reply_markup=markup)
    bot.send_message(message.chat.id, 'Если хочешь узнать, какая кнопка за что отвечает, просто нажми "ИНФО"')


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Старт":
        send_welcome_in_Russian(message)

    if message.text == "Жанры":
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

    elif message.text == "Режиссура":
        bot.send_message(message.chat.id,
                         'Ого! У тебя есть любимый режиссёр? Это здорово! Просто введи его фамилию и имя, а я уже постараюсь найти что-нибудь для тебя!')

    elif message.text == "Театр":
        bot.send_message(message.chat.id, 'Хочешь сходить в какой-то определенный театр?')
        bot.send_message(message.chat.id,
                         'Понимаю, мне тоже не нравится стоять в часовых пробках, или толкаться в метро. Хотя... Может ты хочешь с головой окунуться в волшебную атмосферу театра?')

    elif message.text == "Цены":
        message_answer_prise(message)

    elif message.text == "Описание":
        bot.send_message(message.chat.id,
                         'Хочешь узнать подробнее о представлении? Без проблем! Просто введи его название.')
        bot.register_next_step_handler(message, message_answer_description)

    elif message.text == "Вернуться в главное меню":
        button_main_menu(message)


    elif message.text == "Дата":
        bot.send_message(message.chat.id, 'Хорошо! Сейчас я постараюсь тебе что-нибудь подобрать!')
        bot.send_message(message.chat.id, 'Напиши, какая дата тебя интересует. Например: 17 марта 2022')
        bot.register_next_step_handler(message, message_answer_date)


def send_welcome_in_Russian(message):
    bot.send_message(message.chat.id,
                     "Привет! Я Театральный Telegram-бот Тиа, и моя задача - помочь тебе быстро и просто выбрать, куда сходить, чтобы весело провести время!")  # Привет! Я Telegram-бот версии 2.0!


def message_answer_prise(message):
    # if message.text=="Цены":
    markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttonprice1 = types.KeyboardButton("Выбор по цене")
    buttonprice2 = types.KeyboardButton("Узнать цену")
    buttonprice3 = types.KeyboardButton("Вернуться в главное меню")
    markup3.add(buttonprice1, buttonprice2)
    markup3.add(buttonprice3)
    bot.send_message(message.chat.id,
                     'Я изо всех сил постараюсь помочь тебе подобрать интересное театральное представление по идеальной цене!',
                     reply_markup=markup3)


def message_answer_description(message):
    rb = xlrd.open_workbook(
        "NameAndDescription2.xls")
    sheet = rb.sheet_by_index(0)
    success = 0

    # bot.send_message(message.chat.id, 'Ты ввёл:')
    # bot.send_message(message.chat.id, message.text)

    for rowcounter in range(sheet.nrows):
        nameofthepresentation = sheet.cell(rowcounter, 0).value
        if nameofthepresentation == message.text:
            descriptionofthepresentation = sheet.cell(rowcounter, 1).value
            bot.send_message(message.chat.id, descriptionofthepresentation)
            success = 1
            return
    if success == 0:
        bot.send_message(message.chat.id, 'Прости, но я пока ничего не знаю об этом представлении.')
    bot.send_message(message.chat.id, 'конец цикла!')


def message_answer_date(message):
    # На вход дата, на выход - краткая информация о спектакле
    rb = xlrd.open_workbook(
        "NameAndDescription2.xls")
    sheet = rb.sheet_by_index(0)
    success = 0

    # number=bot.register_next_step_handler(message, callback)
    # bot.send_message(message.chat.id, number)
    # bot.send_message(message.chat.id, message.text)

    for rowcounter in range(1, sheet.nrows):
        dateofthepresentation = sheet.cell(rowcounter, 6).value

        if dateofthepresentation == message.text:
            message_info_about_presentation(message, rowcounter, sheet)
            success = success + 1
            if (success > 5):
                return
    if success == 0:
        bot.send_message(message.chat.id, 'Прости, но я не знаю, проводятся ли представления в эту дату.')
    # bot.send_message(message.chat.id, 'конец цикла!')


def message_info_about_presentation(message, rowcounter, sheet):
    nameofthepresentation = sheet.cell(rowcounter, 0).value
    priceofthepresentation = sheet.cell(rowcounter, 2).value

    timeofthepresentation = sheet.cell(rowcounter, 4).value
    python_time = xldate_as_datetime(float(timeofthepresentation), 0)

    dateofthepresentation2 = sheet.cell(rowcounter, 5).value
    # Преобразование в дату данных из экселя
    python_datetime = xldate_as_datetime(float(dateofthepresentation2), 0)

    genreofthepresentation = sheet.cell(rowcounter, 8).value
    linkofthepresentation = sheet.cell(rowcounter, 15).value
    bot.send_message(message.chat.id,
                     f"Название: {nameofthepresentation}\nДата: {python_datetime.strftime('%d.%m.%Y')}\nВремя: {python_time.strftime('%H:%M')}\nМинимальная цена билета: {priceofthepresentation}\nЖанр: {genreofthepresentation}\nСсылка: {linkofthepresentation}")


if __name__ == '__main__':
    bot.polling(none_stop=True)