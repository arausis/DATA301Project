import pandas as pd
import requests
from bs4 import BeautifulSoup
from icecream import ic
import csv

headers = {
    'User-Agent': r"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 " ,
    'Accept-Language': 'en-US,en;q=0.5'
}

url = "https://catalog.calpoly.edu/facultyandstaff/#facultystaffemeritustext"

def extract_columns(row_tag):
    """
    Extracts and prints columns from a given table row tag.

    :param row_tag: BeautifulSoup tag representing the table row
    :return: List of column texts
    """
    columns = row_tag.find_all('td')
    column_texts = [column.get_text(separator=" ", strip=True) for column in columns]
    return column_texts

response = requests.get(url, headers = headers)
soup = BeautifulSoup(response.content, "html.parser")

tab = soup.find_all("table")[-1]
rows = tab.find_all("tr")[1:]

with open("position.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "year", "dept", "position", "education"])

    for row in rows:

        cols = extract_columns(row)

        temp, position, education = tuple(cols)

        if(temp.count("(") == 1):
            name, temp = tuple(temp.split("("))
            year, dept = tuple(temp.split(")"))
            cRow=[name.strip(), year.strip(), dept.strip(), position.strip(), education.strip()]        

            writer.writerow(cRow)
        else:
            print(cols)


