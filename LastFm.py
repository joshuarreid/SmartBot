import pylast
from Token import lastfm_network, lastfm_username
import Timestamp

###Changing lastfm_username here allows to lookup any account###
#LASTFM = lastfm_network.get_user(lastfm_username)


### Corrects playback time ####
def playbackTime(time):
    hourMin = str(time)[13:]
    return Timestamp.utcToEst(hourMin)

### Grabs played tracks within a time interval ###
def getTracks(time_from, time_to, user):
    tracks = lastfm_network.get_user(user).get_recent_tracks(cacheable=False, limit=None, time_from=time_from, time_to=time_to)
    return tracks

### Grabs played tracks from last 24 hours ###
def lastDayTracks(user):
    lastDayTracksList = getTracks(int(Timestamp.twentyFourHours()["time_from"]), int(
        Timestamp.twentyFourHours()["time_to"]), user)
    return lastDayTracksList

def pastThreeHoursTracks(user):
    pastThreeHoursList = getTracks(int(Timestamp.pastThreeHours()["time_from"]), int(
        Timestamp.pastThreeHours()["time_to"]), user)
    return pastThreeHoursList

### Grabs played tracks from a year ago ###
def oneYearAgoTracks(user):
    oneYearAgoTracksList = getTracks(int(Timestamp.threeSixFive()["time_from"]), int(
        Timestamp.threeSixFive()["time_to"]), user)
    return oneYearAgoTracksList

def nowPlaying(user):
    now_playing = [lastfm_network.get_user(user).get_now_playing()]
    return now_playing

def topTracks(user, periodInput):
        topTracksList = lastfm_network.get_user(user).get_top_tracks(period = periodInput, limit=25)
        return topTracksList


def topArtist(user, periodInput):
    topTracksList = lastfm_network.get_user(user).get_top_artists(period=periodInput, limit=25)
    return topTracksList



### TODO Modify to add comma to the number ###
def playCount(user):
    playCount = lastfm_network.get_user(user).get_playcount()
    return '{:,}'.format(playCount) ### formats number with comma








