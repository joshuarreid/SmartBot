from groupy.client import Client
from Token import groupyToken, groupy_id, bot_id
import time
from GroupMe.Command import Command
client = Client.from_token(groupyToken)
group = client.groups.get(groupy_id)


class Bot:
    def __init__(self, name, id):
        print("Bot is initiated!")
        self.bot_name = name
        self.bot_id = id
        self.lastMsgID = (list(group.messages.list(limit=1)))[0].id
        self.command = Command()
        self.listen()

    def listen(self):

        while True:
            nextMessageList = []
            nextMessageList = list(group.messages.list_after(message_id=self.lastMsgID))
            if len(nextMessageList) != 0:
                nextMessage = nextMessageList[0]
                text = nextMessage.text
                response = self.command.handle_command(text)
                self.lastMsgID = nextMessage.id
                if response == "!stop":
                    break



            time.sleep(4)












