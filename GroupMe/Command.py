from datetime import datetime
from groupy.client import Client
from Token import groupyToken, groupy_id, bot_id
import LastFm
import Database
client = Client.from_token(groupyToken)
group = client.groups.get(groupy_id)



class Command:
    def __init__(self):
        self.commands = {
            "!stop": self.stop,
            "!commands": self.listCommands,
            "!musiclastyear": self.playbacksOneYearAgo,
            "!musicrecents": self.recentPlaybacks,
            "!toptracks": self.listTopTracks,
            "!topartists": self.listTopArtists,
            "!playcount": self.playbackCount,
            "!nowplaying": self.currentlyPlaying

        }

        self.commandDescriptions = {
            "!stop": "terminates bot",
            "!commands": "Lists all commands",
            "!musiclastyear": "Tracks 1 year ago",
            "!musicrecents": "Recent Tracks (24hrs)",
            "!toptracks": "Top Tracks",
            "!topartists": "Top Artists",
            "!playcount": "Total plays",
            "!nowplaying": "Currently playing song"
        }


    ### Function handles each command and creates the correct response ###
    def handle_command(self, command, user):
        botResponse = ""
        if command == "!stop":
            return "!stop"
        splitCommandList = command.split()
        if splitCommandList[0] in self.commands:
            if len(splitCommandList) == 1:
                botResponse += str(self.commands[splitCommandList[0]](user))
                print(str(datetime.now().hour) + ":" + str(datetime.now().minute) + " " + user + ": " + splitCommandList[0])
                client.bots.post(bot_id=bot_id, text=str(botResponse))
                return botResponse

            elif len(splitCommandList) == 2:
                botResponse += str(self.commands[splitCommandList[0]](user, splitCommandList[1]))
                print(str(datetime.now().hour) + ":" + str(datetime.now().minute) + " " + user + ": " + splitCommandList[0] + " " + splitCommandList[1])
                client.bots.post(bot_id=bot_id, text=str(botResponse))
                return botResponse




    ### Gives a listed response in format "hr:minAM/PM  artist - title" ###
    def timeFormatedTrackList(self, listOfTracks):
        botResponse = ""
        if not listOfTracks:
            botResponse = "None"
        else:
            for track in listOfTracks:
                if len(botResponse) < 900: ### Checking if response is under the 1000 character limit ###
                    try:
                        botResponse += LastFm.playbackTimeUtcToEst(track.playback_date) + "  " + str(track.track.artist) + " - " + str(track.track.title) + "\r\n"
                    except UnicodeEncodeError: ### If the track or artist title has non ascii characters ###
                        botResponse += LastFm.playbackTimeUtcToEst(track.playback_date) + "  " + "Unreadable Track"
            return botResponse


    ### Gives a listed response in format "rank. artist - title"" ###
    def rankFormatedTrackList(self, listOfTracks):
        botResponse = ""
        if not listOfTracks:
            botResponse = "None"
        else:
            rank = 1
            for item in listOfTracks:
                if len(botResponse) < 900: ### Checking if response is under the 1000 character limit ###
                    try:
                            botResponse += str(rank) + ". " + str(item.item.artist) + " - " + str(item.item.title) + "\r\n"
                            rank+=1
                    except UnicodeEncodeError:  ### If the track or artist title has non ascii characters ###
                            botResponse += str(rank) + ". " + "Unreadable Track"
                            rank+=1

            return botResponse





    ### Command stops the bot ###
    def stop(self, user):
        stop = "!stop"
        return stop


    ### Command lists all of the available commands ###
    def listCommands(self, user):
        botResponse = "Commands:\r\n"

        for command in self.commandDescriptions:
            botResponse += "-" + command + ": " + self.commandDescriptions[command] + "\r\n"

        return botResponse


    ### Command lists music that was listened to one year ago ###
    def playbacksOneYearAgo(self, user):
        response = "One Year Ago Tracks: @" + str(user) + "\r\n"
        trackList = LastFm.oneYearAgoTracks(Database.fetchLastFmUsername(user))
        response += str(self.timeFormatedTrackList(trackList))
        return response


    ### Command lists music from the past 24 hours ###
    def recentPlaybacks(self, user):
        response = "Recently Played Tracks: @" + str(user) + "\r\n"
        trackList = LastFm.playbackPastDay(Database.fetchLastFmUsername(user))
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
            topTrackList = LastFm.getTopTracks(Database.fetchLastFmUsername(user), periodOptions[period])
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
            listOfArtists = LastFm.getTopArtist(Database.fetchLastFmUsername(user), periodOptions[period])
            if not listOfArtists:
                botResponse += "None"
            else:
                rank =1
                for item in listOfArtists:
                    if len(botResponse) < 900:  ### Checking if response is under the 1000 character limit ###
                        try:
                            botResponse += str(rank) + ". " + str(item.item) + " (" + str(item.weight) + " plays)\r\n"
                            rank+=1
                        except UnicodeEncodeError:  ### If the track or artist title has non ascii characters ###
                            botResponse += str(rank) + ". Unreadable Artist (" + str(item.weight) + ")\r\n"
                            rank+=1
                return botResponse
        else:
            botResponse = "Try: \r\n"
            for item in periodOptions:
                botResponse += "!topartists {" + item + "}\r\n"
        return botResponse



    def playbackCount(self, user):
        playBackCount = "Total Scrobbles: @" + str(user) + "\r\n" + str(LastFm.playCount(Database.fetchLastFmUsername(user)))
        return playBackCount


    def currentlyPlaying(self, user):
        botResponse = "Currently Playing: @" + str(user) + "\r\n"
        currentlyPlayingTrackList = LastFm.getNowPlaying(Database.fetchLastFmUsername(user))
        if None in currentlyPlayingTrackList:
            botResponse += "None"
        else:
            for track in currentlyPlayingTrackList:
                try:
                    botResponse += str(track.artist) + " - " + str(track.title)
                except UnicodeEncodeError:
                    botResponse += "Unreadable Track"
        return botResponse



    ### TODO ranking scrobbles of users ###
    #def rankScrobbles(self):








