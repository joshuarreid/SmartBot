from groupy.client import Client
from Token import groupyToken, groupy_id, bot_id

client = Client.from_token(groupyToken)
group = client.groups.get(groupy_id)


class Bot(object):
    def __init__(self):
        self.bot_name = "SmartBot"
        self.bot_id = bot_id


    def listen(self):
        __allMessages = list(group.messages.list().autopage())  # Fetching all messages
        mostRecentMessage = None
        if __allMessages:
            print("Successfully connected, listening for commands")
            while True:
                __recentMessage = list(group.messages.list_since(message_id=__allMessages[0].id))  ## Tracks most recent message
                if __recentMessage != mostRecentMessage:
                    return __recentMessage
                    sleep(3)







        if not __allMessages:
            exit("Error, Connection Failed")












