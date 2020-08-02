from groupy.client import Client
from Token import groupyToken, groupy_id, bot_id
import time
from GroupMe.Command import Command
client = Client.from_token(groupyToken)
group = client.groups.get(groupy_id)

# New Bot Class
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
            nextMessageList = list(group.messages.list_since(message_id=self.lastMsgID))

            if nextMessageList:
                nextMessage =  nextMessageList[0]
                text = nextMessage.text
                response = self.command.handle_command(text)
                if response == "!stop":
                    break
                print(response)
                self.lastMsgID = nextMessage.id
            time.sleep(4)












