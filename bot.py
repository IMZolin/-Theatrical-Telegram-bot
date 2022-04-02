# -*- coding: cp1251 -*-
# -*- coding: utf-8 -*-
from os import kill
import telebot  # ������ pyTelegramBotAPI
from telebot import types  # ����� �������� ����
import xlrd  # ��������� ������ ����������� ������
from xlrd.xldate import xldate_as_datetime

import datetime

from config import TOKEN

bot = telebot.TeleBot(TOKEN)


# �������
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "������! � ����������� Telegram-��� ���, � ��� ������ - ������ ���� ������ � ������ �������, ���� �������, ����� ������ �������� �����!")  # ������! � Telegram-��� ������ 2.0!


@bot.message_handler(commands=['help'])
def send_message_after_help(message):
    bot.send_message(message.chat.id, '��� ������ ���� �������� ������')


@bot.message_handler(commands=['buttons'])
def button_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("��������")
    item2 = types.KeyboardButton("�������")
    item3 = types.KeyboardButton("�����")
    item4 = types.KeyboardButton("����")
    item5 = types.KeyboardButton("����")
    item6 = types.KeyboardButton("�����")
    item7 = types.KeyboardButton("�������")
    item = types.KeyboardButton("����")
    markup.add(item1, item2, item3, item4, item5)
    markup.add(item6, item7)
    markup.add(item)
    bot.send_message(message.chat.id, '�� ���������� � ������� ����! ����� ����� �������, ����� �������� ��� ��������.',
                     reply_markup=markup)
    bot.send_message(message.chat.id, '���� ������ ������, ����� ������ �� ��� ��������, ������ ����� "����"')


@bot.message_handler(content_types='text')
def message_reply(message):
    rb = xlrd.open_workbook("D:/_New/Program vs/bot/ticketland_parsing_2.xlsx")
    rsheet = rb.sheet_by_index(0)

    # ������� �������
    if message.text == "�����":
        send_welcome(message)
    elif message.text == "������":
        button_main_menu(message)
    elif (
            message.text == "����" or message.text == "����" or message.text == "������" or message.text == "������" or message.text == "help" or message.text == "help me"):
        send_message_after_help(message)

    # ������� ������
    elif message.text == "��������":
        bot.send_message(message.chat.id,
                         '������ ������ ��������� � �������������? ��� �������! ������ ����� ��� ��������.')
        bot.register_next_step_handler(message, search_performance_for_name, rsheet)
    elif message.text == "�������":
        message_answer_rating(message)
    elif message.text == "�����":
        message_answer_genre(message)
    elif message.text == "����":
        message_answer_date(message)
    elif message.text == "����":
        message_answer_prise(message)
    elif message.text == "�����":
        bot.send_message(message.chat.id, '������ ������� � �����-�� ������������ �����?')
        bot.send_message(message.chat.id,
                         '�������, ��� ���� �� �������� ������ � ������� �������, ��� ��������� � �����. ����... ����� �� ������ � ������� ��������� � ��������� ��������� ������?')
    elif message.text == "�������":
        bot.send_message(message.chat.id, '������ ������� �� ��������� � ������ ��������?')
    elif message.text == "����":
        bot.send_message(message.chat.id, '����� ������ ���� ���-������ ��������, ��� ����� �������� ������������')

    # ������� � ������� ����
    elif message.text == "��������� � ������� ����":
        button_main_menu(message)

    # �������������� ������

    # �������
    elif message.text == "������� ��":
        bot.send_message(message.chat.id, '��� ����, ����� � ���-������ �����, ������ ����� ����� �� 1 �� 10')
        bot.register_next_step_handler(message, search_for_performance_by_rating_with_price, rsheet)
    elif message.text == "5 ���������� � ����� ������� ���������":
        bot.send_message(message.chat.id, '���, ��� � ������ �����:')
        search_for_performance_by_the_highest_rating_with_price(message, rsheet)

    # ����
    elif message.text == "����� �� ����":
        bot.send_message(message.chat.id, '������! ������ � ���������� ���� ���-������ ���������!')
        bot.send_message(message.chat.id, '������, ����� ���� ���� ����������. ��������: 17 ����� 2022')
        bot.register_next_step_handler(message, input_the_date2, rsheet)
    elif message.text == "��������� ����":
        bot.send_message(message.chat.id, '���, ��� ��� ������� �����!')
        search_for_performances_by_the_nearest_date(message, rsheet)


# �������� �� ��������� "�������"
def message_answer_rating(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttongenre1 = types.KeyboardButton("������� ��")
    buttongenre2 = types.KeyboardButton("5 ���������� � ����� ������� ���������")
    buttongenre3 = types.KeyboardButton("��������� � ������� ����")
    markup.add(buttongenre1, buttongenre2)
    markup.add(buttongenre3)
    bot.send_message(message.chat.id,
                     '�� �� ������� "�������". ����� �� ������ �������, ��� ��� �������� - 5 ���������� � ���������, ���������� ��� ��������� �����, ��� 5 ���������� � ����� ������� ���������.',
                     reply_markup=markup)
    bot.send_message(message.chat.id,
                     '��, ��, � ����������� ��������� ������������� � ����� ������ �����! �������, ���� ���-������ ����������!')


# �������� �� ��������� "����"
def message_answer_genre(message):
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


# �������� �� ��������� "����"
def message_answer_date(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttongenre1 = types.KeyboardButton("��������� ����")
    buttongenre2 = types.KeyboardButton("����� �� ����")
    buttongenre3 = types.KeyboardButton("��������� � ������� ����")
    markup.add(buttongenre1, buttongenre2)
    markup.add(buttongenre3)
    bot.send_message(message.chat.id,
                     '�� �� ������� "����". ��� � ���� ��������� ��������� � ��������� ����, ��� �� � �����-������ ������������!',
                     reply_markup=markup)


# �������� �� ��������� "����"
def message_answer_prise(message):
    markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttonprice1 = types.KeyboardButton("����� �� ����")
    buttonprice2 = types.KeyboardButton("������ ����")
    buttonprice3 = types.KeyboardButton("��������� � ������� ����")
    markup3.add(buttonprice1, buttonprice2)
    markup3.add(buttonprice3)
    bot.send_message(message.chat.id,
                     '� ��� ���� ��� ���������� ������ ���� ��������� ���������� ����������� ������������� �� ��������� ����!',
                     reply_markup=markup3)


# �������������� �������
# ������� ��� ��������� ���������� � ���������
def info_about_performance_one(message, rsheet, rownumber):
    performancentmp = rsheet.row_values(rownumber, 0, 13)
    str1 = ''
    strdescription = ''
    str2 = ''
    if (performancentmp[0] != -1):
        str1 += "��������: " + performancentmp[0] + "\n"
    if (performancentmp[1] != -1):
        strdescription += "��������: " + performancentmp[1] + "\n"
    if (performancentmp[5] != -1):
        str1 += "����: " + performancentmp[5] + "\n"
    if (performancentmp[6] != '-1'):
        str1 += "�������: " + str(performancentmp[6]) + "\n"
    if (performancentmp[9] != -1):
        str1 += "���������� �����������: " + performancentmp[9] + "\n"
    if (performancentmp[4] != -1):
        str1 += "��������� ����: " + performancentmp[4] + "\n"
    if (performancentmp[3] != -1):
        str1 += "�����: " + performancentmp[3] + "\n"
    if (performancentmp[11] != -1):
        str1 += "�����������������: " + performancentmp[11] + "\n"
    if (performancentmp[2] != -1):
        str1 += "����: " + performancentmp[2] + "\n"
    if (performancentmp[7] != -1):
        str1 += "�����: " + performancentmp[7] + "\n"
    if (performancentmp[10] != -1):
        str1 += "�����: " + performancentmp[10] + "\n"
    if (performancentmp[12] != -1):
        str2 += "������ ����: " + performancentmp[12] + "\n"
    if (performancentmp[8] != -1):
        str2 += "������: " + performancentmp[8] + "\n"
    bot.send_message(message.chat.id, f"{str1}{strdescription}{str2}")
    # 0 ��������.  1 ��������.  2 ���� ��.  3 ����� ������.
    # 4 ���� �������.  5 ����.  6 �������.  7 �����.  8 ������.  9 ���������� �����������.  10 �����
    # 11 ����������������� 12 ������ ���� � �����


# ������ ���� �� ����� � ������� � � ������ - ����, �����, ���.
def converting_a_date_string_to_numbers(rsheet, rownumber):
    strdate = rsheet.cell(rownumber, 4).value
    daymonthyearstr = strdate.split(".")
    daymonthyear = [-1, -1, -1]
    daymonthyear[0] = int(daymonthyearstr[0])
    daymonthyear[1] = int(daymonthyearstr[1])
    daymonthyear[2] = int(daymonthyearstr[2]) + 2000
    return daymonthyear


# ���������� ������, ��������� �������������.
# ������� ��������� ����, ��������� ������������� � ����� - ����, �����, ���
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
                         f"���� ������� ����� ����, �����?\n {daymonthyear[0]}.{daymonthyear[1]}.{daymonthyear[2]} ")
    return daymonthyear


# ������� ���������� ������������� ������ � �����.
def converting_a_month_to_numbers(strmonth):
    monthnumber = -1
    if ((strmonth == '������') or (strmonth == '���') or (strmonth == '01') or (strmonth == '1')):
        monthnumber = 1
    elif ((strmonth == '�������') or (strmonth == '���') or (strmonth == '02') or (strmonth == '2')):
        monthnumber = 2
    elif ((strmonth == '�����') or (strmonth == '���') or (strmonth == '03') or (strmonth == '3')):
        monthnumber = 3
    elif ((strmonth == '������') or (strmonth == '���') or (strmonth == '04') or (strmonth == '4')):
        monthnumber = 4
    elif ((strmonth == '���') or (strmonth == '���') or (strmonth == '05') or (strmonth == '5')):
        monthnumber = 5
    elif ((strmonth == '����') or (strmonth == '���') or (strmonth == '06') or (strmonth == '6')):
        monthnumber = 6
    elif ((strmonth == '����') or (strmonth == '���') or (strmonth == '07') or (strmonth == '7')):
        monthnumber = 7
    elif ((strmonth == '�������') or (strmonth == '���') or (strmonth == '08') or (strmonth == '8')):
        monthnumber = 8
    elif ((strmonth == '��������') or (strmonth == '���') or (strmonth == '09') or (strmonth == '9')):
        monthnumber = 9
    elif ((strmonth == '�������') or (strmonth == '���') or (strmonth == '10') or (strmonth == '10')):
        monthnumber = 10
    elif ((strmonth == '������') or (strmonth == '���') or (strmonth == '11') or (strmonth == '11')):
        monthnumber = 11
    elif ((strmonth == '�������') or (strmonth == '���') or (strmonth == '12') or (strmonth == '12')):
        monthnumber = 12
    return monthnumber


s = 0


# ���� ���� �� ������������. �� ������ ������ ��������, ���� ��� ������ �� �����!!
def input_the_date2(message, rsheet):
    daymonthyear = [-1, -1, -1]
    global s
    daymonthyear = converting_a_message_string_to_numbers2(message)
    if daymonthyear[0] != -1:
        s = 1
    if (s == 0):
        # print("HELLO")
        bot.send_message(message.chat.id, '������, �� � ���� ������� �� ������, ������ ���������?')
        bot.register_next_step_handler(message, input_the_date2, rsheet)
        # print("hello2")
    else:
        # print("poisk po date")
        bot.send_message(message.chat.id, '���, ��� � ���� ���������� �����!')
        search_for_performances_by_date(message, rsheet, daymonthyear)
    s = 0
    print("end")


# ����� �� ������ ���������
# �������
# �������, ����� �������, ����� ����� ������ ����
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


# ����� ������������� �� �������� ���� ���������� �������������????
# ������� ���������� ������� �������, ����� ����� ������ ����
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
                    # ���� ����� ������ �������, ���� ����� ������ - 2, �� ���� ����� ������� ����
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


# ����� ���������� � ����� ������� ���������. ����� �������� ����������� ����� ���������� ��������� ����������?
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
                # ���� ����� ������ �������, ���� ����� ������ - 2, �� ���� ����� ������� ����
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


# ����
# ����� ���������� �� ��������� ����, ��� ������ ������� ����������� ����, � ����� - �������
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


# ����� ��������� ��� �������� ������, �� ������ �� ����, ����� �� �������, � ���� �� ��������� ��������� ���������
# �� ����� ��������, ���� ������ ����� �����, ���� ��������� ������ ������� �������� + �������� ���������� ����
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


# ����� �� ����� ������ ����, ����� �� ������ �������� ��������
# ���� ����� ������ � ���������� ����������, ����� �������� �� ������� ������, ������� �� ����� ������ ������� ������
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


# ��������
# ����� ������������� �� ��������. ���� ����� ������ ����.
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
        bot.send_message(message.chat.id, '���, ��� � ���� ���������� �����!')
        info_about_performance_one(message, rsheet, numberofperformancewithminprice)
    else:
        bot.send_message(message.chat.id, '������, �� � ������ �� ���� �� ���� ���������.')


if __name__ == '__main__':
    bot.polling(none_stop=True)
