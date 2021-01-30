# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import mysql.connector
import datetime
from datetime import datetime
import os

def funcDetail():
    time = datetime.now()
    print("TIME >>",time)

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="car"
    )
    print("Connect")

    mycursor = mydb.cursor()
    query = mycursor.execute("SELECT link FROM links WHERE active = 'Yes' ")
    myresult = mycursor.fetchall()
    for link in myresult:
        # print("link >>> ",link)
        url = str(link)
        u = url.split("'")
        url_detail = u[1]
        print("url_detail = ",url_detail)
        split_url = url_detail.split("/")
        # print("split_url -1 = ",split_url[-1])
        c = split_url[-1].split("'")
        cc = c[0].split("?")
        car_id = cc[0]
        # print("car_id  = ", car_id)
        location = split_url[-2]
        # print("location = ",location)

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
            "ลิงก์": "",
            "ประเภทเชื้อเพลิง": ""
        }

        # เช็ค read_at in links database
        mycursor = mydb.cursor()
        query = mycursor.execute("SELECT read_at FROM links WHERE active = 'Yes' AND car_id = " + car_id)
        myresult = mycursor.fetchall()
        for read_at in myresult:
            #print("read_at >>> ",read_at)
            if read_at == (None,):
                t = "None"
            else:
                read_str =  str(read_at)
                sp = read_str.split(" ")
                # print("เดือน = ",sp[1])
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
                elif sp[1] == "12,":
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
                # print("parsed_datetime >> ", parsed_datetime)
                t = time - parsed_datetime
                # print("timedelta >> ",t)
                # print("timedelta.day >> ",t.days)

            if t == "None":
                print(">>>>>>>>>>>>> read_at == none <<<<<<<<<<<<<<<")
                # ADD TO ARRAY
                data_car_array["ลิงก์"] = url_detail
                # ADD TO ARRAY
                data_car_array["สถานที่"] = location

                web_data = requests.get(url_detail)
                soup2 = BeautifulSoup(web_data.text,'html.parser')

                # หา รถที่ขายแล้ว เปลี่ยน active เป็น No
                error = soup2.find("div",{"class":"headline"})
                try:
                    error_404 = error.text
                except:
                    error_404 = "รถยังอยู่จ้าา"
                print("title >>",error_404)
                if error_404 == "รถคันนี้ได้ขายไปแล้ว":
                    mycursor = mydb.cursor()
                    sql = "UPDATE links SET active = %s , read_at = %s WHERE car_id = %s"
                    val = ("No", time, car_id)
                    mycursor.execute(sql, val)

                    sql_1 = "UPDATE details SET active = %s , updated_at = %s WHERE car_id = %s"
                    val_1 = ("No", time, car_id)
                    mycursor.execute(sql_1, val_1)

                    sql_2 = "UPDATE data_cars SET active = %s , updated_at = %s WHERE car_id_detail = %s"
                    val_2 = ("No", time, car_id)
                    mycursor.execute(sql_2, val_2)

                    mydb.commit()
                elif error_404 == None:

                # error_404 = soup2.find("title").text
                # print("title >>",error_404)
                # if error_404 == "ไม่ค้นพบหน้าที่คุณต้องการ - One2car.com":
                #     mycursor = mydb.cursor()
                #     sql = "UPDATE links SET active = %s , read_at = %s WHERE car_id = %s"
                #     val = ("No", time, car_id)
                #     mycursor.execute(sql, val)
                #     mydb.commit()
                #     break
                # elif error_404 == None:
                #     continue

                if soup2.find("div",{"class":"listing__price"}) == None :
                    print("ERROR")
                    # print(web_data.text)
                try:
                    price_car = soup2.find("div",{"class":"listing__price"}).text
                    if price_car == None:
                        continue
                    # print("price_car >> ",price_car)
                    # ADD TO ARRAY
                    data_car_array["ราคา"] = price_car
                except:
                    data_car_array["ราคา"] = "ติดต่อผู้ขาย"

                try:
                    type_car = soup2.find("div",{"class":"listing__title"}).text
                    #print(type_car)
                    split_type_car = type_car.split(" ")
                    #print(split_type_car)
                    #print(split_type_car[-1])
                    # ADD TO ARRAY
                    data_car_array["ประเภท"] = split_type_car[-1]
                except:
                    data_car_array["ประเภท"] = ""

                try:
                    img = soup2.find("div", {"class": "gallery__image"})
                    img_car = img.find('img')['data-src']
                    #print("IMG >>> "+img_car)
                    # ADD TO ARRAY
                    data_car_array["รูป"] = img_car
                except:
                    data_car_array["รูป"] = ""

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

                        if item.find_all('span')[0].text == "รัศมีการเลี้ยว" :
                            key = item.find_all('span')[0].text
                            value = item.find_all('span')[1].text
                            break
                        # ADD TO ARRAY
                        data_car_array[key] = value
                        #print(data_car_array)

                # save to json
                # print("car", json.dumps(data_car_array, ensure_ascii=False), "\n")
                with open("detail/" + car_id + ".json", "w") as f:
                    json.dump(data_car_array, f, ensure_ascii=False)

                # filenames = os.listdir('../scraping detail/detail')
                # # print(filenames)
                # for file in filenames:
                #     # print(file)
                #     split = file.split(".")
                #     print(split[0])
                #     car_id = split[0]

                with open("detail/" + car_id + ".json") as f:
                    data = json.load(f)
                # print(data)
                # print(data['ประเภทเชื้อเพลิง'])

                mycursor = mydb.cursor()

                sql_1 = "INSERT INTO details (created_at, price, type, brand, model, face, submodel, year, motor, gear, seats, distance, color, image, car_id, location, link, fuel, active)" \
                       " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val_1 = [
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
                     data['ลิงก์'],
                     data['ประเภทเชื้อเพลิง'],
                     "Yes")
                ]
                mycursor.executemany(sql_1, val_1)

                sql2 = "UPDATE links SET read_at = %s WHERE active = %s AND car_id = %s"
                val2 = (time, "Yes", car_id)
                mycursor.execute(sql2, val2)

                mydb.commit()

            elif int(t.days) > 7:
                print("--------- ค่ามากกว่า 7 ----------")
                mycursor = mydb.cursor()
                sql2 = "UPDATE links SET read_at = %s WHERE active = %s AND car_id = %s"
                val2 = (time, "Yes", car_id)
                mycursor.execute(sql2, val2)

                sql = "UPDATE details SET updated_at = %s WHERE active = %s AND car_id = %s"
                val = (time, "Yes", car_id)
                mycursor.execute(sql, val)

                mydb.commit()

                mycursor = mydb.cursor()
                query = mycursor.execute("SELECT link FROM links WHERE active = 'Yes' ")
                myresult = mycursor.fetchall()
                for link in myresult:
                    # print("link >>> ", link)
                    url = str(link)
                    u = url.split("'")
                    url_detail = u[1]
                    print("url_detail = ", url_detail)
                    split_url = url_detail.split("/")
                    # print("split_url -1 = ",split_url[-1])
                    c = split_url[-1].split("'")
                    car_id = c[0]
                    # print("car_id  = ", car_id)
                    location = split_url[-2]
                    # print("location = ", location)

                    # ADD TO ARRAY
                    data_car_array["ลิงก์"] = url_detail
                    # ADD TO ARRAY
                    data_car_array["สถานที่"] = location

                    web_data = requests.get(url_detail)
                    soup2 = BeautifulSoup(web_data.text, 'html.parser')

                    # หา รถที่ขายแล้ว เปลี่ยน active เป็น No
                    error = soup2.find("div", {"class": "headline"})
                    try:
                        error_404 = error.text
                    except:
                        error_404 = "รถยังอยู่จ้าา"
                    print("title >>", error_404)
                    if error_404 == "รถคันนี้ได้ขายไปแล้ว":
                        mycursor = mydb.cursor()
                        sql = "UPDATE links SET active = %s , read_at = %s WHERE car_id = %s"
                        val = ("No", time, car_id)
                        mycursor.execute(sql, val)

                        sql_1 = "UPDATE details SET active = %s , updated_at = %s WHERE car_id = %s"
                        val_1 = ("No", time, car_id)
                        mycursor.execute(sql_1, val_1)

                        sql_2 = "UPDATE data_cars SET active = %s , updated_at = %s WHERE car_id_detail = %s"
                        val_2 = ("No", time, car_id)
                        mycursor.execute(sql_2, val_2)

                        mydb.commit()
                    elif error_404 == "รถยังอยู่จ้าา":

                        # error_404 = soup2.find("title").text
                        # print("title >>",error_404)
                        # if error_404 == "ไม่ค้นพบหน้าที่คุณต้องการ - One2car.com":
                        #     mycursor = mydb.cursor()
                        #     sql = "UPDATE links SET active = %s , read_at = %s WHERE car_id = %s"
                        #     val = ("No", time, car_id)
                        #     mycursor.execute(sql, val)
                        #     mydb.commit()
                        #     break
                        # elif error_404 == None:
                        #     continue


                        if soup2.find("div", {"class": "listing__price"}) == None:
                            print("ERROR")
                            # print(web_data.text)

                        try:
                            price_car = soup2.find("div", {"class": "listing__price"}).text
                            if price_car == None:
                                continue
                            # print("price_car >> ",price_car)
                            # ADD TO ARRAY
                            data_car_array["ราคา"] = price_car
                        except:
                            data_car_array["ราคา"] = "ติดต่อผู้ขาย"

                        try:
                            type_car = soup2.find("div", {"class": "listing__title"}).text
                            # print(type_car)
                            split_type_car = type_car.split(" ")
                            # print(split_type_car)
                            # print(split_type_car[-1])
                            # ADD TO ARRAY
                            data_car_array["ประเภท"] = split_type_car[-1]
                        except:
                            data_car_array["ประเภท"] = ""

                        try:
                            img = soup2.find("div", {"class": "gallery__image"})
                            img_car = img.find('img')['data-src']
                            #print("IMG >>> " + img_car)
                            # ADD TO ARRAY
                            data_car_array["รูป"] = img_car
                        except:
                            data_car_array["รูป"] = ""

                        car = soup2.find_all("div", {"class": "list-item"})
                        for item in car:
                            if item.find('span') == None:
                                continue
                            if len(item.find_all('span')) == 2 or 3:
                                # print(item.find_all('span')[0].text, " / ", item.find_all('span')[1].text)
                                if item.find_all('span')[0].text == "ประเภทรถ":
                                    continue
                                if item.find_all('span')[0].text == "เล่มทะเบียน":
                                    continue

                                key = item.find_all('span')[0].text
                                value = item.find_all('span')[1].text

                                if item.find_all('span')[0].text == "รัศมีการเลี้ยว":
                                    key = item.find_all('span')[0].text
                                    value = item.find_all('span')[1].text
                                    break
                                # ADD TO ARRAY
                                data_car_array[key] = value
                                # print(data_car_array)

                        # save to json
                        # print("car", json.dumps(data_car_array, ensure_ascii=False), "\n")
                        with open("detail/" + car_id + ".json", "w") as f:
                            json.dump(data_car_array, f, ensure_ascii=False)

                        # filenames = os.listdir('../scraping detail/detail')
                        # # print(filenames)
                        # for file in filenames:
                        #     # print(file)
                        #     split = file.split(".")
                        #     print(split[0])
                        #     car_id = split[0]

                        try:
                            with open("../scraping detail/detail/" + car_id + ".json") as f:
                                data = json.load(f)
                        except:
                            continue
                        # print(data)
                        # print(data['ราคา'])

                        mycursor = mydb.cursor()
                        sql = "UPDATE details SET price = %s, type = %s, brand = %s, model = %s, face = %s," \
                               " submodel = %s, year = %s, motor = %s, gear = %s, seats = %s, distance = %s, color = %s," \
                               " image = %s, car_id = %s, location = %s, link = %s, fuel = %s WHERE car_id = %s"
                        val =(data['ราคา'],
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
                             data['ลิงก์'],
                             data['ประเภทเชื้อเพลิง'],
                             car_id)
                        mycursor.execute(sql, val)
                        mydb.commit()
            else:
                print(">> ข้ า ม <<")

    print("เสร็จเรียบร้อย")

