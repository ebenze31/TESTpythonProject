import requests
import json
from bs4 import BeautifulSoup
import mysql.connector
import datetime
from datetime import datetime
import string
import os

def funcClean():
    time = datetime.now()
    print("TIME >>",time)

    mydb = mysql.connector.connect(
        host="159.65.128.190",
        user="viicheck2",
        password="viicheck",
        database="viicheck"
    )
    print("Connect")

    mycursor_1 = mydb.cursor()
    query_1 = mycursor_1.execute("SELECT created_at, updated_at, price, type, brand, model, submodel, year, motor, "
                                 "gear, seats, distance, color, image, location, link, clean_at, fuel, car_id FROM details WHERE active = 'Yes'")
    myresult_1 = mycursor_1.fetchall()

    for data in myresult_1:
        clean_at = data[16]
        print("clean_at == ", clean_at)
        if clean_at == None:
            print(">>>>>>>>> clean_at NONE <<<<<<<<<< ")

            print("---------------------------------------------------")
            # รหัสรถ
            car_id_detail = data[-1]
            print("รหัสรถ >> ", car_id_detail)

            # ราคา
            price_old = data[2]
            p = price_old.split("%")
            pp = p[-1].replace("บาท","")
            ppp = pp.replace("\n","")
            price = ppp.replace(",","")
            # print("ราคาเดิม >>> ",p)
            print("ราคา >>> ", price)

            # ประเภท
            t = data[3].replace("...","")
            type = t.replace("\n","")
            print("ประเภทรถ >>> ", type)

            # ยี่ห้อ
            brand = data[4]
            print("ยี่ห้อ >>> ", brand)

            # รุ่น
            model = data[5]
            print("รุ่น >>> ", model)

            # รุ่นย่อย
            submodel = data[6]
            print("รุ่นย่อย >>> ", submodel)

            # ปีที่ผลิต
            year = data[7]
            print("ปีที่ผลิต >>> ", year)

            # เครื่องยนต์
            motor_old = data[8]
            motor = motor_old.replace("ซีซี","")
            print("เครื่องยนต์ >>> ", motor)

            # ระบบเกียร์
            gear = data[9]
            print("ระบบเกียร์ >>> ", gear)

            # จำนวนที่นั่ง
            seats = data[10]
            print("จำนวนที่นั่ง >>> ", seats)

            # เลขไมล์
            distance_old = data[11]
            distance = distance_old.replace("K", "")
            print("เลขไมล์ >>> ", distance)

            # สี
            color = data[12]
            print("สี >>> ", color)

            # รูปภาพ
            image = data[13]
            print("รูปภาพ >>> ", image)

            # สถานที่
            location_old = data[14]
            # ลบ A - Z
            lo_a = location_old.replace("a", "")
            lo_b = lo_a.replace("b", "")
            lo_c = lo_b.replace("c", "")
            lo_d = lo_c.replace("d", "")
            lo_e = lo_d.replace("e", "")
            lo_f = lo_e.replace("f", "")
            lo_g = lo_f.replace("g", "")
            lo_h = lo_g.replace("h", "")
            lo_i = lo_h.replace("i", "")
            lo_j = lo_i.replace("j", "")
            lo_k = lo_j.replace("k", "")
            lo_l = lo_k.replace("l", "")
            lo_m = lo_l.replace("m", "")
            lo_n = lo_m.replace("n", "")
            lo_o = lo_n.replace("o", "")
            lo_p = lo_o.replace("p", "")
            lo_q = lo_p.replace("q", "")
            lo_r = lo_q.replace("r", "")
            lo_s = lo_r.replace("s", "")
            lo_t = lo_s.replace("t", "")
            lo_u = lo_t.replace("u", "")
            lo_v = lo_u.replace("v", "")
            lo_w = lo_v.replace("w", "")
            lo_x = lo_w.replace("x", "")
            lo_y = lo_x.replace("y", "")
            lo_z = lo_y.replace("z", "")

            # ลบ 0 - 9
            lo_0 = lo_z.replace("0", "")
            lo_1 = lo_0.replace("1", "")
            lo_2 = lo_1.replace("2", "")
            lo_3 = lo_2.replace("3", "")
            lo_4 = lo_3.replace("4", "")
            lo_5 = lo_4.replace("5", "")
            lo_6 = lo_5.replace("6", "")
            lo_7 = lo_6.replace("7", "")
            lo_8 = lo_7.replace("8", "")
            lo_9 = lo_8.replace("9", "")
            ll = lo_9.replace("-", " ")
            location = ll.strip()
            print("สถานที่ >>> ", location)

            # ลิงก์
            link = data[15]
            print("ลิงก์ >>> ", link)

            # ประเภทเชื้อเพลิง
            fuel = data[17]
            print("ประเภทเชื้อเพลิง >>> ", fuel)

            mycursor = mydb.cursor()

            sql1 = "INSERT INTO data_cars (created_at, price, type, brand, model, submodel, year, motor, gear, " \
                   "seats, distance, color, image, location, link, car_id_detail, fuel, active)" \
                   " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val1 = [
                (time,
                 price,
                 type,
                 brand,
                 model,
                 submodel,
                 year,
                 motor,
                 gear,
                 seats,
                 distance,
                 color,
                 image,
                 location,
                 link,
                 car_id_detail,
                 fuel,
                 "Yes")
            ]
            mycursor.executemany(sql1, val1)
            sql2 = "UPDATE details SET clean_at = %s WHERE car_id = %s"
            val2 = (time,  car_id_detail)
            mycursor.execute(sql2, val2)

            mydb.commit()
        else:
            t = time - clean_at
            print("จำนวนวันที่อ่านผ่านมาแล้ว >>>",t)
            if int(t.days) > 7:
                print(">>>>>>>> ทำงาน <<<<<<<<<<")
                print("มากกว่า 7")
                # รหัสรถ
                car_id_detail = data[-1]
                print("รหัสรถ >> ", car_id_detail)

                # ราคา
                price_old = data[2]
                p = price_old.split("%")
                pp = p[-1].replace("บาท", "")
                ppp = pp.replace("\n", "")
                price = ppp.replace(",", "")
                # print("ราคาเดิม >>> ",p)
                print("ราคา >>> ", price)

                # ประเภท
                t = data[3].replace("...", "")
                type = t.replace("\n", "")
                print("ประเภทรถ >>> ", type)

                # ยี่ห้อ
                brand = data[4]
                print("ยี่ห้อ >>> ", brand)

                # รุ่น
                model = data[5]
                print("รุ่น >>> ", model)

                # รุ่นย่อย
                submodel = data[6]
                print("รุ่นย่อย >>> ", submodel)

                # ปีที่ผลิต
                year = data[7]
                print("ปีที่ผลิต >>> ", year)

                # เครื่องยนต์
                motor_old = data[8]
                motor = motor_old.replace("ซีซี", "")
                print("เครื่องยนต์ >>> ", motor)

                # ระบบเกียร์
                gear = data[9]
                print("ระบบเกียร์ >>> ", gear)

                # จำนวนที่นั่ง
                seats = data[10]
                print("จำนวนที่นั่ง >>> ", seats)

                # เลขไมล์
                distance_old = data[11]
                distance = distance_old.replace("K", "")
                print("เลขไมล์ >>> ", distance)

                # สี
                color = data[12]
                print("สี >>> ", color)

                # รูปภาพ
                image = data[13]
                print("รูปภาพ >>> ", image)

                # สถานที่
                location_old = data[14]
                # ลบ A - Z
                lo_a = location_old.replace("a", "")
                lo_b = lo_a.replace("b", "")
                lo_c = lo_b.replace("c", "")
                lo_d = lo_c.replace("d", "")
                lo_e = lo_d.replace("e", "")
                lo_f = lo_e.replace("f", "")
                lo_g = lo_f.replace("g", "")
                lo_h = lo_g.replace("h", "")
                lo_i = lo_h.replace("i", "")
                lo_j = lo_i.replace("j", "")
                lo_k = lo_j.replace("k", "")
                lo_l = lo_k.replace("l", "")
                lo_m = lo_l.replace("m", "")
                lo_n = lo_m.replace("n", "")
                lo_o = lo_n.replace("o", "")
                lo_p = lo_o.replace("p", "")
                lo_q = lo_p.replace("q", "")
                lo_r = lo_q.replace("r", "")
                lo_s = lo_r.replace("s", "")
                lo_t = lo_s.replace("t", "")
                lo_u = lo_t.replace("u", "")
                lo_v = lo_u.replace("v", "")
                lo_w = lo_v.replace("w", "")
                lo_x = lo_w.replace("x", "")
                lo_y = lo_x.replace("y", "")
                lo_z = lo_y.replace("z", "")

                # ลบ 0 - 9
                lo_0 = lo_z.replace("0", "")
                lo_1 = lo_0.replace("1", "")
                lo_2 = lo_1.replace("2", "")
                lo_3 = lo_2.replace("3", "")
                lo_4 = lo_3.replace("4", "")
                lo_5 = lo_4.replace("5", "")
                lo_6 = lo_5.replace("6", "")
                lo_7 = lo_6.replace("7", "")
                lo_8 = lo_7.replace("8", "")
                lo_9 = lo_8.replace("9", "")
                ll = lo_9.replace("-", " ")
                location = ll.strip()
                print("สถานที่ >>> ", location)

                # ลิงก์
                link = data[15]
                print("ลิงก์ >>> ", link)

                # ประเภทเชื้อเพลิง
                fuel = data[17]
                print("ประเภทเชื้อเพลิง >>> ", fuel)

                mycursor = mydb.cursor()

                sql = "UPDATE data_cars SET updated_at = %s, price= %s, type= %s, brand= %s, model= %s, submodel= %s," \
                        " year= %s, motor= %s,gear= %s, seats= %s, distance= %s, color= %s, image= %s, location= %s," \
                        " link= %s, car_id_detail= %s, fuel= %s, active= 'Yes' WHERE car_id_detail = %s"
                val = (time, price, type, brand, model, submodel, year, motor, gear, seats, distance, color, image,
                         location, link, car_id_detail,fuel, car_id_detail)

                mycursor.execute(sql, val)

                sql2 = "UPDATE details SET clean_at = %s WHERE car_id = %s"
                val2 = (time, car_id_detail)
                mycursor.execute(sql2, val2)

                mydb.commit()
            else:
                print(">>>>>>>> ข้ า ม <<<<<<<<<<")
                print("---------------------------------------------------")

