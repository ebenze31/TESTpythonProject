# -*- coding: utf-8 -*-
import json
import os
import mysql.connector
import datetime as dt

time = dt.datetime.now()
#print(time)

mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="collect-all-cars"
    )
print("Connect")

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

for id_car in split_array:
    # print(id_car)
    id_car = id_car

    mycursor = mydb.cursor()

    query = mycursor.execute("SELECT link FROM links WHERE car_id = 111")
    myresult = mycursor.fetchall()

    print("มี ", mycursor.rowcount, "บรรทัด")
    if link_in_database == "":
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

    else:
        if mycursor.rowcount >= 1:
            sql = "UPDATE links SET updated_at = %s WHERE car_id = %s"
            val = (time, "111")
            mycursor.execute(sql, val)
            mydb.commit()
