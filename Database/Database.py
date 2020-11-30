import pandas as pd
import sqlite3 as sql
from Token import databaseLocation

class Database:
    """The LastfmAPIWrapper Class

    The LastfmAPIWrapper class contains all the commands their methods for the
    interacting with a Sqlite3 database through the pandas library.

    """
    def __init__(self, database_name):
        con = sql.connect(databaseLocation)
        self.df = pd.read_sql_query("SELECT * from " + database_name, con)
        cur = con.cursor()


    def printDatabase(self):
        print(self.df.head(5))






