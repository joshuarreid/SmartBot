import sqlite3
conn = sqlite3.connect('/Users/joshuareid/Documents/GitHub/SmartBotDatabase/SmartBot.db')
cur = conn.cursor()


def fetchLastFmUsername(user):
    user += "'"
    fetchGroupMeIDStatement = "SELECT GroupMeID FROM GroupMe WHERE name = '"
    cur.execute(fetchGroupMeIDStatement + user)
    GroupMeID = str(cur.fetchone()[0]) + "'"

    fetchLastFmStatement = "SELECT username FROM LastFm WHERE GroupMeID = '"
    cur.execute(fetchLastFmStatement + GroupMeID)
    lastFmUsername = cur.fetchone()[0]
    return str(lastFmUsername)

