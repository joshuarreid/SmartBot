import pylast
from Token import lastfm_network, lastfm_username
import Timestamp

LASTFM = lastfm_network.get_user(lastfm_username)


### Grabs played tracks within a time interval ###
def getTracks(time_from, time_to):
    tracks = LASTFM.get_recent_tracks(cacheable=False, limit=None, time_from=time_from, time_to=time_to)
    return tracks


### Grabs played tracks from last 24 hours ###
def lastDayTracks():
    lastDayTracksList = getTracks(int(Timestamp.twentyFourHours()["time_from"]), int(
        Timestamp.twentyFourHours()["time_to"]))
    return lastDayTracksList


### Grabs played tracks from a year ago ###
def oneYearAgoTracks():
    oneYearAgoTracksList = getTracks(int(Timestamp.threeSixFive()["time_from"]), int(
        Timestamp.threeSixFive()["time_to"]))
    return oneYearAgoTracksList

def nowPlaying():
    now_playing = [lastfm_network.get_user(lastfm_username).get_now_playing()]
    return now_playing




### RESEARCH PARSER ###
#def mostLovedTracks():
    #topTracks = LASTFM.get_top_tracks(period="PERIOD_OVERALL", limit=50)
    #recentTracks = lastDayTracks()
    #overlaps = set(topTracks).intersection(recentTracks)
    #return overlaps






