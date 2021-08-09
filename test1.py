import requests
from bs4 import BeautifulSoup
my_data = {
    '_csrf': "a498de51-bbe2-48bb-a9fb-7c6bbef854db",
    'trainTypeList': 'ALL',
    'transfer': 'ONE',
    'startStation': '1000-臺北',
    'endStation': '4400-高雄',
    'rideDate': '2021/08/09',
    'startOrEndTime': 'true',
    'startTime': '00:00',
    'endTime': '23:59'
}
r = requests.post(
    'https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip112/querybytime', data=my_data)

soup = BeautifulSoup(r.text, 'html.parser')
x = soup.find("tr", class_="trip-column")
# print(x)
y = x.find_all("td")

print(y)
t1 = y[1].text
t2 = y[2].text
print(t1)
print(t2)

"""
x = soup.find("td", class_="coloum1").text
y = soup.find("td", class_="coloum3").text
z = soup.find("td", class_="coloum4").text
print(x+''+y+''+z)
"""
