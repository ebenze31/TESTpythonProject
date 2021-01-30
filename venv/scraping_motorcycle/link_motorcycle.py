# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import os
import mysql.connector
import datetime as dt

# def funcUrl_allpage():
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="car"
)
print("Connect")


time = dt.datetime.now()
print(time)

url_home = 'https://xn--42cgk3b7cdl3dvabeb1k5etc5gd.tv/%E0%B8%97%E0%B8%B8%E0%B8%81%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B9%80%E0%B8%A0%E0%B8%97-%E0%B9%80%E0%B8%A3%E0%B8%B5%E0%B8%A2%E0%B8%87-%E0%B8%AB%E0%B8%99%E0%B9%89%E0%B8%B21'
home = requests.get(url_home)
soup = BeautifulSoup(home.text, 'html.parser')

# เก็บ url ใน 1 pagr
links = soup.find_all("ul",{"class":"catalog_table"})
link_array = {}
value = {}
for item in links:
    value = item.find_all("a",{"class":"thumb"})['href']
    print(value)