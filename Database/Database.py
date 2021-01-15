import pandas as pd
import sqlite3 as sql
from Token import databaseLocation

class Database:
    """The Database Class

    The Database class is responsible for connecting each command library with its
    database table.

    """
    def __init__(self, database_name):
        con = sql.connect(databaseLocation)
        self.df = pd.read_sql_query("SELECT * from " + database_name, con)
        cur = con.cursor()


    def printDatabase(self):
        print(self.df.head(5))






