from groupy.client import Client
from Token import groupyToken, groupy_id, bot_id
import LastFm
client = Client.from_token(groupyToken)
group = client.groups.get(groupy_id)


class Command:
    def __init__(self):
        self.commands = {
            "!stop": self.stop,
            "!help": self.help,
            "!musiclastyear": self.musicLastYear,
            "!musicrecents": self.musicRecents
        }

    def handle_command(self, command):
        response= ""
        if command in self.commands:
            response += str(self.commands[command]())
            print("handling command: " + command)
            client.bots.post(bot_id=bot_id, text=str(response))
            return response

    def stop(self):
        return "!stop"

    def help(self):
        response = "help:\r\n"

        for command in self.commands:
            response += command + "\r\n"

        return response

    def musicLastYear(self):
        response = "One Year Ago Tracks: \r\n"
        trackList = LastFm.oneYearAgoTracks()
        if not trackList:
            response+= "None"
        else:
            for item in trackList:
                try:
                    response += str(item.playback_date)[13:] + ": " + str(item.track.artist) + " - " + str(item.track.title) + "\r\n"
                except UnicodeEncodeError:
                    response += str(item.playback_date)[13:] + ": " + str(item.playback_date) + "Unreadable Track"
        return response


    def musicRecents(self):
        response = "Recently Played Tracks: \r\n"
        trackList = LastFm.pastThreeHoursTracks()
        if not trackList:
            response+= "None"
        counter = 1
        for item in trackList:
            try:
                response += str(item.playback_date)[13:] + ": " + str(item.track.artist) + " - " + str(item.track.title) + "\r\n"
                counter += 1
            except UnicodeEncodeError:
                response += str(item.playback_date)[13:] + ": " + str(item.playback_date) + "Unreadable Track"
                counter += 1
        return response





