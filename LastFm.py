import pylast
from Token import lastfm_network
import Timestamp


### Converts playback time from UTC time zone to EST time zone ####
def playbackTimeUtcToEst(utcTime):
    hourMin = str(utcTime)[13:]
    return Timestamp.utcToEst(hourMin)

### Grabs played tracks within a time interval ###
def getTracksTimeInterval(timeFrom, timeTo, user):
    trackList = lastfm_network.get_user(user).get_recent_tracks(cacheable=False, limit=None, time_from=timeFrom, time_to=timeTo)
    return trackList

### Grabs played tracks from last 24 hours ###
def playbackPastDay(user):
    pastDayTrackList = getTracksTimeInterval(int(Timestamp.twentyFourHours()["time_from"]), int(
        Timestamp.twentyFourHours()["time_to"]), user)
    return pastDayTrackList

def playbackPastThreeHours(user):
    pastThreeHoursTrackList = getTracksTimeInterval(int(Timestamp.pastThreeHours()["time_from"]), int(
        Timestamp.pastThreeHours()["time_to"]), user)
    return pastThreeHoursTrackList

### Grabs played tracks from a year ago ###
def oneYearAgoTracks(user):
    oneYearAgoTracksList = getTracksTimeInterval(int(Timestamp.threeSixFive()["time_from"]), int(
        Timestamp.threeSixFive()["time_to"]), user)
    return oneYearAgoTracksList

def getNowPlaying(user):
    now_playing = [lastfm_network.get_user(user).get_now_playing()]
    return now_playing

def getTopTracks(user, periodInput):
        topTracksList = lastfm_network.get_user(user).get_top_tracks(period = periodInput, limit=25)
        return topTracksList


def getTopArtist(user, periodInput):
    topTracksList = lastfm_network.get_user(user).get_top_artists(period=periodInput, limit=25)
    return topTracksList


def playCount(user):
    playCount = lastfm_network.get_user(user).get_playcount()
    return '{:,}'.format(playCount) ### formats number with comma








