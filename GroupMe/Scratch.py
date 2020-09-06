import sqlite3

conn = sqlite3.connect('/Users/joshuareid/Documents/GitHub/SmartBotDatabase/SmartBot.db')
cur = conn.cursor()

#cur.execute("INSERT INTO GroupMe VALUES (1, 'Joshua Reid', 1)")
#conn.commit()

cur.execute("SELECT GroupMeID FROM GroupMe WHERE name = 'Joshua Reid'")
GroupMeID = cur.fetchone()[0]

def fetchLastFmUsername(user):
    user += "'"
    fetchGroupMeIDStatement = "SELECT GroupMeID FROM GroupMe WHERE name = '"
    cur.execute(fetchGroupMeIDStatement + user)
    GroupMeID = str(cur.fetchone()[0]) + "'"

    fetchLastFmStatement = "SELECT username FROM LastFm WHERE GroupMeID = '"
    cur.execute(fetchLastFmStatement + GroupMeID)
    lastFmUsername = cur.fetchone()[0]
    return lastFmUsername


cur.execute("SELECT username FROM LastFm INNER JOIN GroupMe ON GroupMe.GroupMeID = LastFm.GroupMeID WHERE GroupMe.name = 'Joshua Reid'")
print(cur.fetchall())

