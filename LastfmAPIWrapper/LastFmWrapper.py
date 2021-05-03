import datetime as DT
from time import mktime
from Statify.Statify import Statify
import pylast


class LastfmWrapper:
    """
    The LastFm Wrapper Class.

    This class provides useful methods for interacting with LastFm's API. It allows for
    fetching user information. It also provides datetime methods for fetching timestamps.

    """
    def __init__(self, api_key, api_secret, username, password_hash):
        self.lastfm_network = pylast.LastFMNetwork(
            api_key = api_key,
            api_secret = api_secret,
            username = username,
            password_hash= password_hash
        )
        self.statify = Statify()


    def get_unix_timestamp(self, days_ago=0, hours_ago=0, minutes_ago=0):
        """
        This method creates a timestamp from x days/hours/minutes ago.

        :param days_ago: {int} Number of days ago
        :param hours_ago: {int} Number of hours ago
        :param minutes_ago: {int} Number of minutes ago
        :return: a unix timestamp representing the inputted date
        """
        today = DT.datetime.today()
        timestamp = today - DT.timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
        unix = int(mktime(timestamp.timetuple()))
        return unix


    def convert_utc_to_est(self, utc_time): #list_playbacks utilizes method
        """
        This method converts track.playback_date from UTC to EST.

        :param utc_time: {String} UTC time in the format "dd mmm yyyy, hh:mm"
        :return estTime: {String} EST time in the format "hh:mm"
        """
        hour_min = utc_time[-5:]
        hour = int(hour_min[0:2])
        min = int(hour_min[3:])
        if (hour - 4) < 0:
            hour = 24 + (hour - 4)
        else:
            hour -= 4

        if min < 10:
            min = "0" + str(min)

        est_time = str(hour) + ":" + str(min)
        return est_time



    def get_tracks(self, time_from, time_to, lastfm_username, limit=100):
        """
        This method returns a tracklist from a given time interval.

        :param time_from: {int} Unix Timestamp of beginning time
        :param time_to: {int} Unix Timestamp of end time
        :param lastfm_username: {String} A lastfm username
        :param limit: {int} The max number of tracks fetched
        :return: List of Pylast.Track Objects
        """

        track_list = self.lastfm_network.get_user(lastfm_username).get_recent_tracks(
            limit=limit,
            time_from=time_from,
            time_to=time_to)
        if (len(track_list) == 0):
            return None
        else:
            return track_list



    def get_now_playing(self, lastfm_username):
        """
        This method returns a user's currently playing track.

        :param lastfm_username: {String} A lastfm username
        :return: A Pylast.Track Object
        """
        now_playing = [self.lastfm_network.get_user(lastfm_username).get_now_playing()]
        return now_playing

    def get_top_tracks_legacy(self, lastfm_username, period, limit=25):
        """
        This method returns a user's top tracks based on period options.

        :param lastfm_username: {String} A lastfm username
        :param period: {String} "overall","7day", "1month", "12month"
        :param limit: {int} The max number of tracks fetched
        :return: List of Pylast.Track Objects
        """
        top_tracks_list = self.lastfm_network.get_user(lastfm_username).get_top_tracks(
            period=period,
            limit=limit)
        return top_tracks_list


    def get_top_tracks(self, lastfm_username, time_from, time_to, limit=10):
        """
        This method returns a user's top tracks from one timestamp to another.

        :param lastfm_username: {String} A lastfm username
        :param time_from: {int} Unix Timestamp of beginning time
        :param time_to: {int} Unix Timestamp of end time
        :param limit: {int} The max number of tracks fetched
        :return: dict in format {track : playcount}
        """
        track_list = self.get_tracks(
            lastfm_username=lastfm_username,
            time_from=time_from,
            time_to=time_to,
            limit=999,
        )
        if (track_list == None):
            return None
        formated_track_list = []
        for track in track_list:
            formated_track_list.append(str(track.track.artist) + " - " + str(track.track.title))
        track_occurences = list(self.statify.get_occurences(formated_track_list).most_common(limit))
        return track_occurences

    def get_top_artists_legacy(self, lastfm_username, period, limit=25):
        """
        This method returns a user's top tracks.

        :param lastfm_username: {String} A lastfm username
        :param period: {String} "overall","7day", "1month", "12month"
        :param limit: {int} The max number of tracks fetched
        :return: List of Pylast.Artist Objects
        """
        top_artists_list = self.lastfm_network.get_user(lastfm_username).get_top_artists(
            period=period,
            limit=25)
        return top_artists_list




    def get_top_artists(self, lastfm_username, time_from, time_to, limit=10):
        """

        :param lastfm_username: {String} A lastfm username
        :param time_from: {int} Unix Timestamp of beginning time
        :param time_to: {int} Unix Timestamp of end time
        :param limit: {int} The max number of tracks fetched
        :return: dict in format {artist : playcount}
        """
        track_list = self.get_tracks(
            lastfm_username=lastfm_username,
            time_from=time_from,
            time_to=time_to,
            limit=999,
        )
        if (track_list == None):
            return None
        formated_track_list = []
        for track in track_list:
            formated_track_list.append(str(track.track.artist))
        artist_occurences = list(self.statify.get_occurences(formated_track_list).most_common(limit))
        return artist_occurences



    def get_user_playcount(self, lastfm_username):
        """
        This method returns the total number of plays a user has

        :param lastfm_username: {String} A lastfm username
        :return: {int} of a user's total playcount
        """
        play_count = self.lastfm_network.get_user(lastfm_username).get_playcount()
        return '{:,}'.format(play_count)






















