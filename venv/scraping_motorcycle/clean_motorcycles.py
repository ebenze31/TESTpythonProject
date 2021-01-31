import requests
import json
from bs4 import BeautifulSoup
import mysql.connector
import datetime
from datetime import datetime
import string
import os

time = datetime.now()
print("TIME >>",time)
def funcClean():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="car"
    )
    print("Connect")

    mycursor_1 = mydb.cursor()
    query_1 = mycursor_1.execute("SELECT created_at, updated_at, motorcycles_id, type, brand, model, submodel, year, gear, "
                                 "color, motor, price, img, location, link, clean_at FROM motorcycles_deatils WHERE active = 'Yes'")
    myresult_1 = mycursor_1.fetchall()

    for data in myresult_1:
        clean_at = data[-1]
        # print("clean_at == ", clean_at)
        if clean_at == None:
            print(">>>>>>>>> clean_at NONE <<<<<<<<<< ")

            # รหัสรถ
            motorcycles_id = data[2]
            print("รหัสรถ >> ", motorcycles_id)

            # ประเภท
            ty1 = data[3]
            ty2 = ty1.replace("\n", "")
            ty3 = ty2.replace("\t", "")
            type = ty3.replace(" ", "")
            print("ประเภท >> ", type)

            # ยี่ห้อ
            br1 = data[4]
            br2 = br1.replace("\n", "")
            br3 = br2.replace("\t", "")
            brand = br3.replace(" ", "")
            print("ยี่ห้อ >> ", brand)

            # รุ่น
            mo1 = data[5]
            mo2 = mo1.replace("\n", "")
            mo3 = mo2.replace("\t", "")
            model = mo3.replace(" ", "")
            print("รุ่น >> ", model)

            # รุ่นย่อย
            su1 = data[6]
            su2 = su1.replace("\n", "")
            su3 = su2.replace("\t", "")
            submodel = su3.replace(" ", "")
            print("รุ่นย่อย >> ", submodel)

            # ปี
            year = data[7]
            print("ปี >> ", year)

            # เกียร์
            ge1 = data[8]
            ge2 = ge1.replace("\n", "")
            ge3 = ge2.replace("\t", "")
            gear = ge3.replace(" ", "")
            print("เกียร์ >> ", gear)

            # สี
            co1 = data[9]
            co2 = co1.replace("\n", "")
            co3 = co2.replace("\t", "")
            color = co3.replace(" ", "")
            print("สี >> ", color)

            # เครื่องยนต์
            mo1 = data[10]
            mo2 = mo1.replace("\n", "")
            mo3 = mo2.replace("\t", "")
            motor = mo3.replace(" ", "")
            print("เครื่องยนต์ >> ", motor)

            # ราคา
            price = data[11]
            print("ราคา >> ", price)

            # รูป
            img = data[12]
            print("รูป >> ", img)

            # สถานที่
            location = data[13]
            print("สถานที่ >> ", location)

            # ลิงก์
            link = data[14]
            print("ลิงก์ >> ", link)

            print("---------------------------------------------------")

            mycursor = mydb.cursor()

            sql1 = "INSERT INTO motorcycles_datas (created_at, motorcycles_id, type, brand, model, submodel, year, gear, " \
                   "color, motor, price, img, location, link, active)" \
                   " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val1 = [
                (time,
                 motorcycles_id,
                 type,
                 brand,
                 model,
                 submodel,
                 year,
                 gear,
                 color,
                 motor,
                 price,
                 img,
                 location,
                 link,
                 "Yes")
            ]
            mycursor.executemany(sql1, val1)
            sql2 = "UPDATE motorcycles_deatils SET clean_at = %s WHERE motorcycles_id = %s"
            val2 = (time, motorcycles_id)
            mycursor.execute(sql2, val2)

            mydb.commit()
        else:
            t = time - clean_at
            print("จำนวนวันที่อ่านผ่านมาแล้ว >>>", t)
            if int(t.days) > 4:
                print(">>>>>>>> ทำงาน <<<<<<<<<<")
                print("มากกว่า 4")

                # รหัสรถ
                motorcycles_id = data[2]
                print("รหัสรถ >> ", motorcycles_id)

                # ประเภท
                ty1 = data[3]
                ty2 = ty1.replace("\n", "")
                ty3 = ty2.replace("\t", "")
                type = ty3.replace(" ", "")
                print("ประเภท >> ", type)

                # ยี่ห้อ
                br1 = data[4]
                br2 = br1.replace("\n", "")
                br3 = br2.replace("\t", "")
                brand = br3.replace(" ", "")
                print("ยี่ห้อ >> ", brand)

                # รุ่น
                mo1 = data[5]
                mo2 = mo1.replace("\n", "")
                mo3 = mo2.replace("\t", "")
                model = mo3.replace(" ", "")
                print("รุ่น >> ", model)

                # รุ่นย่อย
                su1 = data[6]
                su2 = su1.replace("\n", "")
                su3 = su2.replace("\t", "")
                submodel = su3.replace(" ", "")
                print("รุ่นย่อย >> ", submodel)

                # ปี
                year = data[7]
                print("ปี >> ", year)

                # เกียร์
                ge1 = data[8]
                ge2 = ge1.replace("\n", "")
                ge3 = ge2.replace("\t", "")
                gear = ge3.replace(" ", "")
                print("เกียร์ >> ", gear)

                # สี
                co1 = data[9]
                co2 = co1.replace("\n", "")
                co3 = co2.replace("\t", "")
                color = co3.replace(" ", "")
                print("สี >> ", color)

                # เครื่องยนต์
                mo1 = data[10]
                mo2 = mo1.replace("\n", "")
                mo3 = mo2.replace("\t", "")
                motor = mo3.replace(" ", "")
                print("เครื่องยนต์ >> ", motor)

                # ราคา
                price = data[11]
                print("ราคา >> ", price)

                # รูป
                img = data[12]
                print("รูป >> ", img)

                # สถานที่
                location = data[13]
                print("สถานที่ >> ", location)

                # ลิงก์
                link = data[14]
                print("ลิงก์ >> ", link)

                print("---------------------------------------------------")

                mycursor = mydb.cursor()

                sql = "UPDATE motorcycles_datas SET updated_at = %s, motorcycles_id= %s, type= %s, brand= %s, model= %s, submodel= %s," \
                      " year= %s, gear= %s,color= %s, motor= %s, price= %s, img= %s, location= %s, link= %s," \
                      " active= 'Yes' WHERE motorcycles_id = %s"
                val = (time, motorcycles_id, type, brand, model, submodel, year, gear, color, motor, price, img, location,
                       link, motorcycles_id)

                mycursor.execute(sql, val)

                sql2 = "UPDATE motorcycles_deatils SET clean_at = %s WHERE motorcycles_id = %s"
                val2 = (time, motorcycles_id)
                mycursor.execute(sql2, val2)

                mydb.commit()
            else:
                print(">>>>>>>> ข้ า ม <<<<<<<<<<")
                print("---------------------------------------------------")
