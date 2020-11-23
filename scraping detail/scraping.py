# -*- coding: utf-8 -*-
import requests
import json
from bs4 import BeautifulSoup

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
                "สี": ""
            }
            url_detail = url

            id_car = url_detail.split("/")
            print(id_car)
            print(id_car[-1])

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



