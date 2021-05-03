import time
from datetime import datetime
from Token import groupyToken, groupy_id
from groupy.client import Client
from Bot.GroupmeCommandHandler import GroupmeCommandHandler

client = Client.from_token(groupyToken)
group = client.groups.get(groupy_id)


class Bot:
    """The Bot Class

    The bot class is what the main program calls. It listens to the messages
    in the groupchat waiting for a command to be called.


    """
    def __init__(self, name, id):
        print(str(datetime.now().hour) + ":" + str(datetime.now().minute) + "  " + "Bot is initiated!")
        self.bot_name = name
        self.bot_id = id
        self.recentMessageID = (list(group.messages.list(limit=1)))[0].id
        self.command_handler = GroupmeCommandHandler()
        self.run()



    def run(self):
        """
        Listens for commands in the chat by retrieving the message after the most previous one. After
        it refreshes (2 second intervals), if a new message is sent in the groupchat it checks if
        there is a !{command} present. If a command is present inside the message, it calls the
        command handler to execute the command.
        """
        while True:
            """
            The bot listening for new messages.
            """
            fetchedMessageList = []
            fetchedMessageList = list(group.messages.list_after(message_id=self.recentMessageID))
            if len(fetchedMessageList) != 0:
                mostRecentMessage = fetchedMessageList[0]
                self.command_handler.execute(mostRecentMessage.text, mostRecentMessage.name, mostRecentMessage.user_id, mostRecentMessage.attachments)
                self.recentMessageID = mostRecentMessage.id

            self.command_handler.run_scheduled_tasks()
            time.sleep(2)
