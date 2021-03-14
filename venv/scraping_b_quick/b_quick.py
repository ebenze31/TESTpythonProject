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
sql_delete = "DELETE FROM promotions WHERE company='B-Quik'"
mycursor.execute(sql_delete)
mydb.commit()

time = dt.datetime.now()
print(time)

url_home = 'https://www.b-quik.com/th/promotion'
home = requests.get(url_home)
soup = BeautifulSoup(home.text, 'html.parser')

# โปรโมชั่น 2 อันบน
div_img_up = soup.find_all("div",{"class":"col-lg-6 pt-3"})

for i in div_img_up:
    link_link = i.find('a')['href']
    link = ps.Shortener().tinyurl.short(link_link)
    link_img_up = i.find('img')['src']
    img_up = ps.Shortener().tinyurl.short(link_img_up)
    title = i.find("div", {"class": "txt-title"}).text
    detail = i.find("p", {"class": "cut-text"}).text
    time_period = i.find("span", {"style": "font-size: 20px; font-weight: bold; line-height: 18px;"}).text

    # print("link >> " + link)
    # print("img_up >> " + img_up)
    # print("title >> " + title)
    # print("detail >> " + detail)
    # print("ระยะเวลา >> " + time_period)
    # print("-----------------------------------------------------------------------")

    mycursor = mydb.cursor()

    sql_div_up = "INSERT INTO promotions (created_at, company, titel, detail, photo, time_period, link )" \
                " VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = [
        (time,
         "B-Quik",
         title,
         detail,
         img_up,
         time_period,
         link)
    ]
    mycursor.executemany(sql_div_up, val)
    mydb.commit()

# โปรโมชั่น ล่าง
div_img_down = soup.find_all("div",{"class":"col-lg-3 col-md-4 col-6"})

for i in div_img_down:
    link_link = i.find('a')['href']
    link = ps.Shortener().tinyurl.short(link_link)
    link_img_up = i.find('img')['src']
    img_up = ps.Shortener().tinyurl.short(link_img_up)
    title = i.find("div", {"class": "txt-title"}).text
    detail = i.find("p", {"class": "cut-text"}).text
    time_period = i.find("span", {"class": "txt-time-p-d"}).text

    print("link >> " + link)
    print("img_up >> " + img_up)
    print("title >> " + title)
    print("detail >> " + detail)
    print("ระยะเวลา >> " + time_period)
    print("-----------------------------------------------------------------------")

    mycursor = mydb.cursor()

    sql_div_up = "INSERT INTO promotions (created_at, company, titel, detail, photo, time_period, link )" \
                " VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = [
        (time,
         "B-Quik",
         title,
         detail,
         img_up,
         time_period,
         link)
    ]
    mycursor.executemany(sql_div_up, val)
    mydb.commit()


