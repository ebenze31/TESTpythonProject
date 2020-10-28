# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

url_home = 'https://www.one2car.com/%E0%B8%A3%E0%B8%96%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%AA%E0%B8%AD%E0%B8%87-%E0%B8%AA%E0%B8%B3%E0%B8%AB%E0%B8%A3%E0%B8%B1%E0%B8%9A-%E0%B8%82%E0%B8%B2%E0%B8%A2'

home =  requests.get(url_home)
soup = BeautifulSoup(home.text,'html.parser')

link = soup.find_all("h2",{"class":"listing__title  epsilon  flush"})

#ARRAY FIND ALL ได้ ARRAY เสมอ
links = soup.find_all('h2')

for item in links:
    if item.find('a') == None :
        continue
    print(item.find('a')['href'])