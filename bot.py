# -*- coding: cp1251 -*-
# -*- coding: utf-8 -*-
import telebot  # ������ pyTelegramBotAPI
from telebot import types  # ����� �������� ����
import random  # ������ �����������
import xlrd  # ��������� ������ ����������� ������

# import pandas as pn
from xlrd.xldate import xldate_as_datetime
import time
import datetime

from config import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "������! � ����������� Telegram-��� ���, � ��� ������ - ������ ���� ������ � ������ �������, ���� �������, ����� ������ �������� �����!")  # ������! � Telegram-��� ������ 2.0!


@bot.message_handler(commands=['button'])
def button_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("�����")
    item2 = types.KeyboardButton("���������")
    item3 = types.KeyboardButton("�����")
    item4 = types.KeyboardButton("����")
    item5 = types.KeyboardButton("��������")
    item = types.KeyboardButton("����")
    markup.add(item1, item2, item3, item4, item5)
    markup.add(item)
    bot.send_message(message.chat.id, '�� ���������� � ������� ����! ����� ����� �������, ����� �������� ��� ��������.',
                     reply_markup=markup)
    bot.send_message(message.chat.id, '���� ������ ������, ����� ������ �� ��� ��������, ������ ����� "����"')


@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "�����":
        send_welcome_in_Russian(message)

    if message.text == "�����":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttongenre1 = types.KeyboardButton("�����")
        buttongenre2 = types.KeyboardButton("�������")
        buttongenre3 = types.KeyboardButton("������")
        buttongenre4 = types.KeyboardButton("�����")
        buttongenre5 = types.KeyboardButton("�����")
        buttongenre6 = types.KeyboardButton("��������� ���������")
        buttongenre7 = types.KeyboardButton("�����")
        buttongenre8 = types.KeyboardButton("��������� � ������� ����")
        markup.add(buttongenre1, buttongenre2, buttongenre3, buttongenre4)
        markup.add(buttongenre5, buttongenre6, buttongenre7, buttongenre8)
        bot.send_message(message.chat.id,
                         '�� �� ������� "�����". ����� ����, �� ������ ������� �����, ������ ���-�� ��������� �� �����������, ��� "����� � ���������", ��� ��, ��������, �� ���� ���������� ��� ��������� ������� "�������� ������"?',
                         reply_markup=markup)

    elif message.text == "���������":
        bot.send_message(message.chat.id,
                         '���! � ���� ���� ������� �������? ��� �������! ������ ����� ��� ������� � ���, � � ��� ���������� ����� ���-������ ��� ����!')

    elif message.text == "�����":
        bot.send_message(message.chat.id, '������ ������� � �����-�� ������������ �����?')
        bot.send_message(message.chat.id,
                         '�������, ��� ���� �� �������� ������ � ������� �������, ��� ��������� � �����. ����... ����� �� ������ � ������� ��������� � ��������� ��������� ������?')

    elif message.text == "����":
        message_answer_prise(message)

    elif message.text == "��������":
        bot.send_message(message.chat.id,
                         '������ ������ ��������� � �������������? ��� �������! ������ ����� ��� ��������.')
        bot.register_next_step_handler(message, message_answer_description)

    elif message.text == "��������� � ������� ����":
        button_main_menu(message)


    elif message.text == "����":
        bot.send_message(message.chat.id, '������! ������ � ���������� ���� ���-������ ���������!')
        bot.send_message(message.chat.id, '������, ����� ���� ���� ����������. ��������: 17 ����� 2022')
        bot.register_next_step_handler(message, message_answer_date)


def send_welcome_in_Russian(message):
    bot.send_message(message.chat.id,
                     "������! � ����������� Telegram-��� ���, � ��� ������ - ������ ���� ������ � ������ �������, ���� �������, ����� ������ �������� �����!")  # ������! � Telegram-��� ������ 2.0!


def message_answer_prise(message):
    # if message.text=="����":
    markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttonprice1 = types.KeyboardButton("����� �� ����")
    buttonprice2 = types.KeyboardButton("������ ����")
    buttonprice3 = types.KeyboardButton("��������� � ������� ����")
    markup3.add(buttonprice1, buttonprice2)
    markup3.add(buttonprice3)
    bot.send_message(message.chat.id,
                     '� ��� ���� ��� ���������� ������ ���� ��������� ���������� ����������� ������������� �� ��������� ����!',
                     reply_markup=markup3)


def message_answer_description(message):
    rb = xlrd.open_workbook(
        "NameAndDescription2.xls")
    sheet = rb.sheet_by_index(0)
    success = 0

    # bot.send_message(message.chat.id, '�� ���:')
    # bot.send_message(message.chat.id, message.text)

    for rowcounter in range(sheet.nrows):
        nameofthepresentation = sheet.cell(rowcounter, 0).value
        if nameofthepresentation == message.text:
            descriptionofthepresentation = sheet.cell(rowcounter, 1).value
            bot.send_message(message.chat.id, descriptionofthepresentation)
            success = 1
            return
    if success == 0:
        bot.send_message(message.chat.id, '������, �� � ���� ������ �� ���� �� ���� �������������.')
    bot.send_message(message.chat.id, '����� �����!')


def message_answer_date(message):
    # �� ���� ����, �� ����� - ������� ���������� � ���������
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
        bot.send_message(message.chat.id, '������, �� � �� ����, ���������� �� ������������� � ��� ����.')
    # bot.send_message(message.chat.id, '����� �����!')


def message_info_about_presentation(message, rowcounter, sheet):
    nameofthepresentation = sheet.cell(rowcounter, 0).value
    priceofthepresentation = sheet.cell(rowcounter, 2).value

    timeofthepresentation = sheet.cell(rowcounter, 4).value
    python_time = xldate_as_datetime(float(timeofthepresentation), 0)

    dateofthepresentation2 = sheet.cell(rowcounter, 5).value
    # �������������� � ���� ������ �� ������
    python_datetime = xldate_as_datetime(float(dateofthepresentation2), 0)

    genreofthepresentation = sheet.cell(rowcounter, 8).value
    linkofthepresentation = sheet.cell(rowcounter, 15).value
    bot.send_message(message.chat.id,
                     f"��������: {nameofthepresentation}\n����: {python_datetime.strftime('%d.%m.%Y')}\n�����: {python_time.strftime('%H:%M')}\n����������� ���� ������: {priceofthepresentation}\n����: {genreofthepresentation}\n������: {linkofthepresentation}")


if __name__ == '__main__':
    bot.polling(none_stop=True)