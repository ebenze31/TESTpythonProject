# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
url_detail = 'https://www.one2car.com/for-sale/bmw-530e-m-sport-กรุงเทพและปริมณฑล-พระราม3-สาทร-พระราม4/7170868'

test = url_detail.split("/")
print(test)
print(test[-1])

web_data = requests.get(url_detail)

soup2 = BeautifulSoup(web_data.text,'html.parser')

car = soup2.find_all("div",{"class":"list-item"})

example_array = {}

for item in car :
    if item.find('span') == None :
        continue
    if len(item.find_all('span')) == 2 :
        print(item.find_all('span')[0].text, " / ", item.find_all('span')[1].text)
        key = item.find_all('span')[0].text
        value = item.find_all('span')[1].text
        example_array[key] = value

#save to json
print("car",json.dumps(example_array,ensure_ascii=False),"\n")
with open(test[-1]+".json", "w") as f:
    json.dump(example_array, f, ensure_ascii=False)



