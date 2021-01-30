# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup
import mysql.connector
import datetime
from datetime import datetime
import os

def funcDetail():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="car"
    )
    print("Connect")

    time = datetime.now()
    print("TIME >>",time)

    mycursor = mydb.cursor()
    query = mycursor.execute("SELECT link FROM motorcycles_links WHERE active = 'Yes' ")
    myresult = mycursor.fetchall()
    for link in myresult:
        # print("link >>> ",link)
        url = str(link)
        u = url.split("'")
        url_detail = u[1]
        print("url_detail = ", url_detail)
        split_url = url_detail.split("-")
        sp = split_url[-1].split(".")
        motorcycles_id = sp[0]
        print("motorcycles_id = ", motorcycles_id)

        data_motorcycles_array = {
            "ประเภท": "",
            "ยี่ห้อ": "",
            "รุ่น": "",
            "รุ่นย่อย": "",
            "ปี": "",
            "เกียร์": "",
            "สี": "",
            "เครื่องยนต์": "",
            "ราคา": "",
            "รูป": "",
            "สถานที่": "",
            "ลิงก์": ""
        }

        # เช็ค read_at in links database
        mycursor = mydb.cursor()
        query = mycursor.execute("SELECT read_at FROM motorcycles_links WHERE active = 'Yes' AND motorcycles_id = " + motorcycles_id)
        myresult = mycursor.fetchall()
        for read_at in myresult:
            # print("read_at >>> ",read_at)
            if read_at == (None,):
                t = "None"
            else:
                read_str = str(read_at)
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
                # print("SP 0 >> ", sp[0])
                sp_year = sp[0].split("(")
                # print("sp_year >> ", sp_year)
                sp_sec = sp[5].split(")")
                # print("sp_sec >> ", sp_sec)
                l_read = sp[2] + " " + month + " " + sp_year[-1] + " at " + sp[3] + ":" + sp[4] + ":" + sp_sec[0]
                last_read = l_read.replace(",", "")
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
                data_motorcycles_array["ลิงก์"] = url_detail

                web_data = requests.get(url_detail)
                soup2 = BeautifulSoup(web_data.text, 'html.parser')

                # หา รถที่ขายแล้ว เปลี่ยน active เป็น No
                er= soup2.find("div", {"class": "price"})
                error = er.text
                # print("title >> ",error)
                if error == "อุ๊บส์! ประกาศนี้ไม่มีในระบบแล้ว":
                    mycursor = mydb.cursor()
                    sql = "UPDATE motorcycles_links SET active = %s , read_at = %s WHERE motorcycles_id = %s"
                    val = ("No", time, motorcycles_id)
                    mycursor.execute(sql, val)

                    sql_1 = "UPDATE motorcycles_deatils SET active = %s , updated_at = %s WHERE motorcycles_id = %s"
                    val_1 = ("No", time, motorcycles_id)
                    mycursor.execute(sql_1, val_1)

                    # sql_2 = "UPDATE data_cars SET active = %s , updated_at = %s WHERE car_id_detail = %s"
                    # val_2 = ("No", time, car_id)
                    # mycursor.execute(sql_2, val_2)

                    mydb.commit()
                else:
                    # รูปภาพ
                    im1 = soup2.find("div",{"class":"fotorama"})
                    img = im1.find('img')['src']
                    # img = im1['src']
                    data_motorcycles_array["รูป"] = img
                    # print("IMG >> ", img)

                    # ราคา
                    pr1 = soup2.find("div", {"class": "price"})
                    price = str(pr1['data-price'])
                    data_motorcycles_array["ราคา"] = price
                    # print("ราคา >> ",price)

                    # ประเภท , ยี่ห้อ , รุ่น , รุ่นย่อย
                    t_total = soup2.find("div", {"class": "features_table"})
                    line = t_total.find("div", {"class": "line"})
                    li = line.text.replace("ประเภท :\n","")
                    li2 = li.split(",")
                    # print("li" , li)

                    # ประเภท
                    type = li2[0]
                    data_motorcycles_array["ประเภท"] = type

                    # ยี่ห้อ
                    brand = li2[1]
                    data_motorcycles_array["ยี่ห้อ"] = brand

                    # รุ่น
                    model = li2[2]
                    data_motorcycles_array["รุ่น"] = model

                    # รุ่นย่อย
                    try:
                        submodel = li2[3]
                        data_motorcycles_array["รุ่นย่อย"] = submodel
                    except:
                        submodel = ""
                        data_motorcycles_array["รุ่นย่อย"] = submodel

                    # print("type >> ", type)
                    # print("brand >> ", brand)
                    # print("model >> ", model)
                    # print("submodel >> ", submodel)

                    # ปี
                    text_year = soup2.find(text="ปี :")
                    ye = text_year.parent
                    ye2 = ye.parent
                    ye3 = ye2.findNext('a')
                    year = ye3.contents[0]
                    data_motorcycles_array["ปี"] = year
                    # print ("year = ", year)

                    # เกียร์
                    text_gear = soup2.find(text="เกียร์ :")
                    ge = text_gear.parent
                    ge2 = ge.parent
                    gear = ge2.text.replace("เกียร์ :\n","")
                    data_motorcycles_array["เกียร์"] = gear
                    # print ("gear = ", gear)

                    # สี
                    text_color = soup2.find(text="สี :")
                    co = text_color.parent
                    co2 = co.parent
                    color = co2.text.replace("สี :\n", "")
                    data_motorcycles_array["สี"] = color
                    # print ("color = ", color)

                    # เครื่องยนต์
                    text_motor = soup2.find(text="เครื่องยนต์ :")
                    mo = text_motor.parent
                    mo2 = mo.parent
                    motor = mo2.text.replace("เครื่องยนต์ :\n", "")
                    data_motorcycles_array["เครื่องยนต์"] = motor
                    # print ("motor = ", motor)

                    # สถานที่
                    text_location = soup2.find(text="จุดนัดดูรถ :")
                    lo = text_location.parent
                    lo2 = lo.parent
                    lo3 = lo2.findNext('a')
                    loca = lo3.contents[0]
                    location = loca.text
                    data_motorcycles_array["สถานที่"] = location
                    # print ("location = ", location)


                    with open("detail/" + motorcycles_id + ".json", "w") as f:
                        json.dump(data_motorcycles_array, f, ensure_ascii=False)

                    with open("detail/" + motorcycles_id + ".json") as f:
                        data = json.load(f)

                    mycursor = mydb.cursor()

                    sql_1 = "INSERT INTO motorcycles_deatils (created_at, motorcycles_id, type, brand, model, submodel, year, gear, color, motor, price, img, location, link, active)" \
                           " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    val_1 = [
                        (time,
                         motorcycles_id,
                         data['ประเภท'],
                         data['ยี่ห้อ'],
                         data['รุ่น'],
                         data['รุ่นย่อย'],
                         data['ปี'],
                         data['เกียร์'],
                         data['สี'],
                         data['เครื่องยนต์'],
                         data['ราคา'],
                         data['รูป'],
                         data['สถานที่'],
                         data['ลิงก์'],
                         "Yes")
                    ]
                    mycursor.executemany(sql_1, val_1)

                    sql2 = "UPDATE motorcycles_links SET read_at = %s WHERE active = %s AND motorcycles_id = %s"
                    val2 = (time, "Yes", motorcycles_id)
                    mycursor.execute(sql2, val2)

                    mydb.commit()

            elif int(t.days) > 4:
                print("--------- ค่ามากกว่า 4 ----------")

                mycursor = mydb.cursor()
                sql2 = "UPDATE motorcycles_links SET read_at = %s WHERE active = %s AND motorcycles_id = %s"
                val2 = (time, "Yes", motorcycles_id)
                mycursor.execute(sql2, val2)

                sql = "UPDATE motorcycles_deatils SET updated_at = %s WHERE active = %s AND motorcycles_id = %s"
                val = (time, "Yes", motorcycles_id)
                mycursor.execute(sql, val)

                mydb.commit()

                # ADD TO ARRAY
                data_motorcycles_array["ลิงก์"] = url_detail

                web_data = requests.get(url_detail)
                soup2 = BeautifulSoup(web_data.text, 'html.parser')

                # หา รถที่ขายแล้ว เปลี่ยน active เป็น No
                er = soup2.find("div", {"class": "price"})
                error = er.text
                # print("title >> ",error)
                if error == "อุ๊บส์! ประกาศนี้ไม่มีในระบบแล้ว":
                    mycursor = mydb.cursor()
                    sql = "UPDATE motorcycles_links SET active = %s , read_at = %s WHERE motorcycles_id = %s"
                    val = ("No", time, motorcycles_id)
                    mycursor.execute(sql, val)

                    sql_1 = "UPDATE motorcycles_deatils SET active = %s , updated_at = %s WHERE motorcycles_id = %s"
                    val_1 = ("No", time, motorcycles_id)
                    mycursor.execute(sql_1, val_1)

                    # sql_2 = "UPDATE data_cars SET active = %s , updated_at = %s WHERE car_id_detail = %s"
                    # val_2 = ("No", time, car_id)
                    # mycursor.execute(sql_2, val_2)

                    mydb.commit()
                else:
                    # รูปภาพ
                    im1 = soup2.find("div", {"class": "fotorama"})
                    img = im1.find('img')['src']
                    # img = im1['src']
                    data_motorcycles_array["รูป"] = img
                    # print("IMG >> ", img)

                    # ราคา
                    pr1 = soup2.find("div", {"class": "price"})
                    price = str(pr1['data-price'])
                    data_motorcycles_array["ราคา"] = price
                    # print("ราคา >> ",price)

                    # ประเภท , ยี่ห้อ , รุ่น , รุ่นย่อย
                    t_total = soup2.find("div", {"class": "features_table"})
                    line = t_total.find("div", {"class": "line"})
                    li = line.text.replace("ประเภท :\n", "")
                    li2 = li.split(",")
                    # print("li" , li)

                    # ประเภท
                    type = li2[0]
                    data_motorcycles_array["ประเภท"] = type

                    # ยี่ห้อ
                    brand = li2[1]
                    data_motorcycles_array["ยี่ห้อ"] = brand

                    # รุ่น
                    model = li2[2]
                    data_motorcycles_array["รุ่น"] = model

                    # รุ่นย่อย
                    try:
                        submodel = li2[3]
                        data_motorcycles_array["รุ่นย่อย"] = submodel
                    except:
                        submodel = ""
                        data_motorcycles_array["รุ่นย่อย"] = submodel

                    # print("type >> ", type)
                    # print("brand >> ", brand)
                    # print("model >> ", model)
                    # print("submodel >> ", submodel)

                    # ปี
                    text_year = soup2.find(text="ปี :")
                    ye = text_year.parent
                    ye2 = ye.parent
                    ye3 = ye2.findNext('a')
                    year = ye3.contents[0]
                    data_motorcycles_array["ปี"] = year
                    # print ("year = ", year)

                    # เกียร์
                    text_gear = soup2.find(text="เกียร์ :")
                    ge = text_gear.parent
                    ge2 = ge.parent
                    gear = ge2.text.replace("เกียร์ :\n", "")
                    data_motorcycles_array["เกียร์"] = gear
                    # print ("gear = ", gear)

                    # สี
                    text_color = soup2.find(text="สี :")
                    co = text_color.parent
                    co2 = co.parent
                    color = co2.text.replace("สี :\n", "")
                    data_motorcycles_array["สี"] = color
                    # print ("color = ", color)

                    # เครื่องยนต์
                    text_motor = soup2.find(text="เครื่องยนต์ :")
                    mo = text_motor.parent
                    mo2 = mo.parent
                    motor = mo2.text.replace("เครื่องยนต์ :\n", "")
                    data_motorcycles_array["เครื่องยนต์"] = motor
                    # print ("motor = ", motor)

                    # สถานที่
                    text_location = soup2.find(text="จุดนัดดูรถ :")
                    lo = text_location.parent
                    lo2 = lo.parent
                    lo3 = lo2.findNext('a')
                    loca = lo3.contents[0]
                    location = loca.text
                    data_motorcycles_array["สถานที่"] = location
                    # print ("location = ", location)

                    with open("detail/" + motorcycles_id + ".json", "w") as f:
                        json.dump(data_motorcycles_array, f, ensure_ascii=False)

                    with open("detail/" + motorcycles_id + ".json") as f:
                        data = json.load(f)

                    mycursor = mydb.cursor()

                    sql = "UPDATE motorcycles_deatils SET motorcycles_id = %s, type = %s, brand = %s, model = %s, submodel = %s," \
                          " year = %s, gear = %s, color = %s, motor = %s, price = %s, img = %s, location = %s," \
                          " link = %s, active = %s WHERE motorcycles_id = %s"
                    val = (motorcycles_id,
                           data['ประเภท'],
                           data['ยี่ห้อ'],
                           data['รุ่น'],
                           data['รุ่นย่อย'],
                           data['ปี'],
                           data['เกียร์'],
                           data['สี'],
                           data['เครื่องยนต์'],
                           data['ราคา'],
                           data['รูป'],
                           data['สถานที่'],
                           data['ลิงก์'],
                           "Yes",
                           motorcycles_id)
                    mycursor.execute(sql, val)
                    mydb.commit()

            else:
                print(">> ข้ า ม <<")

        print("เสร็จเรียบร้อย")


