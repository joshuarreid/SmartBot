from datetime import datetime
from Token import bot_id
import time
from Bot.Command_Handler import Command_Handler, client, group


class Bot:
    def __init__(self, name, id):
        print(str(datetime.now().hour) + ":" + str(datetime.now().minute) + "  " +  "Bot is initiated!")
        #client.bots.post(bot_id=bot_id, text="Bot is initiated!")
        self.bot_name = name
        self.bot_id = id
        self.recentMessageID = (list(group.messages.list(limit=1)))[0].id
        self.command_handler = Command_Handler()
        self.listen()


    ### Listens for commands in the chat ###
    def listen(self):
        while True:
            fetchedMessageList = []
            fetchedMessageList = list(group.messages.list_after(message_id=self.recentMessageID))
            if len(fetchedMessageList) != 0:
                mostRecentMessage = fetchedMessageList[0]
                botResponse = self.command_handler.execute(mostRecentMessage.text, mostRecentMessage.name, mostRecentMessage.user_id)
                self.recentMessageID = mostRecentMessage.id

                ### Stop command ###
                #if botResponse == "!stop":
                    #if recentMessageUser == "Joshua Reid": ### Only owner can !stop the bot ###
                        #client.bots.post(bot_id=bot_id, text="Going Offline!")
                        #print("Bot is offline.")


                    #else:
                       # client.bots.post(bot_id=bot_id, text="Access denied: only Joshua Reid can use this command")
                if botResponse == "!reboot":
                    client.bots.post(bot_id=bot_id, text="Rebooting!")
                    print("Bot is rebooting")
                    break




            time.sleep(2)
