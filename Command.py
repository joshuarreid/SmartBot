from groupy.client import Client
from Token import groupyToken, groupy_id, bot_id
import LastFm
client = Client.from_token(groupyToken)
group = client.groups.get(groupy_id)


class Command:
    def __init__(self):
        self.users = {
            "Joshua Reid": "bumi_",
            "Carly Mclaughlin": "carly_mac1",
            "Jason Allen": "FGMatrix",
            "Grace Tang": "gracetangg"
        }

        self.commands = {
            "!stop": self.stop,
            "!help": self.help,
            "!musiclastyear": self.musicLastYear,
            "!musicrecents": self.musicRecents,
            "!mytoptracks": self.myTopTracks,

        }



    def handle_command(self, command, user):
        response= ""
        if command in self.commands:
            if command == "!stop":
                return "!stop"
            else:
                response += str(self.commands[command](user))
                print("handling command by " + user + ": " + command)
                client.bots.post(bot_id=bot_id, text=str(response))
                return response



    def stop(self, user):
        stop = "!stop"
        return stop



    def help(self, user):
        response = "help:\r\n"

        for command in self.commands:
            response += command + "\r\n"

        return response



    def musicLastYear(self, user):
        response = "One Year Ago Tracks: \r\n"
        trackList = LastFm.oneYearAgoTracks(str(self.users[user]))
        if not trackList:
            response+= "None"
        else:
            for item in trackList:
                try:
                    response += str(item.playback_date)[13:] + ": " + str(item.track.artist) + " - " + str(item.track.title) + "\r\n"
                except UnicodeEncodeError:
                    response += str(item.playback_date)[13:] + ": " + str(item.playback_date) + "Unreadable Track"
        return response



    def musicRecents(self, user):
        response = "Recently Played Tracks: \r\n"
        trackList = LastFm.pastThreeHoursTracks(str(self.users[user]))
        if not trackList:
            response+= "None"
        for item in trackList:
            try:
                response += str(item.playback_date)[13:] + ": " + str(item.track.artist) + " - " + str(item.track.title) + "\r\n"
            except UnicodeEncodeError:
                response += str(item.playback_date)[13:] + ": " + str(item.playback_date) + "Unreadable Track"
        return response


    def myTopTracks(self, user):
        response = "Top Tracks: \r\n"
        trackList = LastFm.topTracks(str(self.users[user]))
        if not trackList:
            response+= "None"
        else:
            counter = 1
            for item in trackList:
                try:
                    response += str(counter) + ". " + str(item.item.artist) + " - " + str(item.item.title) + "\r\n"
                    counter+=1
                except UnicodeEncodeError:
                    response += str(counter) + ". " + "Unreadable Track"
                    counter+=1
        return response






