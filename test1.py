import requests
import re
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from os import system


class My_train:
    def __init__(self, type, num, st, et, td, path):
        self.type = type
        self.num = num
        self.st = st
        self.et = et
        self.td = td
        self.path = path
        self.start_min = int(st.split(':')[0])*60+int(st.split(':')[1])
        self.end_min = int(et.split(':')[0])*60+int(et.split(':')[1])
        self.td_min = self.end_min-self.start_min
        if self.td_min < 0:
            self.td_min += 1440


start_month, start_day = map(int, input(
    "Enter the start date (MM/DD): ").split('/'))
end_month, end_day = map(int, input(
    "Enter the start date (MM/DD): ").split('/'))
d1 = date(2021, start_month, start_day)
d2 = date(2021, end_month, end_day)
delta = d2-d1

datas = []
print("processing ...")
for i in range(delta.days+1):
    day = d1+timedelta(days=i)
    day = str(day)
    days = day.split('-')
    day = '/'.join(days)
    my_data = {
        '_csrf': "a498de51-bbe2-48bb-a9fb-7c6bbef854db",
        'trainTypeList': 'ALL',
        'transfer': 'ONE',
        'startStation': '1000-臺北',
        'endStation': '4400-高雄',
        'rideDate': day,
        'startOrEndTime': 'true',
        'startTime': '00:00',
        'endTime': '23:59'
    }
    r = requests.post(
        'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip112/querybytime', data=my_data)

    soup = BeautifulSoup(r.text, 'html.parser')
    trains = soup.find_all("tr", class_="trip-column")
    for train in trains:
        r = train.find_all("td")
        type = re.search('\D+', r[0].find("a").text).group(0)
        if len(type) == 2:
            type = "  "+type
        num = re.search(r'\d+', r[0].find("a").text).group(0)
        st = r[1].text
        et = r[2].text
        td = r[3].text
        if len(td) == 8:
            td = td[:5]+" "+td[5:]
        path = r[4].text
        datas.append(My_train(type, num, st, et, td, path))


option = {'order': "", 'type': "", 'path': ""}


def print_data():
    data2 = []

    if option['type'] == '1':
        for data in datas:
            if data.type == '  莒光':
                data2.append(data)
    elif option['type'] == '2':
        for data in datas:
            if data.type == '  自強':
                data2.append(data)
    elif option['type'] == '3':
        for data in datas:
            if data.type == '普悠瑪':
                data2.append(data)
    else:
        data2 = datas

    data3 = []
    if option['path'] == '1':
        for data in data2:
            if data.path == '山線':
                data3.append(data)
    elif option['path'] == '2':
        for data in data2:
            if data.path == '海線':
                data3.append(data)
    else:
        data3 = data2

    if option['order'] == '1':
        data3.sort(key=lambda x: x.start_min)
    elif option['order'] == '2':
        print("hi")
        data3.sort(key=lambda x: x.td_min)
    for data in data3:
        print(data.type, data.num.rjust(3),
              data.st, data.et, data.td, data.path)


while True:
    c = input(
        "功能: 輸入'order'指定順序, 輸入'type'指定車種, 輸入'path'指定路線, 輸入'c'清空設定 ,輸入'p'print結果, 輸入'e'結束\n")
    if c == 'order':
        option['order'] = input("1:時間, 2:速度\n")
    elif c == 'type':
        option['type'] = input("1:莒光, 2:自強, 3:普悠瑪\n")
    elif c == 'path':
        option['path'] = input("1:山線, 2:海線\n")
    elif c == 'c':
        option['order'] = ''
        option['type'] = ''
        option['path'] = ''
    elif c == 'p':
        print_data()
    elif c == 'e':
        break
