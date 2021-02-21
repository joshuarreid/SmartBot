from Bot.Bot import Bot
from Bot.LastfmCommands import LastfmCommands
import unittest

lastFm = LastfmCommands()

class TestLastfm(unittest.TestCase):
    def test_playbacks_recents(self):
        result = lastFm.list_playbacks(groupme_id=22886889, period="recents")
        self.assertEqual(type(result), str)




bot = Bot("SmartBot-Beta" , "5c6adff9f6cc8781e7eb0ab24c")




