import LastFm



### Fetching currently playing song and playback count
now_playing = LastFm.nowPlaying()
recentlyPlayedList = LastFm.lastDayTracks()
recentlyPlayedCount = 0
for item in recentlyPlayedList:
    recentlyPlayedCount += 1


### Printing total number of playbacks in the past 24 hours
print("TOTAL PLAYBACKS 24HRS: " + str(recentlyPlayedCount))


### Print the song that is currently playing ###
if None in now_playing:
   print("NOW PLAYING: None")
else:
    for item in now_playing:
        try:
            print("NOW PLAYING: " + str(item.artist) + " - " + str(item.title))
        except UnicodeEncodeError:
            print(str(item.playback_date) + "     Unreadable Track")


### Print recently played songs in a list format ###
print()
print("-----  RECENTLY PLAYED  -----")
for item in recentlyPlayedList:
    try:
        print(str(item.playback_date) + "     " + str(item.track.artist) + " - " + str(item.track.title))
    except UnicodeEncodeError:
        print(str(item.playback_date) + "     Unreadable Track")


### Printing One Year Ago Tracks
oneYearAgoList = LastFm.oneYearAgoTracks()
print()
print("-----  ONE YEAR AGO LISTENS   -----")
if not oneYearAgoList:
    print("None")
else:
    for item in oneYearAgoList:
        try:
            print(str(item.playback_date) + "     " + str(item.track.artist) + " - " + str(item.track.title))
        except UnicodeEncodeError:
            print(str(item.playback_date) + "     Unreadable Track")


