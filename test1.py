import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta


class My_train:
    def __init__(self, num, st, et, td, path):
        self.num = num
        self.st = st
        self.et = et
        self.td = td
        self.path = path


start_month, start_day = map(int, input(
    "Enter the start date (MM/DD): ").split('/'))
end_month, end_day = map(int, input(
    "Enter the start date (MM/DD): ").split('/'))
d1 = date(2021, start_month, start_day)
d2 = date(2021, end_month, end_day)
delta = d2-d1

datas = []

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

        num = r[0].find("a").text
        st = r[1].text
        et = r[2].text
        td = r[3].text
        path = r[4].text
        datas.append(My_train(num, st, et, td, path))

for data in datas:
    print(data.num, data.st, data.et, data.td, data.path)
