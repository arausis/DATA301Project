import pandas as pd
import requests
from bs4 import BeautifulSoup
from icecream import ic
import csv

headers = {
    'User-Agent': r"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 " ,
    'Accept-Language': 'en-US,en;q=0.5'
}

url = "https://afd.calpoly.edu/payroll/compensation_report/state/"

response = requests.get(url, headers = headers)
soup = BeautifulSoup(response.content, "html.parser")

doc = soup.find('div', id='large_report')

names = doc.find_all("h3")
tables = doc.find_all("table")

with open("salaries.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow( ("name", "avgPay"))

    for i in range(len(names)):
        name = names[i].text

        earnings = tables[i].find_all("td")[-3:]
        nonzero = [float(e.text.replace(",", "")) for e in earnings if float(e.text.replace(",", "") ) > 0]

        if len(nonzero) > 0:
            avg = sum(nonzero) / len(nonzero)
        else:
            avg = 0

        ic(name)
        ic(avg)
        writer.writerow((name,avg))

