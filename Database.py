import sqlite3
from Token import databaseLocation

conn = sqlite3.connect(databaseLocation)
cur = conn.cursor()



def getLastFmUsername(user):
    user += "'"
    fetchLastFmStatement = "SELECT username FROM LastFm INNER JOIN GroupMe ON GroupMe.GroupMeID = LastFm.GroupMeID WHERE GroupMe.name = '"
    cur.execute(fetchLastFmStatement + user)
    lastFmUsername = str(cur.fetchone()[0])
    return str(lastFmUsername)
