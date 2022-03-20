import requests
import json
import pandas as pd
from bs4 import BeautifulSoup

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

def InformationInFile(soup):
    genre = ""
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
            #print(all_day_list)
            str_day = all_day_list[0]
            #print(str_day)
            str_day_list = str_day.split(' ')
            if(str_day_list[0] == 'Сегодня'):
                performance_day = str_day_list[0]
            else:
                performance_day = str_day_list[0] + ' ' + str_day_list[1]
            #print(str_day_list)
            #performance_time = str_day_list[2]
            print(performance_day)

            if (str_day_list[1] == 'в'):
                performance_time = str_day_list[2]
            else:
                performance_time = str_day_list[3]
            print(performance_time)

        if (performance.find("span", class_="_21BWX _2O1ut _1lIKZ bsB4F")):
            performance_price = performance.find("span", class_="_21BWX _2O1ut _1lIKZ bsB4F").find("span")
        performance_urls = "https://www.afisha.ru" + performance.find("div", class_="_1V-Pk").find("a").get("href")
        if (
                performance_name and performance_min_discription and performance_theatre and performance_rating and performance_urls and performance_price):
            performance_data_list.append(
                {
                    "Название спектакля:": performance_name.text,
                    #"День и время:": performance_day,
                    "Дата:": performance_day,
                    "Время:": performance_time,
                    "Жанр:": genre,
                    "Рейтинг:": performance_rating.text,
                    "Цена:": performance_price.text,
                    "Театр:": performance_theatre.text,
                    "Описание:": performance_min_discription.text,
                    "URL спектакля:": performance_urls,
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