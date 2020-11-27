# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import mysql.connector
import datetime
from datetime import datetime
import os

time = datetime.now()
print("TIME >>",time)

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
        # print("FILE >>",file)
        print("Type:", type(data))
        print(file +":", data[file])
        # print("DATA FILE", data[file])

        for key in data[file]:
            print("KEY >>> ",key)
            print("URL = ", data[file][key])
            url = data[file][key]
            url_detail = url
            id_car = url_detail.split("/")
            print(id_car)
            print("id_car[-1] >>", id_car[-1])
            print(id_car[-2])

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


            # เช็ค read_at in links database
            mycursor = mydb.cursor()
            query = mycursor.execute("SELECT read_at FROM links WHERE car_id = " + id_car[-1])
            myresult = mycursor.fetchall()
            for read_at in myresult:
                #print("read_at >>> ",read_at)
                if read_at == (None,):
                    t = "None"
                else:
                    read_str =  str(read_at)
                    sp = read_str.split(" ")
                    # print("sp[1]",sp[1])
                    if sp[1] == "1,":
                        month = "Jan"
                    elif sp[1] == "2,":
                        month = "Feb"
                    elif sp[1] == "3,":
                        month = "Mar"
                    elif sp[1] == "4,":
                        month = "Apr"
                    elif sp[1] == "5,":
                        month = "May"
                    elif sp[1] == "6,":
                        month = "Jun"
                    elif sp[1] == "7,":
                        month = "Jul"
                    elif sp[1] == "8,":
                        month = "Aug"
                    elif sp[1] == "9,":
                        month = "Sep"
                    elif sp[1] == "10,":
                        month = "Oct"
                    elif sp[1] == "11,":
                        month = "Nov"
                    elif sp[1] == "12":
                        month = "Dec"
                    #print("SP 0 >> ", sp[0])
                    sp_year = sp[0].split("(")
                    #print("sp_year >> ", sp_year)
                    sp_sec = sp[5].split(")")
                    #print("sp_sec >> ", sp_sec)
                    l_read = sp[2]+" "+ month+" "+sp_year[-1]+" at "+ sp[3]+":"+ sp[4]+":"+ sp_sec[0]
                    last_read = l_read.replace(",","")
                    print("วันที่ที่อ่านล่าสุด >> ", last_read)
                    format = "%d %b %Y at %H:%M:%S"
                    parsed_datetime = datetime.strptime(last_read, format)
                    print("parsed_datetime >> ", parsed_datetime)
                    t = time - parsed_datetime
                    print("timedelta >> ",t.days)

                if t == "None" or t.days > 2:

                    # ADD TO ARRAY
                    data_car_array["ลิงก์"] = url_detail
                    # ADD TO ARRAY
                    data_car_array["สถานที่"] = id_car[-2]

                    web_data = requests.get(url_detail)
                    soup2 = BeautifulSoup(web_data.text,'html.parser')

                    # หา 404 เปลี่ยน active เป็น No

                    error_404 = soup2.find("title").text
                    print("title >>",error_404)
                    if error_404 == "ไม่ค้นพบหน้าที่คุณต้องการ - One2car.com":
                        mycursor = mydb.cursor()
                        sql = "UPDATE links SET active = %s , read_at = %s WHERE car_id = %s"
                        val = ("No", time, id_car[-1])
                        mycursor.execute(sql, val)
                        mydb.commit()
                        break
                    elif error_404 == None:
                        continue

                    if soup2.find("div",{"class":"listing__price"}) == None :
                        print("ERROR")
                        print(web_data.text)

                    price_car = soup2.find("div",{"class":"listing__price"}).text
                    if price_car == None:
                        continue
                    print("price_car >> ",price_car)
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

                    # save to json
                    print("car", json.dumps(data_car_array, ensure_ascii=False), "\n")
                    with open("detail/" + id_car[-1] + ".json", "w") as f:
                        json.dump(data_car_array, f, ensure_ascii=False)

                    filenames = os.listdir('../scraping detail/detail')
                    # print(filenames)
                    for file in filenames:
                        # print(file)
                        split = file.split(".")
                        print(split[0])
                        car_id = split[0]

                        with open("../scraping detail/detail/" + split[0] + ".json") as f:
                            data = json.load(f)
                        print(data)
                        print(data['ราคา'])

                        mycursor = mydb.cursor()

                        query = mycursor.execute("SELECT link FROM details WHERE car_id = " + car_id)
                        myresult = mycursor.fetchall()

                        print("มี ", mycursor.rowcount, "บรรทัด")
                        if mycursor.rowcount == 0:
                            sql1 = "INSERT INTO details (created_at, price, type, brand, model, face, submodel, year, motor, gear, seats, distance, color, image, car_id, location, link)" \
                                   " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            val1 = [
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
                            mycursor.executemany(sql1, val1)

                            sql2 = "UPDATE links SET read_at = %s WHERE active = %s AND car_id = %s"
                            val2 = (time, "Yes", car_id)
                            mycursor.execute(sql2, val2)

                            mydb.commit()

                        elif mycursor.rowcount >= 1:
                            sql = "UPDATE details SET updated_at = %s WHERE car_id = %s"
                            val = (time, car_id)
                            mycursor.execute(sql, val)

                            sql2 = "UPDATE links SET read_at = %s WHERE active = %s AND car_id = %s"
                            val2 = (time, "Yes", car_id)
                            mycursor.execute(sql2, val2)

                            mydb.commit()

                else:
                    print(">> ข้ า ม <<")

print("เสร็จเรียบร้อย")
#
#
# filenames = os.listdir('../scraping detail/detail')
# #print(filenames)
# for file in filenames:
#     #print(file)
#     split = file.split(".")
#     print(split[0])
#     car_id = split[0]


