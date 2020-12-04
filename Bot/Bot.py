import time
from datetime import datetime
from Bot.Command_Handler import Command_Handler, client, group
from Token import bot_id


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
        self.command_handler = Command_Handler()
        self.listen()



    def listen(self):
        """
        Listens for commands in the chat by retrieving the message after the most previous one. After
        it refreshes (2 second intervals), if a new message is sent in the groupchat it checks if
        there is a !{command} present. If a command is present inside the message, it calls the
        command handler to execute the command.
        """
        while True:
            fetchedMessageList = []
            fetchedMessageList = list(group.messages.list_after(message_id=self.recentMessageID))
            if len(fetchedMessageList) != 0:
                mostRecentMessage = fetchedMessageList[0]
                botResponse = self.command_handler.execute(mostRecentMessage.text, mostRecentMessage.name,
                                                           mostRecentMessage.user_id, mostRecentMessage.attachments)
                self.recentMessageID = mostRecentMessage.id

                if botResponse == "!reboot":
                    client.bots.post(bot_id=bot_id, text="Rebooting!")
                    print("Bot is rebooting")
                    break

            time.sleep(2)
