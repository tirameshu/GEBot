import requests
import sqlite3
from bs4 import BeautifulSoup


class DBHelper:
    def __init__(self, dbname="constituencies.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
        self.has_setup = False

    def setup(self):
        # only postal code is unique because different districts could have same MP, and different areas could belong to same district
        stmt = "CREATE TABLE IF NOT EXISTS constituencies (district TEXT, postal_code TEXT, description TEXT, UNIQUE(district, postal_code, description))"
        self.conn.execute(stmt)
        self.conn.commit()

        if self.has_setup:
            return
        url_to_scrape = "https://www.ura.gov.sg/realEstateIIWeb/resources/misc/list_of_postal_districts.htm"
        plain_html_text = requests.get(url_to_scrape)
        soup = BeautifulSoup(plain_html_text.text, "html.parser")

        table = soup.find("table")
        rows = table.findAll("tr")
        for row in rows:
            entry = row.findAll("td")
            district = entry[0].text
            digits = entry[1].text
            desc = entry[2].text
            self.add_item(district, digits, desc)
        self.has_setup = True

    def add_item(self, district, postal_code, district_text):
        stmt = "INSERT OR IGNORE INTO constituencies (district, postal_code, description) VALUES (?, ?, ?)"
        args = (district, postal_code, district_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()

#    def delete_item(self, item_text):
#        stmt = "DELETE FROM items WHERE description = (?)"
#        args = (item_text, )
#        self.conn.execute(stmt, args)
#        self.conn.commit()

    def get_items(self, postal_code):
        # stmt = "SELECT description FROM districts WHERE postal_code = (?)"
        # args = (postal_code, )
        # return [x[0] for x in self.conn.execute(stmt, args)]
        digits = postal_code[:2]
        stmt = "SELECT description FROM constituencies WHERE postal_code LIKE '%'||(?)||'%'" # i think variables must be enclosed in ||
        args = (digits, )
        # execute returns a cursor, data extracted with for-loop
        
        result = [x[0] for x in self.conn.execute(stmt, args)]
        if not result:
            return False
        info = result[0].strip("\n")
        string = ""
        backslash, space = False, False
        for c in info:
            if ord(c) == 92:
                backslash = True
            elif backslash:
                backslash = False
                continue
            elif (65 <= ord(c) <= 90 or 97 <= ord(c) <= 122 or ord(c) == 44):
                string += c
                space = False
            elif ord(c) == 32 and (not space):
                space = True
                string += c
        return [string.strip()]


#    def exists(self, postal_code):
#        if self.get_items(postal_code): # assuming get_items returns a 1-d list
#            return false
#        return false

