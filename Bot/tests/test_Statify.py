from unittest import TestCase
from Token import lastfm_api_key, lastfm_api_secret, lastfm_username, lastfm_password_hash
from LastfmAPIWrapper.LastFmWrapper import LastfmWrapper
from Statify.Statify import Statify

username = lastfm_username

lastfm = LastfmWrapper(
    api_key=lastfm_api_key,
    api_secret=lastfm_api_secret,
    username=lastfm_username,
    password_hash=lastfm_password_hash)

statify = Statify()

class TestStatify(TestCase):
    def test_get_occurences(self):
        timestamps = lastfm.get_timestamps(
            time_from="09-23-2018-01-00",
            time_to="09-30-2018-00-00")

        track_list = lastfm.get_tracks(
            time_from=timestamps["time_from"],
            time_to=timestamps["time_to"],
            lastfm_username=lastfm_username,
            limit=999)

        edit = []
        print(len(track_list))
        for track in track_list:
            edit.append(str(track.track.artist) + " - " + str(track.track.title))
        occurences = statify.get_occurences(edit)
        print(occurences)





    def test_graph_top_artists(self):
        self.fail()
