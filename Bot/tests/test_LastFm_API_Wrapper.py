from unittest import TestCase
from Token import lastfm_api_key, lastfm_api_secret, lastfm_username, lastfm_password_hash
from LastfmAPIWrapper.LastFmWrapper import LastfmWrapper
import pylast
from traceback import format_exc
from Bot.LastfmCommands import LastfmCommands


username = lastfm_username

lastfm = LastfmWrapper(
    api_key=lastfm_api_key,
    api_secret=lastfm_api_secret,
    username=lastfm_username,
    password_hash=lastfm_password_hash)


class TestLastfmWrapper(TestCase):
    def test_convert_utc_to_est(self):
        self.fail()


    def test_get_timestamps(self):
        """
        Case 1: Correct formatting of time
        """
        raised = False
        try:
            timestamps = lastfm.get_timestamps(
                time_from="01-26-2021-01-00",
                time_to="01-27-2021-00-00")

            print("time_from: " + str(timestamps["time_from"]) + "\r\n" +
                  "time_to: " + str(timestamps["time_to"]))
        except Exception as e:
            print(e)
            raised = True
        self.assertFalse(raised)

        """
        Case 2: char instead of int for day
        """
        raised = False
        try:
            timestamps = lastfm.get_timestamps(
                time_from="01-ab-2021-01-00",
                time_to="01-cd-2021-00-00")

        except ValueError:
            raised = True
        self.assertTrue(raised)

        """
        Case 3: month out of range
        """
        raised = False
        try:
            timestamps = lastfm.get_timestamps(
                time_from="15-01-2021-01-00",
                time_to="15-02-2021-00-00")

        except ValueError:
            raised = True
        self.assertTrue(raised)

        """
        Case 3: day out of range
        """
        raised = False
        try:
            timestamps = lastfm.get_timestamps(
                time_from="01-45-2021-01-00",
                time_to="01-21-2021-00-00")

        except ValueError:
            raised = True
        self.assertTrue(raised)

        """
        Case 4: February 30th
        """
        raised = False
        try:
            timestamps = lastfm.get_timestamps(
                time_from="02-29-2019-01-00",
                time_to="02-30-2019-00-00")

        except ValueError:
            raised = True
        self.assertTrue(raised)


    def test_get_tracks(self):
        raised = False
        try:
            timestamps = lastfm.get_timestamps(
                time_from="01-26-2021-01-00",
                time_to="01-27-2021-00-00")

            track_list = lastfm.get_tracks(
                time_from=timestamps["time_from"],
                time_to=timestamps["time_to"],
                lastfm_username=lastfm_username)

        except Exception as e:
            print(e)
            raised = True
        self.assertFalse(raised)
        self.assertIsInstance(track_list[0], pylast.PlayedTrack)
        self.assertTrue(len(track_list) != 0)






