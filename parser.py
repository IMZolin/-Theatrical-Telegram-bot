import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time
import datetime
from dateutil.parser import parse

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

def GetPerformance(url):
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

def GetIngormationFromPerformance(soup, performance_url_name):
    with open(f"data/{performance_url_name}.html", 'r', encoding='utf-8') as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")
    additional_inf_performances = []
    performance_data1 = []
    performance_data2 = []
    performance_data = soup.find_all("span", class_="_1gC4P")
    performance_age = performance_data[1]
    performance_place_adress = soup.find("div", class_="_2jztV _2Nzs2 _2XtXq")
    soup.find("div", class_="_3NqYW G_0Rp")
    performance_data_right1 = performance_data[2].text
    performance_data_right2 = performance_data[3].text
    performance_data1 = performance_data_right1.split(' ')
    performance_data2 = performance_data_right2.split(' ')
    performance_duration = " "
    if(performance_data1[1] == "часа" or performance_data1[1] == "час" or performance_data1[1] == "час," or performance_data1[1] == "часа,"):
        performance_duration = performance_data[2].text
    if (performance_data2[1] == "часа" or performance_data2[1] == "час" or performance_data2[1] == "час," or performance_data2[1] == "часа,"):
        performance_duration = performance_data[3].text
    performance_adress = performance_place_adress.find("span", class_="_1gC4P")
    #print(performance_adress)
    return [performance_age.get_text(), performance_adress.get_text(),performance_duration]

def InformationInFile(soup):
    price=""
    genre = ""
    adress = ""
    duration = ""
    age =""
    today = datetime.datetime.today()
    tomorrow = today + datetime.timedelta(days=1)
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
        if (performance_genre.text == "Кукольный"):
            genre = performance_genre.text
            genre = genre.replace(genre, "Кукольный спектакль")
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
                performance_day = today.strftime("%d.%m.%Y")
            elif (str_day_list[0] == 'Завтра'):
                performance_day = tomorrow.strftime("%d.%m.%Y")
            else:
                performance_day = str_day_list[0] + ' ' + str_day_list[1]
                month = str_day_list[1]
                print(month)
                if(month == "января"):
                    performance_day = str_day_list[0] + '.' + '01' + today.strftime("%y")
                if (month == "февраля"):
                    performance_day = str_day_list[0] + '.' + '02' + today.strftime("%y")
                if (month == "марта"):
                    performance_day = str_day_list[0] + '.' + '03' + today.strftime("%y")
                if (month == "апреля"):
                    performance_day = str_day_list[0] + '.' + '04' + today.strftime("%y")
                if (month == "мая"):
                    performance_day = str_day_list[0] + '.' + '05' + today.strftime("%y")
                if (month == "июня"):
                    performance_day = str_day_list[0] + '.' + '06' + today.strftime("%y")
                if (month == "июля"):
                    performance_day = str_day_list[0] + '.' + '07' + today.strftime("%y")
                if (month == "августа"):
                    performance_day = str_day_list[0] + '.' + '08' + today.strftime("%y")
                if (month == "сентября"):
                    performance_day = str_day_list[0] + '.' + '09' + today.strftime("%y")
                if (month == "октября"):
                    performance_day = str_day_list[0] + '.' + '10' + today.strftime("%y")
                if (month == "ноября"):
                    performance_day = str_day_list[0] + '.' + '11' + today.strftime("%y")
                if (month == "декабря"):
                    performance_day = str_day_list[0] + '.' + '12' + today.strftime("%y")

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

        age = GetIngormationFromPerformance(GetPerformance(performance_urls)[0], GetPerformance(performance_urls)[1])[0]
        adress_all = GetIngormationFromPerformance(GetPerformance(performance_urls)[0], GetPerformance(performance_urls)[1])[1]
        adress_list = adress_all.split(' ')
        adress = adress_all
        if(len(adress_list) == 3):
            if(adress_list[2] == 'назад'):
                adress = -1

        duration_all = GetIngormationFromPerformance(GetPerformance(performance_urls)[0], GetPerformance(performance_urls)[1])[2]
        duration_list = duration_all.split(' ')
        duration = duration_all

        if (
                performance_name and performance_min_discription and performance_theatre and performance_rating and performance_urls ):
            performance_data_list.append(
                {
                    "Название представления": performance_name.text,
                    "Описание": performance_min_discription.text,
                    "Минимальная цена": price,
                    "Ближайшее время": performance_time,
                    "Ближайшая дата": performance_day,
                    "Жанр": genre,
                    "Рейтинг": performance_rating.text,
                    "Театр": performance_theatre.text,
                    "Ссылка на представление": performance_urls,
                    "Возрастное ограничение": age,
                    "Адрес театра": adress,
                    "Продолжительность": duration,
                    "Другие даты и время": -1,
                }
            )
    print(performance_data_list)
    with open("all_performance_dict.json", "w", encoding='utf-8') as file:
        json.dump(performance_data_list, file, indent=4, ensure_ascii=False)
        # data=json.load(file)
        # df=pd.DataFrame(data)
        # df.to_excel("performance_list.xlsx")
def GoToPages():
    hrefs = []
    driver = webdriver.Chrome(
        executable_path="D:\\University\\OPD\\LabOPD\\chromedriver\\chromedriver.exe")
    url = "https://www.afisha.ru/spb/schedule_theatre/"
    driver.get(url)
    try:
        button = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[1]/div/main/div[2]')
        agree_button = driver.find_element_by_class_name('_3jiFM _1Lyrw LTCFn _2oJKT _2IYn8')
        agree_button.click()
        for _ in range(25):
            actions = ActionChains(driver)
            actions.move_to_element(button).perform()
            time.sleep(5)
            button.click()
            time.sleep(5)
        with open('hrefs.txt', "w", encoding='utf-8') as file:
            elems = driver.find_elements_by_class_name('Card_nestedLink__2dGug')
            for elem in elems:
                href = elem.get_attribute("href")
                if 'https://www.afisha.ru/spb/schedule_theatre/' in href:
                    hrefs.append(href)
            hrefs = set(hrefs)
            hrefs = list(hrefs)
            for link in hrefs:
                file.write(f'{link}\n')
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


def main():
    GetHTML()
    InformationInFile(GetHTML())
    ConvertToExcel()
    #GoToPages()
main()