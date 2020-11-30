from Database.Database import Database
import LastFmWrapper.LastFmWrapper as pylast


class Lastfm:
    def __init__(self):
        self.commands = {
            "!musiclastyear": self.playbacksOneYearAgo,
            "!recentlyplayed": self.recentPlaybacks,
            "!toptracks": self.listTopTracks,
            "!topartists": self.listTopArtists,
            "!playcount": self.playbackCount,
            "!nowplaying": self.currentlyPlaying,
            "!compareme": self.compareMe,
            "!rank": self.rankPlays()

        }

        self.commandDescriptions = {
            "!musiclastyear": "Tracks 1 year ago",
            "!recentlyplayed": "Recent Tracks (24hrs)",
            "!toptracks": "Top Tracks",
            "!topartists": "Top Artists",
            "!playcount": "Total plays",
            "!nowplaying": "Currently playing song",
            "!compareme": "Compare to other user",
            "!rank": "Not Implimented"
        }

        self.database = Database('LastFm')


    def getUsername(self, user_id):
        return self.database.df.loc[self.database.df['GroupMeID'] == str(user_id)]['username'][0]

    ### Gives a listed response in format "hr:minAM/PM  artist - title" ###
    def timeFormatedTrackList(self, listOfTracks):
        botResponse = ""
        if not listOfTracks:
            botResponse = "None"
        else:
            for track in listOfTracks:
                if len(botResponse) < 900:  ### Checking if response is under the 1000 character limit ###
                    try:
                        botResponse += pylast.playbackTimeUtcToEst(track.playback_date) + "  " + str(
                            track.track.artist) + " - " + str(track.track.title) + "\r\n"
                    except UnicodeEncodeError:  ### If the track or artist title has non ascii characters ###
                        botResponse += pylast.playbackTimeUtcToEst(track.playback_date) + "  " + "Unreadable Track"
            return botResponse

    ### Gives a listed response in format "rank. artist - title"" ###
    def rankFormatedTrackList(self, listOfTracks):
        botResponse = ""
        if not listOfTracks:
            botResponse = "None"
        else:
            rank = 1
            for item in listOfTracks:
                if len(botResponse) < 900:  ### Checking if response is under the 1000 character limit ###
                    try:
                        botResponse += str(rank) + ". " + str(item.item.artist) + " - " + str(
                            item.item.title) + " (" + str(item.weight) + " plays)" + "\r\n"
                        rank += 1
                    except UnicodeEncodeError:  ### If the track or artist title has non ascii characters ###
                        botResponse += str(rank) + ". " + "Unreadable Track" " (" + str(
                            item.weight) + " plays)" + "\r\n"
                        rank += 1

            return botResponse

        ### Command lists music that was listened to one year ago ###
    def playbacksOneYearAgo(self, user):
        response = "One Year Ago Tracks: @" + str(self.getUsername(user)) + "\r\n"
        trackList = pylast.oneYearAgoTracks(self.getUsername(user))
        response += str(self.timeFormatedTrackList(trackList))
        return response

    ### Command lists music from the past 24 hours ###
    def recentPlaybacks(self, user):
        response = "Recently Played Tracks: @" + str(self.getUsername(user)) + "\r\n"
        trackList = pylast.playbackPastDay(self.getUsername(user))
        response += str(self.timeFormatedTrackList(trackList))
        return response

    ### Command lists top tracks ###
    def listTopTracks(self, user, period="overall"):
        periodOptions = {
            "overall": "overall",
            "week": "7day",
            "month": "1month",
            "year": "12month"
        }
        botResponse = "Top Tracks: @" + str(self.getUsername(user)) + "\r\n"
        if period in periodOptions:
            topTrackList = pylast.getTopTracks(self.getUsername(user), periodOptions[period])
            botResponse += self.rankFormatedTrackList(topTrackList)
        else:
            botResponse = "Try: \r\n"
            for item in periodOptions:
                botResponse += "!toptracks {" + item + "}\r\n"
        return botResponse

    ### TODO post picture
    def listTopArtists(self, user, period="overall"):
        periodOptions = {
            "overall": "overall",
            "week": "7day",
            "month": "1month",
            "year": "12month"
        }
        botResponse = "Top Artists: @" + str(self.getUsername(user)) + "\r\n"
        if period in periodOptions:
            listOfArtists = pylast.getTopArtist(self.getUsername(user), periodOptions[period])
            if not listOfArtists:
                botResponse += "None"
            else:
                rank = 1
                for item in listOfArtists:
                    if len(botResponse) < 900:  ### Checking if response is under the 1000 character limit ###
                        try:
                            botResponse += str(rank) + ". " + str(item.item) + " (" + str(
                                item.weight) + " plays)\r\n"
                            rank += 1
                        except UnicodeEncodeError:  ### If the track or artist title has non ascii characters ###
                            botResponse += str(rank) + ". Unreadable Artist (" + str(item.weight) + ")\r\n"
                            rank += 1
                return botResponse
        else:
            botResponse = "Try: \r\n"
            for item in periodOptions:
                botResponse += "!topartists {" + item + "}\r\n"
        return botResponse

    def playbackCount(self, user):
        playBackCount = "Total Scrobbles: @" + str(self.getUsername(user)) + "\r\n" + str(
            pylast.playCount(self.getUsername(user)))
        return playBackCount

    def currentlyPlaying(self, user):
        botResponse = "Currently Playing: @" + str(self.getUsername(user)) + "\r\n"
        currentlyPlayingTrackList = pylast.getNowPlaying(self.getUsername(user))
        if None in currentlyPlayingTrackList:
            botResponse += "None"
        else:
            for track in currentlyPlayingTrackList:
                try:
                    botResponse += str(track.artist) + " - " + str(track.title)
                except UnicodeEncodeError:
                    botResponse += "Unreadable Track"
        return botResponse

    ### input format !compareme @Other User
    def compareMe(self, user, otherUserFirstName, otherUserLastName, period="overall"):
        periodOptions = {
            "overall": "overall",
            "week": "7day",
            "month": "1month",
            "year": "12month"
        }
        if otherUserFirstName[0] == "@":
            otherUser = otherUserFirstName[1:] + " " + otherUserLastName
        else:
            otherUser = otherUserFirstName + " " + otherUserLastName
        botResponse = "Comparing: " + str(self.getUsername(user)) + " & " + str(self.getUsername(otherUser)) + "\r\n"

        similarArtistList = pylast.compareUsersTopArtists(self.getUsername(user),
                                                          self.getUsername(otherUser),
                                                          periodInput=periodOptions[period])
        similarTracksList = pylast.compareUsersTopTracks(self.getUsername(user),
                                                         self.getUsername(otherUser),
                                                         periodInput=periodOptions[period])
        if len(similarArtistList) > 5:
            similarArtistList = similarArtistList[0:10]
        if len(similarTracksList) > 5:
            similarTracksList = similarTracksList[0:10]

        botResponse += "\r\nSIMILAR ARTISTS: \r\n"
        for artist in similarArtistList:
            botResponse += str(artist) + "\r\n"

        botResponse += "\r\nSIMILAR TRACKS: \r\n"
        for track in similarTracksList:
            botResponse += str(track) + "\r\n"
        return botResponse

    ### TODO rank users scrobbles ###
    def rankPlays(self):
        return "Implement Me"
