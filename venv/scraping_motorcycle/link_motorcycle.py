# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import os
import mysql.connector
import datetime as dt

def funcUrl_allpage():
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

    # find page all
    ac = soup.find("div",{"class":"w3-center"})
    ac2 = ac.find("div",{"class":"w3-bar"})

    # active_page
    ac3 = ac2.find("a",{"class":"w3-orange"})
    active_page = ac3.text
    print("active_page = ", active_page)

    # next page
    next = ac3['href'].split("า")
    next_page = int(next[-1]) + 1
    text_next_page = str(next[0])+"า"+str(next_page)
    print("next_page = ", next_page)
    # print("text_next_page = ",text_next_page)

    # last page
    ac4 = ac2.find("a",{"title":"หน้าสุดท้าย"})
    ac5 = ac4['href']
    sp = ac5.split("า")
    last_page = sp[-1]
    print("last_page = ", last_page)

    # เก็บ url ใน 1 pagr
    links = soup.find_all("ul",{"class":"catalog_table"})
    link_array = {}
    for item in links:
        value = item.find_all("div",{"class":"title_box"})
        for i in value:
            value2 = i.find('a')['href']

            sp = value2.split("-")
            sp2 = sp[-1].split(".")
            motorcycles_id = sp2[0]

            link_array[motorcycles_id] = value2

        # print("motorcycles_id = " + motorcycles_id)
        # print("links = "+ value2)
        # print(link_array)

            mycursor = mydb.cursor()

            query = mycursor.execute("SELECT link FROM motorcycles_links WHERE motorcycles_id = " + motorcycles_id)
            myresult = mycursor.fetchall()

            print("มี ", mycursor.rowcount, "บรรทัด")
            if mycursor.rowcount == 0:
                sql_links = "INSERT INTO motorcycles_links (created_at, motorcycles_id, link, active)" \
                            " VALUES (%s, %s, %s, %s)"
                val = [
                    (time,
                     motorcycles_id,
                     link_array[motorcycles_id],
                     "Yes")
                ]
                mycursor.executemany(sql_links, val)
                mydb.commit()

            elif mycursor.rowcount >= 1:
                sql = "UPDATE motorcycles_links SET updated_at = %s WHERE motorcycles_id = %s"
                val = (time, motorcycles_id)
                mycursor.execute(sql, val)
                mydb.commit()
    # loop
    count = 1
    while count < int(last_page) : # int(last_page)
        url_next_page = 'https://xn--42cgk3b7cdl3dvabeb1k5etc5gd.tv/' + text_next_page
        home_next_page = requests.get(url_next_page)
        soup2 = BeautifulSoup(home_next_page.text, 'html.parser')

        # find page all
        ac = soup2.find("div", {"class": "w3-center"})
        ac2 = ac.find("div", {"class": "w3-bar"})

        # active_page
        ac3 = ac2.find("a", {"class": "w3-orange"})
        active_page = ac3.text
        print("active_page = ", active_page)

        # next page
        next = ac3['href'].split("า")
        next_page = int(next[-1]) + 1
        text_next_page = str(next[0]) + "า" + str(next_page)
        print("next_page = ", next_page)
        # print("text_next_page = ", text_next_page)

        # last page
        ac4 = ac2.find("a", {"title": "หน้าสุดท้าย"})
        ac5 = ac4['href']
        sp = ac5.split("า")
        last_page = sp[-1]
        print("last_page = ", last_page)

        # เก็บ url ใน 1 pagr
        links = soup2.find_all("ul", {"class": "catalog_table"})
        link_array = {}
        for item in links:
            value = item.find_all("div", {"class": "title_box"})
            for i in value:
                value2 = i.find('a')['href']

                sp = value2.split("-")
                sp2 = sp[-1].split(".")
                motorcycles_id = sp2[0]

                link_array[motorcycles_id] = value2

                # print("motorcycles_id = " + motorcycles_id)
                # print("links = "+ value2)
                # print(link_array)

                mycursor = mydb.cursor()

                query = mycursor.execute("SELECT link FROM motorcycles_links WHERE motorcycles_id = " + motorcycles_id)
                myresult = mycursor.fetchall()

                print("มี ", mycursor.rowcount, "บรรทัด")
                if mycursor.rowcount == 0:
                    sql_links = "INSERT INTO motorcycles_links (created_at, motorcycles_id, link, active)" \
                                " VALUES (%s, %s, %s, %s)"
                    val = [
                        (time,
                         motorcycles_id,
                         link_array[motorcycles_id],
                         "Yes")
                    ]
                    mycursor.executemany(sql_links, val)
                    mydb.commit()

                elif mycursor.rowcount >= 1:
                    sql = "UPDATE motorcycles_links SET updated_at = %s WHERE motorcycles_id = %s"
                    val = (time, motorcycles_id)
                    mycursor.execute(sql, val)
                    mydb.commit()

        count = count + 1