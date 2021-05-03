from Token import lastfm_api_key, lastfm_api_secret, lastfm_username, lastfm_password_hash
from LastfmAPIWrapper.LastFmWrapper import LastfmWrapper as Lastfm
from Database.Database import Database
import datetime as DT





class LastfmCommands:
    """The Lastfm Command Class

    The Lastfm_Command class contains all the commands their methods for the
    LastFm API Wrapper. It also creates its own dataframe from the Lastfm
    database table.

    """



    def __init__(self):
        self.commands = {
            "!playbacks": self.list_playbacks,
            "!toptracks": self.list_top_tracks,
            "!topartists": self.list_top_artists, #TODO img_top_artists
            "!playcount": self.get_playback_count,
            "!rewind": self.rewind
        }

        self.commandDescriptions = {
            "!playbacks": "1year, recents, now",
            "!toptracks": "overall, week, month, year",
            "!topartists": "overall, week, month, year",
            "!playcount": "Total plays",
            "!rewind": "[x]year"
        }

        self.database = Database('LastFm')
        self.lastfm = Lastfm(lastfm_api_key, lastfm_api_secret, lastfm_username, lastfm_password_hash)



    def get_username(self, groupme_id):
        """
        Fetches and returns a groupme user's registered lastfm username from the lastfm
        dataframe using their groupme id as the key.

        :param groupme_id: {Integer} the user's groupme id
        :return lastfm_username: {String} the users lastfm username
        """
        lastfm_username = self.database.df.loc[self.database.df['GroupMeID'] == str(groupme_id)]['username'].tolist()[0]
        return lastfm_username



    def format_by_time(self, listOfTracks):
        """
        Takes in a list of pylast.Track objects and returns a string that lists
        the tracks with their given playback time.

        :param listOfTracks: {list} track objects
        :return botResponse: {String} a list of tracks with given time
        """
        botResponse = ""
        if not listOfTracks:
            botResponse = "None"
        else:
            for track in listOfTracks:
                if len(botResponse) < 900:  ### Checking if response is under the 1000 character limit ###
                    try:
                        botResponse += self.lastfm.convert_utc_to_est(track.playback_date) + "  " + str( #TODO use datetime.deltatime()
                            track.track.artist) + " - " + str(track.track.title) + "\r\n"
                    except UnicodeEncodeError:  ### If the track or artist title has non ascii characters ###
                        botResponse += self.lastfm.convert_utc_to_est(track.playback_date) + "  " + "Unreadable Track"
            return botResponse



    def format_by_rank(self, listOfTracks):
        """
        Takes in a list of pylast.Track objects and returns a string that lists
        the tracks with their given rank.

        :param listOfTracks: {list} track objects
        :return botResponse: {String} a list of tracks with given rank
        """
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



    def list_playbacks(self, groupme_id, period="recents"):
        """
        lists a users playbacks from one year ago, lists a users playbacks from past 24 hours

        :param groupme_id: {Integer} the user's groupme id
        :return: {String} A formatted list of tracks
        """

        if period == "recents":
            lastfm_username = self.get_username(groupme_id)
            botResponse = "Recently Played Tracks: @" + str(lastfm_username).title() + "\r\n"
            time_from = self.lastfm.get_unix_timestamp(hours_ago=24)
            time_to = self.lastfm.get_unix_timestamp()
            recently_played_list = self.lastfm.get_tracks(
                lastfm_username=lastfm_username,
                time_from=time_from,
                time_to=time_to,
                limit=200)
            if recently_played_list == None:
                botResponse += "None"
            else:
                botResponse += self.format_by_time(recently_played_list)


        elif period == "now":  # Currently Playing
            lastfm_username = self.get_username(groupme_id)
            botResponse = "Currently Playing: @" + str(lastfm_username).title() + "\r\n"
            currentlyPlayingTrackList = self.lastfm.get_now_playing(lastfm_username)
            if None in currentlyPlayingTrackList:
                botResponse += "None"
            else:
                for track in currentlyPlayingTrackList:
                    try:
                        botResponse += str(track.artist) + " - " + str(track.title)
                    except UnicodeEncodeError:
                        botResponse += "Unreadable Track"
        return botResponse




    def list_top_tracks(self, groupme_id, period="overall"):
        """
        lists a users top tracks from a given period

        :param groupme_id: {Integer} the user's groupme id
        :param period: {String} time period to fetch top tracks from
        :return: {String} A formatted list of top tracks
        """
        periodOptions = {
            "overall": "overall",
            "week": "7day",
            "month": "1month",
            "year": "12month"
        }

        lastfm_username = self.get_username(groupme_id)
        botResponse = "Top Tracks " + period.title() + ": @" + str(lastfm_username).title() + "\r\n"
        if period in periodOptions:
            topTrackList = self.lastfm.get_top_tracks_legacy(lastfm_username, periodOptions[period])
            botResponse += self.format_by_rank(topTrackList)
        else:
            botResponse = "Try: \r\n"
            for item in periodOptions:
                botResponse += "!toptracks {" + item + "}\r\n"
        return botResponse




    def list_top_artists(self, groupme_id, period="overall"):
        """
        lists a users top tracks from a given period

        :param groupme_id: {Integer} the user's groupme id
        :param period: {String} time period to fetch top artists from
        :return: {String} A formatted list of top artists
        """
        periodOptions = {
            "overall": "overall",
            "week": "7day",
            "month": "1month",
            "year": "12month"
        }

        lastfm_username = self.get_username(groupme_id)
        botResponse = "Top Artists " + period.title() + ": @" + str(lastfm_username).title() + "\r\n"
        if period in periodOptions:
            listOfArtists = self.lastfm.get_top_artists_legacy(lastfm_username, periodOptions[period])
            if not listOfArtists:
                botResponse += "None"
            else:
                rank = 1
                for item in listOfArtists: #TODO implement format_by_rank
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



    def img_top_artists(self, groupme_id, period="overall"):
        """
        lists a users top tracks from a given period and returns an image

        :param groupme_id: {Integer} the user's groupme id
        :param period: {String} time period to fetch top artists from
        :return: {Image} a png containing graph of top artists
        """
        return "Shits in the works"
        periodOptions = {
            "overall": "overall",
            "week": "7day",
            "month": "1month",
            "year": "12month"
        }
        lastfm_username = self.get_username(groupme_id)
        if period in periodOptions:
            image = self.lastfm.graph_top_artists(lastfm_username, periodOptions[period])
            return image
        else:
            botResponse = "Try: \r\n"
            for item in periodOptions:
                botResponse += "!topartists {" + item + "}\r\n"
            return botResponse



    def get_playback_count(self, groupme_id):
        """
        fetches and returns a users total number of playbacks

        :param groupme_id: {Integer} the user's groupme id
        :return: {String} the user's total number of playbacks
        """
        lastfm_username = self.get_username(groupme_id)
        playbackCount = "Total Scrobbles: @" + str(lastfm_username).title() + "\r\n" + str(
            self.lastfm.get_user_playcount(lastfm_username))
        return playbackCount



    def rewind(self, groupme_id, period="1year"):
        """
        This method should return a user's one year ago today statistics including:
            - top artists the week of one year ago
            - top tracks the week of one year ago
            - recent tracks from past 6 hours one year ago

        :param groupme_id: {Integer} the user's groupme id
        :return: {String} A summary of x years ago
        """


        """
        First calculating time stamps for inputted number of years ago
        """
        lastfm_username = self.get_username(groupme_id)
        time_to_days_ago = int(period[0]) * 365
        time_from_days_ago = time_to_days_ago + 7
        time_to = self.lastfm.get_unix_timestamp(days_ago=time_to_days_ago)
        time_from = self.lastfm.get_unix_timestamp(days_ago=time_from_days_ago)
        botResponse = "In " + str(DT.datetime.now().year - int(period[0])) + ": @" + str(lastfm_username).title() + "\r\n"

        """
        Fetching the top 3 tracks 
        """
        top_tracks_list = self.lastfm.get_top_tracks(
            lastfm_username=lastfm_username,
            time_to=time_to,
            time_from=time_from,
            limit=3
        )
        if top_tracks_list == None:
            botResponse += "No Data Found :("
            return botResponse
        botResponse += "Your Top Tracks This Week: \n"

        rank = 1
        for track in top_tracks_list:
            botResponse += str(rank) + ". " + track[0] + " (" + str(track[1]) + " Plays)" + "\r\n"
            rank += 1


        """
        Fetching the top 3 artists
        """
        botResponse += "\r\nYour Top Artists This Week: \n"
        top_artists_list = self.lastfm.get_top_artists(
            lastfm_username=lastfm_username,
            time_to=time_to,
            time_from=time_from,
            limit=3
        )
        rank = 1
        for artist in top_artists_list:
            botResponse += str(rank) + ". " + artist[0] + " (" + str(artist[1]) + " Plays)" + "\r\n"
            rank += 1


        """
        Fetching what tracks user was currently listening to at the current time.
        time_from is recalculated to be 5 hours before the current time
        """
        botResponse += "\r\nYou Were Listening To: \n"
        time_from = self.lastfm.get_unix_timestamp(days_ago=time_to_days_ago, hours_ago=5)
        currently_playing_tracks = self.lastfm.get_tracks(
            lastfm_username=lastfm_username,
            time_to=time_to,
            time_from=time_from,
            limit=3
        )
        if currently_playing_tracks == None:
            botResponse += "None"
        else:
            botResponse += self.format_by_time(currently_playing_tracks)

        return botResponse


