from Token import lastfm_network
from LastfmAPIWrapper import Timestamp


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

def getTopTracksPeriod(user, time_from, time_to):
    topTracksList = lastfm_network.get_user(user).get_recent_tracks(time_from, time_to)



def getTopArtist(user, periodInput):
    topTracksList = lastfm_network.get_user(user).get_top_artists(period=periodInput, limit=25)
    return topTracksList


def playCount(user):
    playCount = lastfm_network.get_user(user).get_playcount()
    return '{:,}'.format(playCount) ### formats number with comma

def compareUsersTopTracks(user, otherUser, periodInput):
    topTracksListUser = lastfm_network.get_user(user).get_top_tracks(period = periodInput, limit = 150)
    topTracksListOtherUser = lastfm_network.get_user(otherUser).get_top_tracks(period=periodInput, limit=150)

    formattedTrackListUser = []
    for track in topTracksListUser:
        formattedTrackListUser.append(track.item.title)

    formattedTrackListOtherUser = []
    for track in topTracksListOtherUser:
        formattedTrackListOtherUser.append(track.item.title)

    commonTopTracksList = list(set.intersection(set(formattedTrackListUser), set(formattedTrackListOtherUser)))
    return commonTopTracksList


def compareUsersTopArtists(user, otherUser, periodInput):
    topArtistsListUser = lastfm_network.get_user(user).get_top_artists(period=periodInput, limit = 100)
    topArtistsListOtherUser = lastfm_network.get_user(otherUser).get_top_artists(period=periodInput, limit= 100)

    formattedArtistListUser = []
    for artist in topArtistsListUser:
        formattedArtistListUser.append(artist.item)

    formattedArtistListOtherUser = []
    for artist in topArtistsListOtherUser:
        formattedArtistListOtherUser.append(artist.item)

    commonTopArtistsList = list(set.intersection(set(formattedArtistListUser), set(formattedArtistListOtherUser)))
    return commonTopArtistsList










