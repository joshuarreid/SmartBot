import Database
from Lastfm import Lastfm


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





    ### Gives a listed response in format "hr:minAM/PM  artist - title" ###
    def timeFormatedTrackList(self, listOfTracks):
        botResponse = ""
        if not listOfTracks:
            botResponse = "None"
        else:
            for track in listOfTracks:
                if len(botResponse) < 900:  ### Checking if response is under the 1000 character limit ###
                    try:
                        botResponse += Lastfm.playbackTimeUtcToEst(track.playback_date) + "  " + str(
                            track.track.artist) + " - " + str(track.track.title) + "\r\n"
                    except UnicodeEncodeError:  ### If the track or artist title has non ascii characters ###
                        botResponse += Lastfm.playbackTimeUtcToEst(track.playback_date) + "  " + "Unreadable Track"
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

    ### Command stops the bot ###
    # def stop(self, user):
    # stop = "!stop"
    # return stop


        ### TODO command to add new users to database ###
        # def addNewUser(self, name, lastFmUsername):

        ### Command lists music that was listened to one year ago ###
    def playbacksOneYearAgo(self, user):
        response = "One Year Ago Tracks: @" + str(user) + "\r\n"
        trackList = Lastfm.oneYearAgoTracks(Database.getLastFmUsername(user))
        response += str(self.timeFormatedTrackList(trackList))
        return response

    ### Command lists music from the past 24 hours ###
    def recentPlaybacks(self, user):
        response = "Recently Played Tracks: @" + str(user) + "\r\n"
        trackList = Lastfm.playbackPastDay(Database.getLastFmUsername(user))
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
        botResponse = "Top Tracks: @" + str(user) + "\r\n"
        if period in periodOptions:
            topTrackList = Lastfm.getTopTracks(Database.getLastFmUsername(user), periodOptions[period])
            botResponse += self.rankFormatedTrackList(topTrackList)
        else:
            botResponse = "Try: \r\n"
            for item in periodOptions:
                botResponse += "!toptracks {" + item + "}\r\n"
        return botResponse

    def listTopArtists(self, user, period="overall"):
        periodOptions = {
            "overall": "overall",
            "week": "7day",
            "month": "1month",
            "year": "12month"
        }
        botResponse = "Top Artists: @" + str(user) + "\r\n"
        if period in periodOptions:
            listOfArtists = Lastfm.getTopArtist(Database.getLastFmUsername(user), periodOptions[period])
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
        playBackCount = "Total Scrobbles: @" + str(user) + "\r\n" + str(
            Lastfm.playCount(Database.getLastFmUsername(user)))
        return playBackCount

    def currentlyPlaying(self, user):
        botResponse = "Currently Playing: @" + str(user) + "\r\n"
        currentlyPlayingTrackList = Lastfm.getNowPlaying(Database.getLastFmUsername(user))
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
        botResponse = "Comparing: " + str(user) + " & " + otherUser + "\r\n"

        similarArtistList = Lastfm.compareUsersTopArtists(Database.getLastFmUsername(user),
                                                          Database.getLastFmUsername(otherUser),
                                                          periodInput=periodOptions[period])
        similarTracksList = Lastfm.compareUsersTopTracks(Database.getLastFmUsername(user),
                                                         Database.getLastFmUsername(otherUser),
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