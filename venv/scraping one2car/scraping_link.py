# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import os
import mysql.connector
import datetime as dt

def funcUrl_allpage():
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="car"
    )
    print("Connect")


    time = dt.datetime.now()
    print(time)

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
        for c in split_array:
            cc = c.split("?")
            id_car = cc[0]
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
        active_page_n = split[1]
        print("active_page =  ", active_page_n)

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
        last_page_sp = last_page.split("=")
        last_page_num = last_page_sp[1]
        print("last_page =  ", last_page_num)

    # save to json
    print("link",json.dumps(link_array,ensure_ascii=False),"\n")
    with open("scraping_link_URL/URL/" + active_page_n + ".json", "w") as f:
        json.dump(link_array, f, ensure_ascii=False)

        for c in split_array:
            cc = c.split("?")
            id_car = cc[0]
            print(id_car)

            mycursor = mydb.cursor()

            query = mycursor.execute("SELECT link FROM links WHERE car_id = "+id_car)
            myresult = mycursor.fetchall()

            print("มี ", mycursor.rowcount, "บรรทัด")
            if mycursor.rowcount == 0:
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

            elif mycursor.rowcount >= 1:
                sql = "UPDATE links SET updated_at = %s WHERE car_id = %s"
                val = (time, id_car)
                mycursor.execute(sql, val)
                mydb.commit()

    # json loop
    count = 0
    while count < 1 : # int(last_page_num)
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
            for c in split_array:
                cc = c.split("?")
                id_car = cc[0]
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
            active_page_now = split[1]
            print("active_page =  ", active_page_now)

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
        with open("scraping_link_URL/URL/"+ active_page_now + ".json", "w") as f:
            json.dump(link_array, f, ensure_ascii=False)

        for c in split_array:
            cc = c.split("?")
            id_car = cc[0]
            #print(type(id_car))

            mycursor = mydb.cursor()

            query = mycursor.execute("SELECT link FROM links WHERE car_id = " + id_car)
            myresult = mycursor.fetchall()

            print("มี ", mycursor.rowcount, "บรรทัด")
            if mycursor.rowcount == 0:
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

            elif mycursor.rowcount >= 1:
                sql = "UPDATE links SET updated_at = %s WHERE car_id = %s"
                val = (time, id_car)
                mycursor.execute(sql, val)
                mydb.commit()

        count = count + 1
    merge_array = {}
    filenames = os.listdir('scraping_link_URL/URL')
    #print(filenames)
    for file in filenames:
        #print(file)
        split = file.split("=")
        numbre = split[1].split(".")
        #print(numbre[0])
        with open('scraping_link_URL/URL/' + file) as f:
            data = json.load(f)
            merge_array[numbre[0]] = data
            # print(data)
            # print(merge_array)
        # print(data)

    with open("scraping_link_URL/merge/merge.json", "w") as f:
        json.dump(merge_array, f, ensure_ascii=False)

    print("เสร็จเรียบร้อย")

