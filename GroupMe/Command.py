from datetime import datetime
from Timestamp import utcToEst
from groupy.client import Client
from Token import groupyToken, groupy_id, bot_id
import LastFm
from GroupMe import Users
client = Client.from_token(groupyToken)
group = client.groups.get(groupy_id)
Users = Users.Users


class Command:
    def __init__(self):
        self.commands = {
            "!stop": self.stop,
            "!commands": self.commandList,
            "!musiclastyear": self.musicLastYear,
            "!musicrecents": self.musicRecents,
            "!toptracks": self.TopTracks,
            "!playcount": self.playCount,
            "!nowplaying": self.nowPlaying

        }

        self.commandDescriptions = {
            "!stop": "terminates bot",
            "!commands": "Lists all commands",
            "!musiclastyear": "Tracks 1 year ago",
            "!musicrecents": "Recent Tracks (24hrs)",
            "!toptracks": "Overall Top Tracks",
            "!playcount": "Total plays",
            "!nowplaying": "Currently playing song"
        }


    ### Function handles each command and creates the correct response ###
    def handle_command(self, command, user):
        response= ""
        if command in self.commands:
            if command == "!stop":
                return "!stop"
            else:
                response += str(self.commands[command](user))
                print(str(datetime.now().hour) + ":" + str(datetime.now().minute) + " " + user + ": " + command)
                client.bots.post(bot_id=bot_id, text=str(response))
                return response


    ### Gives a listed response in format "hr:minAM/PM  artist - title" ###
    def timeTrackList(self, list):
        response = ""
        if not list:
            response = "None"
        else:
            for item in list:
                if len(response) < 900: ### Checking if response is under the 1000 character limit ###
                    try:
                        response += LastFm.playbackTime(item.playback_date) + "  " + str(item.track.artist) + " - " + str(item.track.title) + "\r\n"
                    except UnicodeEncodeError: ### If the track or artist title has non ascii characters ###
                        response += LastFm.playbackTime(item.playback_date) + "  " + "Unreadable Track"
            return response


    ### Gives a listed response in format "rank. artist - title"" ###
    def rankTrackList(self, list):
        response = ""
        if not list:
            response = "None"
        else:
            counter = 1
            for item in list:
                if len(response) < 900: ### Checking if response is under the 1000 character limit ###
                    try:
                            response += str(counter) + ". " + str(item.item.artist) + " - " + str(item.item.title) + "\r\n"
                            counter+=1
                    except UnicodeEncodeError:  ### If the track or artist title has non ascii characters ###
                            response += str(counter) + ". " + "Unreadable Track"
                            counter+=1

            return response





    ### Command stops the bot ###
    def stop(self, user):
        stop = "!stop"
        return stop


    ### Command lists all of the available commands ###
    def commandList(self, user):
        response = "Commands:\r\n"

        for command in self.commandDescriptions:
            response += "-" + command + ": " + self.commandDescriptions[command] + "\r\n"

        return response


    ### Command lists music that was listened to one year ago ###
    def musicLastYear(self, user):
        response = "One Year Ago Tracks: @" + str(user) + "\r\n"
        trackList = LastFm.oneYearAgoTracks(str(Users.usersLastFM[user]))
        response += str(self.timeTrackList(trackList))
        return response


    ### Command lists music from the past 24 hours ###
    def musicRecents(self, user):
        response = "Recently Played Tracks: @" + str(user) + "\r\n"
        trackList = LastFm.lastDayTracks(str(Users.usersLastFM[user]))
        response += str(self.timeTrackList(trackList))
        return response


    ### Command lists top tracks of all time ###
    ### TODO odify to allow user to select interval  ###
    def TopTracks(self, user):
        response = "Top Tracks: @" + str(user) + "\r\n"
        trackList = LastFm.topTracks(str(Users.usersLastFM[user]))
        response += self.rankTrackList(trackList)
        return response


    def playCount(self, user):
        response = "Total Scrobbles: @" + str(user) + "\r\n" + str(LastFm.playCount(str(Users.usersLastFM[user])))
        return response


    def nowPlaying(self, user):
        response = "Currently Playing: @" + str(user) + "\r\n"
        now_playing = LastFm.nowPlaying(str(Users.usersLastFM[user]))
        if None in now_playing:
            response += "None"
        else:
            for item in now_playing:
                try:
                    response += str(item.artist) + " - " + str(item.title)
                except UnicodeEncodeError:
                    response += "Unreadable Track"
        return response



    ### TODO ranking scrobbles of users ###
    #def rankScrobbles(self):








