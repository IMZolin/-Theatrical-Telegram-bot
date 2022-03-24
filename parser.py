import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date, timedelta

def GetHTML():
    url = 'https://www.afisha.ru/spb/schedule_theatre/'
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    }
    req = requests.get(url, headers)
    src =req.text
    #print(src)
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(src)
    with open('index.html', 'r', encoding='utf-8') as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    return soup

def ConvertToExcel():
    with open("all_performance_dict.json", "r", encoding='utf-8') as file:
        df_json = pd.read_json("all_performance_dict.json")
        df_json.to_excel("all_performance_dict.xlsx")

def GetPage(url):
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    }
    req = requests.get(url, headers)
    src = req.text
    performance_url_name = url.split("/")[-2]
    with open(f"data/{performance_url_name}.html", "w", encoding="utf-8") as file:
        file.write(src)
    with open(f"data/{performance_url_name}.html", 'r', encoding='utf-8') as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    return [soup, performance_url_name]

def GetIngormationFromPage(soup, performance_url_name):
    with open(f"data/{performance_url_name}.html", 'r', encoding='utf-8') as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    additional_inf_performances = []
    performance_data = soup.find_all("span", class_="_1gC4P")
    performance_age = performance_data[1]
    performance_place_adress = soup.find("div", class_="_2jztV _2Nzs2 _2XtXq")
    performance_place_metro = performance_place_adress.find_next()
    soup.find("div", class_="_3NqYW G_0Rp")
    performance_duration = performance_data[3]
    # if(performance_data[2].find("назад")):
    #     performance_duration = performance_data[1].get_text()
    # else:
    #     performance_duration = performance_data[3]
    # if(performance_data[2].find("назад")):
    #     performance_duration = performance_data[1]
    # elif(performance_data[2].find(",") ):
    #     performance_duration = performance_data[2]
    #
    # else:
    #     performance_duration = performance_data[3]

    performance_adress = performance_place_adress.find("span", class_="_1gC4P")
    performance_undeground = performance_place_metro.find("span", class_="_3OB5r")

    return [performance_age.get_text(), performance_adress.get_text(),performance_duration.get_text()]

def InformationInFile(soup):
    genre = ""
    adress = ""
    duration = ""
    age =""
    pages = 49
    performance_data_list = []
    with open("index.html", encoding='utf-8') as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    performances = soup.find_all("div", class_="_1kwbj lkWIA _2Ds3f")
    for performance in performances:
        performance_name = performance.find("a", class_="_3NqYW DWsHS _3lmHp wkn_c")
        performance_theatre = performance.find("a", class_="_3NqYW G_0Rp")
        performance_genre = performance.find("a", class_="_3NqYW G_0Rp").find_next()
        if(performance_genre.text == "Драматический"):
            genre = performance_genre.text
            genre = genre.replace(genre, "Драма")
            #print(genre)
            # performance_genre.text = genre;
        if (performance_genre.text == "Кукольный"):
            genre = performance_genre.text
            genre = genre.replace(genre, "Кукольный спектакль")
            # performance_genre.text = genre;
        if (performance_genre.text != "Кукольный" and performance_genre.text != "Драматический"):
            genre = performance_genre.text
        performance_min_discription = performance.find("div", class_="_3Di4D _2qUBY")
        performance_rating = performance.find("span", class_="_1g1fp ql7kl _3EZKc _1JPCS _20dAu _3VWPW _12fWX")

        if (performance.find("span", class_="_1gC4P")):
            performance_day_all = performance.find("span", class_="_1gC4P")
            all_day = performance_day_all.get_text()
            all_day_list = all_day.split(',')
            performance_time = ""
            performance_day = ""
            str_day = all_day_list[0]
            str_day_list = str_day.split(' ')
            if(str_day_list[0] == 'Сегодня'):
                performance_day = str_day_list[0]
                #performance_day = date.today()
            elif (str_day_list[0] == 'Завтра'):
                performance_day = str_day_list[0]
                #performance_day = date.today()
                #performance_day = date.today() + timedelta(days=1)
            else:
                performance_day = str_day_list[0] + ' ' + str_day_list[1]

            if (str_day_list[1] == 'в'):
                performance_time = str_day_list[2]
            else:
                performance_time = str_day_list[3]

        if (performance.find("span", class_="_21BWX _2O1ut _1lIKZ bsB4F")):
            performance_price = performance.find("span", class_="_21BWX _2O1ut _1lIKZ bsB4F").find("span")
            all_price = performance_price.get_text()
            all_price_list = all_price.split(' ')
            price = all_price_list[1]

        performance_urls = "https://www.afisha.ru" + performance.find("div", class_="_1V-Pk").find("a").get("href")

        age = GetIngormationFromPage(GetPage(performance_urls)[0],GetPage(performance_urls)[1])[0]
        adress_all = GetIngormationFromPage(GetPage(performance_urls)[0], GetPage(performance_urls)[1])[1]
        adress_list = adress_all.split(' ')
        adress = adress_all
        if(len(adress_list) == 3):
            if(adress_list[2] == 'назад'):
                #print(adress_list)
                adress = -1

        duration_all = GetIngormationFromPage(GetPage(performance_urls)[0], GetPage(performance_urls)[1])[2]
        duration_list = duration_all.split(' ')
        duration = duration_all
        if (len(duration_list) == 3):
            print(duration_list)
            duration = -1
        if(len(duration_list) == 2):
            duration = -1

        if (
                performance_name and performance_min_discription and performance_theatre and performance_rating and performance_urls and performance_price):
            performance_data_list.append(
                {
                    "Название": performance_name.text,
                    "Описание": performance_min_discription.text,
                    "Цена от": price,
                    "Время начала": performance_time,
                    "Дата словами": performance_day,
                    "Жанр": genre,
                    "Рейтинг": performance_rating.text,
                    "Ссылка": performance_urls,
                    "Театр": performance_theatre.text,
                    "Возрастное ограничение": age,
                    "Адрес театра": adress,
                    "Продолжительность": duration,
                    #"Длительность": duration,
                    #"Метро": undeground,

                }
            )
    print(performance_data_list)
    with open("all_performance_dict.json", "w", encoding='utf-8') as file:
        json.dump(performance_data_list, file, indent=4, ensure_ascii=False)
        # data=json.load(file)
        # df=pd.DataFrame(data)
        # df.to_excel("performance_list.xlsx")


def main():
    GetHTML()
    InformationInFile(GetHTML())
    ConvertToExcel()

main()