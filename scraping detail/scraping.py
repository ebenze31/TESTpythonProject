# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import mysql.connector
import datetime as dt
import os

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="collect-all-cars"
)
print("Connect")


with open('../scraping link_URL/merge/merge.json') as f:
    data = json.load(f)
    for file in data:
        #print(file)
        print("Type:", type(data))
        print(file +":", data[file])

        for key in data[file]:
            print("KEY >>> "+key)
            print("URL = ", data[file][key])
            url = data[file][key]

            data_car_array = {
                "ราคา": "",
                "ประเภท": "",
                "รูป": "",
                "\n\nดีลเลอร์มีความน่าเชื่อถือ ผ่านการตรวจสอบตามเกณฑ์ที่กำหนด\n": "",
                "ยี่ห้อ": "",
                "รุ่น": "",
                "โฉมรถยนต์": "",
                "รายละเอียดรุ่น": "",
                "ปี": "",
                "ขนาดเครื่องยนต์": "",
                "ระบบเกียร์": "",
                "จำนวนที่นั่ง": "",
                "เลขไมล์ (กม.)": "",
                "สี": "",
                "สถานที่": "",
                "ลิงก์": ""
            }
            url_detail = url

            # ADD TO ARRAY
            data_car_array["ลิงก์"] = url_detail

            id_car = url_detail.split("/")
            print(id_car)
            print(id_car[-1])
            print(id_car[-2])
            # ADD TO ARRAY
            data_car_array["สถานที่"] = id_car[-2]

            web_data = requests.get(url_detail)
            soup2 = BeautifulSoup(web_data.text,'html.parser')
            if soup2.find("div",{"class":"listing__price"}) == None :
                print("ERROR")
                print(web_data.text)


            price_car = soup2.find("div",{"class":"listing__price"}).text
            if price_car == None:
                continue
            print(price_car)
            # ADD TO ARRAY
            data_car_array["ราคา"] = price_car

            type_car = soup2.find("div",{"class":"listing__title"}).text
            #print(type_car)
            split_type_car = type_car.split(" ")
            #print(split_type_car)
            print(split_type_car[-1])
            # ADD TO ARRAY
            data_car_array["ประเภท"] = split_type_car[-1]

            img = soup2.find("div", {"class": "gallery__image"})
            img_car = img.find('img')['data-src']
            print("IMG >>> "+img_car)
            # ADD TO ARRAY
            data_car_array["รูป"] = img_car


            car = soup2.find_all("div",{"class":"list-item"})
            for item in car :
                if item.find('span') == None :
                    continue
                if len(item.find_all('span')) == 2 or 3:
                    #print(item.find_all('span')[0].text, " / ", item.find_all('span')[1].text)
                    if item.find_all('span')[0].text == "ประเภทรถ" :
                        continue
                    if item.find_all('span')[0].text == "เล่มทะเบียน" :
                        continue

                    key = item.find_all('span')[0].text
                    value = item.find_all('span')[1].text

                    if item.find_all('span')[0].text == "เกียร์" :
                        key = item.find_all('span')[0].text
                        value = item.find_all('span')[1].text
                        break
                    # ADD TO ARRAY
                    data_car_array[key] = value
                    print(data_car_array)

            #save to json
            print("car",json.dumps(data_car_array,ensure_ascii=False),"\n")
            with open("detail/"+id_car[-1]+".json", "w") as f:
                json.dump(data_car_array, f, ensure_ascii=False)


                time = dt.datetime.now()
                # print(time)

                mycursor = mydb.cursor()

                sql = "UPDATE links SET read_at = %s WHERE active = %s"
                val = (time, "Yes")

                mycursor.execute(sql, val)

                mydb.commit()

filenames = os.listdir('../scraping detail/detail')
#print(filenames)
for file in filenames:
    #print(file)
    split = file.split(".")
    print(split[0])
    car_id = split[0]

    with open("../scraping detail/detail/" + split[0] + ".json") as f:
        data = json.load(f)
    print(data)
    print(data['ราคา'])

    mycursor = mydb.cursor()



    sql = "INSERT INTO details (created_at, price, type, brand, model, face, submodel, year, motor, gear, seats, distance, color, image, car_id, location, link)" \
          " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = [
        (time,
         data['ราคา'],
         data['ประเภท'],
         data['ยี่ห้อ'],
         data['รุ่น'],
         data['โฉมรถยนต์'],
         data['รายละเอียดรุ่น'],
         data['ปี'],
         data['ขนาดเครื่องยนต์'],
         data['ระบบเกียร์'],
         data['จำนวนที่นั่ง'],
         data['เลขไมล์ (กม.)'],
         data['สี'],
         data['รูป'],
         car_id,
         data['สถานที่'],
         data['ลิงก์'])
    ]

    mycursor.executemany(sql, val)

    mydb.commit()

print("เสร็จเรียบร้อย")



