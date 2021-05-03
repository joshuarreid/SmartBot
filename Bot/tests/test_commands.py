from unittest import TestCase
from Bot.LastfmCommands import LastfmCommands
from Bot.GroupmeCommandHandler import GroupmeCommandHandler, client, bot_id
from groupy.api.attachments import Image, Mentions

lastfm_commands = LastfmCommands()
command_handler = GroupmeCommandHandler()
groupme_id = 22886889
groupme_id_other = 79480351


class TestCommand_Handler(TestCase):
    def test_run_scheduled_tasks(self):
        result = command_handler.run_scheduled_tasks()


    def test_get_member_ids(self):
        result = command_handler.get_member_ids()
        print(result)
        self.assertEqual(type(result), list)



    def test_execute(self):
        raised = False
        try:
            client.bots.post(text="----RUNNING TESTS----", bot_id=bot_id, )
            for command in command_handler.commands:
                if command != '!compareme':
                    print(command_handler.execute(command=command, message_user="Joshua Reid", groupme_id=groupme_id))
        except:
            raised = True
        self.assertFalse(raised)



    def test_list_commands(self):
        raised = False
        try:
            result = command_handler.list_commands(user="Joshua Reid")
            print(result)
        except:
            raised = True
        self.assertFalse(raised)


class TestLastfmCommands(TestCase):

    def test_get_username(self):
        raised = False
        try:
            result = lastfm_commands.get_username(groupme_id=groupme_id)
            print(result)
        except:
            raised = True
        self.assertFalse(raised)



    def test_list_playbacks(self):
        raised = False
        try:
            print(lastfm_commands.list_playbacks(groupme_id=groupme_id, period="recents"))  # !playbacks 1year
            print(lastfm_commands.list_playbacks(groupme_id=groupme_id, period="now"))  # !playbacks now
        except:
            raised = True
        self.assertFalse(raised)



    def test_list_top_tracks(self):
        raised = False
        try:
            print(lastfm_commands.list_top_tracks(groupme_id=groupme_id, period="week"))  # !toptracks week
            print(lastfm_commands.list_top_tracks(groupme_id=groupme_id, period="month"))  # !toptracks month
            print(lastfm_commands.list_top_tracks(groupme_id=groupme_id, period="year"))  # !toptracks year
            result = lastfm_commands.list_top_tracks(groupme_id=groupme_id)  # !toptracks
            print(result)
        except:
            raised = True
        self.assertFalse(raised)



    def test_list_top_artists(self):
        raised = False
        try:
            print(lastfm_commands.list_top_artists(groupme_id=groupme_id, period="week"))  # !topartists week
            print(lastfm_commands.list_top_artists(groupme_id=groupme_id, period="month"))  # !topartists month
            print(lastfm_commands.list_top_artists(groupme_id=groupme_id, period="year"))  # !topartists year
            result = lastfm_commands.list_top_artists(groupme_id=groupme_id, )  # !topartists
            print(result)
        except:
            raised = True
        self.assertFalse(raised)



    def test_img_top_artists(self):
        result = lastfm_commands.img_top_artists(groupme_id=groupme_id)
        self.fail()
        # self.assertEqual(type(result), Image)



    def test_get_playback_count(self):
        raised = False
        try:
            result = lastfm_commands.get_playback_count(groupme_id=groupme_id)
            print(result)
        except:
            raised = True
        self.assertFalse(raised)




    def test_rewind(self):
        raised = False
        try:
            result1 = lastfm_commands.rewind(groupme_id=groupme_id, period="1year")
            print(result1)
            result2 = lastfm_commands.rewind(groupme_id=groupme_id, period="2year")
            print(result2)
            result3 = lastfm_commands.rewind(groupme_id=groupme_id, period="3year")
            print(result3)
            result4 = lastfm_commands.rewind(groupme_id=groupme_id, period="4year")
            print(result4)
        except:
            raised = False
        self.assertFalse(raised)
