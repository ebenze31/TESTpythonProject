# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import os
import mysql.connector
import datetime as dt
import pyshorteners as ps

mydb = mysql.connector.connect(
    host="159.65.128.190",
    user="viicheck2",
    password="viicheck",
    database="viicheck"
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

section = soup.find("section",{"class":"section--promotions-list"})

div = soup.find("img")['src']
print(section)


    # mycursor = mydb.cursor()
    #
    # sql_div_up = "INSERT INTO promotions (created_at, company, titel, detail, photo, time_period, link )" \
    #             " VALUES (%s, %s, %s, %s, %s, %s, %s)"
    # val = [
    #     (time,
    #      "Cockpit",
    #      titel,
    #      "-",
    #      img,
    #      "ดูเพิ่มเติม",
    #      link)
    # ]
    # mycursor.executemany(sql_div_up, val)
    # mydb.commit()



