import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
import time

def get_html():
    url = "https://live.mts.ru/sankt-peterburg/theater"

    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1",
    }

    req = requests.get(url, headers=headers)
    src = req.text
    with open('index.html','w', encoding='utf-8') as file:
        file.write(src)

    with open('index.html', 'r', encoding='utf-8') as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    return soup

# with open('href.csv', 'w') as file:
#     link_prev = 0
#     for link in soup.find_all('a'):
#             if 'theater' in link.get('href'):
#                 string = link.get('href')
#                 string = string.replace('undefined', 'sankt-peterburg')
#                 file.write(f'https://live.mts.ru/{string}\n')
#                 link_prev = link

# def write_links_in_file1(soup):
#     with open('hrefs.txt', "w", encoding='utf-8') as file:
#         LIST = []
#         links = soup.find(class_='Feed_leftColumn__187Fe').find_all('a')
#         for link in links:
#             if 'theater' in link.get('href'):
#                 string = link.get('href')
#                 string = string.replace('undefined', 'sankt-peterburg')
#                 LIST.append(string)
#         LIST = set(LIST)
#         LIST = list(LIST)
#         for link in LIST:
#             file.write(f'https://live.mts.ru{link}\n')


def write_links_in_file():
    hrefs = []
    driver = webdriver.Chrome(
        executable_path="C:\\Users\\Bruhonog\\PycharmProjects\\OPD\\chromedriver\\chromedriver.exe")
    url = "https://live.mts.ru/sankt-peterburg/theater"
    driver.get(url)
    try:
        button = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[1]/div/main/div[2]')
        agree_button = driver.find_element_by_class_name('UserAgreeBanner_buttonContainer__1GeY8')
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
                if 'https://live.mts.ru/sankt-peterburg/theater/' in href:
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


def information_in_file():
    with open('hrefs.txt', 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file.readlines()]
        count = 0
        data_dict = []
        for href in lines[1::]:
            count+=1
            q = requests.get(href)
            result = q.content
            soup = BeautifulSoup(result, 'lxml')
            try:

                info = soup.find_all(class_='EventPageMeta_meta_text__15d-U')
                data = info[0].text
                age = info[1].text
                price = info[2].text
                theater = info[3].text
                adress = info[4].text
                title = soup.find(class_='EventPage_title__N8Fvr').text


                description = soup.find(class_='HidableText_hidableText__24xFf').text

                # time_start = soup.find(class_='CarouselSlides_carousel_slide__36vXY')
                # print(time_start)
                genre = soup.find(class_='Tags_tagItemBig__1vvwX').text


                data = {
                    'title': title,
                    'description': description,
                    'price': price,
                    'data': data,
                    'age': age,
                    'jenre': genre,
                    'theater': theater,
                    'link': href,
                    'adress': adress
                }

                data_dict.append(data)

            except: 'Sorry bro'
    with open ('data.json', 'w', encoding='utf-8') as json_file:
        json.dump(data_dict, json_file, ensure_ascii=False, indent=4)


def main():

    # write_links_in_file()
    information_in_file()
    pd.read_json("data.json").to_excel("data.xlsx")
main()