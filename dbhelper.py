import sqlite3


class DBHelper:
    def __init__(self, dbname="constituencies.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS districts (postal_code INTEGER, description text, UNIQUE(postal_code))"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, postal_code, district_text):
        stmt = "INSERT OR IGNORE INTO districts (postal_code, description) VALUES (?)"
        args = (postal_code, district_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()

#    def delete_item(self, item_text):
#        stmt = "DELETE FROM items WHERE description = (?)"
#        args = (item_text, )
#        self.conn.execute(stmt, args)
#        self.conn.commit()

    def get_items(self, postal_code):
        stmt = "SELECT description FROM districts WHERE postal_code = (?)"
        args = (postal_code, )
        return [x[0] for x in self.conn.execute(stmt, args)]
