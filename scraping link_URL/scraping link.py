# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import os
import mysql.connector
import datetime as dt

time = dt.datetime.now()
#print(time)

url_home = 'https://www.one2car.com/%E0%B8%A3%E0%B8%96%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%AA%E0%B8%AD%E0%B8%87-%E0%B8%AA%E0%B8%B3%E0%B8%AB%E0%B8%A3%E0%B8%B1%E0%B8%9A-%E0%B8%82%E0%B8%B2%E0%B8%A2'
home = requests.get(url_home)
soup = BeautifulSoup(home.text,'html.parser')

#ARRAY FIND ALL ได้ ARRAY เสมอ

#เก็บ url ใน 1 pagr
links = soup.find_all('h2')
link_array = {}
split_array = {}
for item in links:
    if item.find('a') == None :
        continue
    #print(item.find('a')['href'])
    value = item.find('a')['href']
    #print(value)
    split = item.find('a')['href'].split("/")
    #print(split[-1])
    split_array[split[-1]] = split[-1]
    for id_car in split_array:
        print(id_car)
    link_array[id_car] = value

# active_page
active_page_array = {}
active_page = soup.find_all("li",{"class":"active"})
for item in active_page:
    if item.find('a') == None :
        continue
    text_active_page = item.find('a')['href']
    split = item.find('a')['href'].split("&")
    print("text_active_page =  ",text_active_page)
    active_page = split[1]
    print("active_page =  ", active_page)

# next_page
next_page_array = {}
next_page = soup.find_all("li",{"class":"next"})

for item in next_page:
    if item.find('a') == None :
        continue
    text_next_page = item.find('a')['href']
    split = item.find('a')['href'].split("&")
    print("text_next_page =  ",text_next_page)
    page_number = split[1]
    print("next_page =  ", page_number)

# last_page
last_page_array = {}
last_page = soup.find_all("li",{"class":"last"})

for item in last_page:
    if item.find('a') == None :
        continue
    text_last_page = item.find('a')['href']
    split = item.find('a')['href'].split("&")
    print("text_last_page =  ",text_last_page)
    last_page = split[1]
    print("last_page =  ", last_page)

# save to json
print("link",json.dumps(link_array,ensure_ascii=False),"\n")
with open("URL/" + active_page + ".json", "w") as f:
    json.dump(link_array, f, ensure_ascii=False)

# json loop
count = 0
while count < 1 : # last_page
    url_next_page = 'https://www.one2car.com/'+ text_next_page
    home_next_page = requests.get(url_next_page)
    soup2 = BeautifulSoup(home_next_page.text, 'html.parser')

    links = soup2.find_all('h2')
    link_array = {}
    split_array = {}
    for item in links:
        if item.find('a') == None:
            continue
        # print(item.find('a')['href'])
        value = item.find('a')['href']
        #print(value)
        split = item.find('a')['href'].split("/")
        # print(split[-1])
        split_array[split[-1]] = split[-1]
        for id_car in split_array:
            print(id_car)
        link_array[id_car] = value

    # active_page
    active_page_array = {}
    active_page = soup2.find_all("li", {"class": "active"})
    for item in active_page:
        if item.find('a') == None:
            continue
        text_active_page = item.find('a')['href']
        split = item.find('a')['href'].split("&")
        print("text_active_page =  ", text_active_page)
        active_page = split[1]
        print("active_page =  ", active_page)

    # next_page
    next_page_array = {}
    next_page = soup2.find_all("li", {"class": "next"})

    for item in next_page:
        if item.find('a') == None:
            continue
        text_next_page = item.find('a')['href']
        split = item.find('a')['href'].split("&")
        print("text_next_page =  ", text_next_page)
        page_number = split[1]
        print("next_page =  ", page_number)

    # save to json
    print("link", json.dumps(link_array, ensure_ascii=False), "\n")
    with open("URL/"+active_page + ".json", "w") as f:
        json.dump(link_array, f, ensure_ascii=False)

    count = count + 1
merge_array = {}
filenames = os.listdir('URL')
#print(filenames)
for file in filenames:
    #print(file)
    split = file.split("=")
    numbre = split[1].split(".")
    #print(numbre[0])
    with open('URL/' + file) as f:
        data = json.load(f)
        merge_array[numbre[0]] = data
        # print(data)
        # print(merge_array)

    # print(data)

    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="collect-all-cars"
        )
    print("Connect")
    for id_car in split_array:
        print(id_car)

        mycursor = mydb.cursor()

        sql_links = "INSERT INTO links (created_at, car_id, link, active)" \
              " VALUES (%s, %s, %s, %s)"
        val = [
            (time,
             id_car,
             link_array[id_car],
             "Yes")
        ]

        mycursor.executemany(sql_links, val)

        mydb.commit()

print("เสร็จเรียบร้อย")
with open("merge/merge.json", "w") as f:
    json.dump(merge_array, f, ensure_ascii=False)


