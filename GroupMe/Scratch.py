import sqlite3
from LastFm import compareUsersTopArtists, lastfm_network, compareUsersTopTracks


conn = sqlite3.connect('/Users/joshuareid/Documents/GitHub/SmartBotDatabase/SmartBot.db')
cur = conn.cursor()

#cur.execute("INSERT INTO GroupMe VALUES (1, 'Joshua Reid', 1)")
#conn.commit()

cur.execute("SELECT GroupMeID FROM GroupMe WHERE name = 'Joshua Reid'")
GroupMeID = cur.fetchone()[0]
print("GroupMe ID of Joshua Reid: " + str(GroupMeID))

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

#print(combined)







#print("\r\n \r\n \r\n")

topTracksList = lastfm_network.get_user("carly_mac1").get_top_tracks(period = "overall", limit=5)
for item in topTracksList:
    similar = item.item.get_similar(limit=5)
    tagList = item.item.get_top_tags(limit=10)
    #tagOutput = "\r\n" + "Tags of " + item.item.title + ":     "
    #for tag in tagList:
        #tagOutput += str(tag.item) + ", "
    #print(tagOutput)
    for track in similar:
        similarTagList = track.item.get_top_tags()
        print("\r\nSimilar Track to " + item.item.title + ":     " + str(track.item) + " " + str(track.match))
        similarTagOutput = "Similar Tags of " + str(track.item) + ":     "
        for similarTag in similarTagList:
            if similarTag in tagList:
                similarTagOutput += str(similarTag.item) + ", "
        print(similarTagOutput)






