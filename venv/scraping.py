# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
url_home = 'https://www.one2car.com/%E0%B8%A3%E0%B8%96%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%AA%E0%B8%AD%E0%B8%87-%E0%B8%AA%E0%B8%B3%E0%B8%AB%E0%B8%A3%E0%B8%B1%E0%B8%9A-%E0%B8%82%E0%B8%B2%E0%B8%A2'
url_detail = 'https://www.one2car.com/for-sale/bmw-530e-m-sport-กรุงเทพและปริมณฑล-พระราม3-สาทร-พระราม4/7170868'

home =  requests.get(url_home)
web_data = requests.get(url_detail)

soup = BeautifulSoup(home.text,'html.parser')
soup2 = BeautifulSoup(web_data.text,'html.parser')

link = soup.find_all("h2",{"class":"listing__title  epsilon  flush"})

car = soup2.find_all("div",{"class":"listing__key-listing__list"})


print("\n------------------------------------------\n")
print("DETAIL CAR = ↓↓↓↓↓↓↓↓","\n",car[0])
print("\n------------------------------------------\n")

for count in range(0, 25):
    link = soup.find_all('h2')[count].find('a')
    print("link",count," = ↓↓↓↓↓↓↓↓","\n",link,"\n")


