# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import os
import mysql.connector
import datetime as dt
import pyshorteners as ps

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="car"
)
print("Connect")

mycursor = mydb.cursor()
sql_delete = "DELETE FROM promotions WHERE company='FIT Auto'"
mycursor.execute(sql_delete)
mydb.commit()

time = dt.datetime.now()
print(time)

url_home = 'https://www.pttfitauto.com/th/promotions'
home = requests.get(url_home)
soup = BeautifulSoup(home.text, 'html.parser')


# โปรโมชั่น 2 อันบน
div_img_up = soup.find_all("div",{"class":"promotions"})

for i in div_img_up:
    link_link = i.find('a')['href']
    link = ps.Shortener().tinyurl.short(link_link)
    link_img_up = i.find('img')['src']
    img_up = ps.Shortener().tinyurl.short(link_img_up)
    title = i.find("div", {"class": "txt-title"}).text
    detail = i.find("p", {"class": "cut-text"}).text
    time_period = i.find("span", {"style": "font-size: 20px; font-weight: bold; line-height: 18px;"}).text

    print("link >> " + link)
    print("img_up >> " + img_up)
    print("title >> " + title)
    print("detail >> " + detail)
    print("ระยะเวลา >> " + time_period)
    print("-----------------------------------------------------------------------")

    # mycursor = mydb.cursor()
    #
    # sql_div_up = "INSERT INTO promotions (created_at, company, titel, detail, photo, time_period, link )" \
    #             " VALUES (%s, %s, %s, %s, %s, %s, %s)"
    # val = [
    #     (time,
    #      "FIT Auto",
    #      title,
    #      detail,
    #      img_up,
    #      time_period,
    #      link)
    # ]
    # mycursor.executemany(sql_div_up, val)
    # mydb.commit()



