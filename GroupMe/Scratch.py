import pylast
from Token import lastfm_network, lastfm_username
import Timestamp
topTracksList = lastfm_network.get_user("bumi_").get_top_artists(period="12month", limit=50)
counter = 1
for item in topTracksList:
    print(item)

