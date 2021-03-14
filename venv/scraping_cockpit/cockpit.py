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
sql_delete = "DELETE FROM promotions WHERE company='Cockpit'"
mycursor.execute(sql_delete)
mydb.commit()

time = dt.datetime.now()
print(time)

url_home = 'https://www.cockpit.co.th/offers'
home = requests.get(url_home)
soup = BeautifulSoup(home.text, 'html.parser')

link = ps.Shortener().tinyurl.short(url_home)

div = soup.find_all("div",{"class":"gnext-re-promotion-v1-card-a"})
for i in div:
    mat = i.find("mat-card")['style']
    sp = mat.split("(")
    sp2 = sp[1].split(")")
    img_img = sp2[0]
    img = ps.Shortener().tinyurl.short(img_img)

    h2 = i.find("h2").text
    p = i.find("p").text
    titel = h2 + p

    print("img >> " + img)
    print("titel >> " + titel)
    print("link >> " + link)
    print("--------------------------------------------------")

    mycursor = mydb.cursor()

    sql_div_up = "INSERT INTO promotions (created_at, company, titel, detail, photo, time_period, link )" \
                " VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = [
        (time,
         "Cockpit",
         titel,
         "-",
         img,
         "ดูเพิ่มเติม",
         link)
    ]
    mycursor.executemany(sql_div_up, val)
    mydb.commit()
    



