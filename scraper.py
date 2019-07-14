import requests
import sqlite3
from bs4 import BeautifulSoup

dbname = "constituencies.sqlite"
conn = sqlite3.conn(dbname)

#URL to be scraped
url_to_sc::wqrape = 'https://www.ura.gov.sg/realEstateIIWeb/resources/misc/list_of_postal_districts.htm'
#Load html's plain data into a variable
plain_html_text = requests.get(url_to_scrape)
#parse the data
soup = BeautifulSoup(plain_html_text.text, "html.parser")

title = soup.title.string
table = soup.find("table")
rows = table.findAll("tr")
for row in rows:
    print(row.findAll("td")[1])
