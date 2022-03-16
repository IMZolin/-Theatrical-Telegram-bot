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

def InformationInFile():
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
        performance_min_discription = performance.find("div", class_="_3Di4D _2qUBY")
        performance_rating = performance.find("span", class_="_1g1fp ql7kl _3EZKc _1JPCS _20dAu _3VWPW _12fWX")
        if (performance.find("span", class_="_1gC4P")):
            performance_day_all = performance.find("span", class_="_1gC4P")
            str_day = performance_day_all.get_text()
            performance_day = ""
            i = 0
            while str_day[i] != ",":
                performance_day += str_day[i]
                i += 1

        if (performance.find("span", class_="_21BWX _2O1ut _1lIKZ bsB4F")):
            performance_price = performance.find("span", class_="_21BWX _2O1ut _1lIKZ bsB4F").find("span")
        performance_urls = "https://www.afisha.ru" + performance.find("div", class_="_1V-Pk").find("a").get("href")

        if (
                performance_name and performance_min_discription and performance_theatre and performance_rating and performance_urls and performance_price):
            performance_data_list.append(
                {
                    "Название спектакля:": performance_name.text,
                    "День и время:": performance_day,
                    "Жанр:": performance_genre.text,
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
    InformationInFile()
    ConvertToExcel()

main()

# "#Выводим основную информацию с главной страницы"
    #     print(f"Название спектакля: {performance_name.text}")
    #     print(f"Рейтинг:{performance_rating.text}")
    #     print(f"Дата: {performance_day}")
    #     print(f"Цена:{performance_price.text}")
    #     print(performance_urls)
    #     print(f"Жанр: {performance_genre.text}")
    #     print(f"Театр: {performance_theatre.text}")
    #     print(f"Описание: {performance_min_discription.text}")
    #     print("\n")
    # else:
    #     print(f"Название спектакля: {performance_name.text}")
    #     print(performance_urls)
    #     print(f"Цена: {performance_price.text}")
    #     print(f"Дата: {performance_day}")
    #     #print(f"Рейтинг:{performance_rating.text}")
    #     print(f"Жанр: {performance_genre.text}")
    #     print(f"Театр: {performance_theatre.text}")
    #     print(f"Описание: {performance_min_discription.text}")
    #     print("\n")

#Создаём словарь из ссылок на спектакли"
    # all_performance_hrefs = soup.find_all(class_="_3NqYW DWsHS _3lmHp wkn_c")
    # all_performance_dict = {}
    # for item in all_performance_hrefs:
    #     item_text = item.text
    #     item_href = "https://www.afisha.ru" + item.get("href")
    #     print(f"{item_text}: {item_href}")
    #     all_performance_dict[item_text] = item_href

# with open("all_performance_dict.json",encoding='utf-8') as file:
#     all_performances = json.load(file)
#print(all_performances)
# count = 0
# for per_name, per_href in all_performances.items():
#     req = requests.get(url=per_href, headers=headers)
#     src = req.text
#     if count == 0:
#         with open(f"data/{count} {per_name}.html", "w", encoding='utf-8') as file:
#             file.write(src)




# if(performance_urls):
#     for performance_url in performance_urls:
#         #req = requests.get(performance_url, headers)
#         req = requests.get(performance_url, headers)
#         performance_url_name = performance_url.split("/")[-2]
#
#         with open(f"{performance_url_name}.html", "w") as file:
#             file.write(req.text)
#     with open(f"{performance_url_name}.html") as file:
#         src=file.read()