import sqlite3
from LastFm import compareUsersTopArtists, compareUsersTopTracks

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
#print(cur.fetchall())
list1 = [1,2,3]
list2 = [1,3,4]
combined = list(set.intersection(set(list1), set(list2)))
print(combined)


comparedArtists = compareUsersTopArtists("bumi_", "carly_mac1", "week")
for item in comparedArtists:
    print(item)

print("\r\n \r\n \r\n")

comparedTracks = compareUsersTopTracks("bumi_", "carly_mac1", "week")
for item in comparedTracks:
    print(item)





