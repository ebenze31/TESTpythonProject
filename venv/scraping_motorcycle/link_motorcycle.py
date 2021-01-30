# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import os
import mysql.connector
import datetime as dt

# def funcUrl_allpage():
# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="",
#     database="car"
# )
# print("Connect")


time = dt.datetime.now()
print(time)

url_home = 'https://xn--42cgk3b7cdl3dvabeb1k5etc5gd.tv/%E0%B8%97%E0%B8%B8%E0%B8%81%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B9%80%E0%B8%A0%E0%B8%97-%E0%B9%80%E0%B8%A3%E0%B8%B5%E0%B8%A2%E0%B8%87-%E0%B8%AB%E0%B8%99%E0%B9%89%E0%B8%B21'
home = requests.get(url_home)
soup = BeautifulSoup(home.text, 'html.parser')

# เก็บ url ใน 1 pagr
links = soup.find_all("ul",{"class":"catalog_table"})
link_array = {}
for item in links:
    value = item.find_all("div",{"class":"title_box"})
    for i in value:
        value2 = i.find('a')['href']

        sp = value2.split("-")
        sp2 = sp[-1].split(".")
        motorcycles_id = sp2[0]

        link_array[motorcycles_id] = value2

    # print("motorcycles_id = " + motorcycles_id)
    # print("links = "+ value2)
    # print(link_array)

# find page all
ac = soup.find("div",{"class":"w3-center"})
ac2 = ac.find("div",{"class":"w3-bar"})

# active_page
ac3 = ac2.find("a",{"class":"w3-orange"})
active_page = ac3.text
print("active_page = ", active_page)

# last page
ac4 = ac2.find("a",{"title":"หน้าสุดท้าย"})
ac5 = ac4['href']
sp = ac5.split("า")
last_page = sp[-1]
print("last_page = ", last_page)


with open("link_url/url/" + active_page + ".json", "w") as f:
        json.dump(link_array, f, ensure_ascii=False)