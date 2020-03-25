from bs4 import BeautifulSoup
import requests
import sqlite3
headers = {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0"}
url = "https://en.wikipedia.org/wiki/Comparison_of_computer_viruses"
r = requests.get(url,headers=headers)
soup = BeautifulSoup(r.content, "html.parser")
table = soup.find_all('table')[1]
rows = table.find_all('tr')
row_list= list()
for tr in rows:
    td = tr.find_all('td')
    row = [i.text for i in td]
    row_list.append(row)
print(row_list)
print(row_list[1][1])
maldb = sqlite3.connect("maldb")
cursor = maldb.cursor()
cursor.execute('''drop table if exists mal''')
cursor.execute('''create table mal
            (virus text primRY key,
            alias text ,
            typeof text,
            subtype text,
            isolation_date text,
            isolation text,
            origin text,
            author text,
            notes text)
            ''')
cursor.executemany('''INSERT into mal values(?,?,?,?,?,?,?,?,?)''',
                   [row for row in row_list if len(row) == 9])
maldb.commit()
maldb.close()