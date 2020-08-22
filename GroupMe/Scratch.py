from groupy.client import Client
from Token import groupyToken, groupy_id, bot_id
import time
from GroupMe.Bot import Bot
from GroupMe.Command import Command


client = Client.from_token(groupyToken)
group = client.groups.get(groupy_id)





'''

class Command(object):
    def __init__(self):
        self.commands = {
            "!help": self.help,
            "!test": self.test
        }


    def handle_command(self, command):
        response = ""

        if command in self.commands:
            response += self.commands[command]()
        else:
            response += "Sorry I don't understand the command: " + command + ". " + self.help()

        return response

    def help(self):
        response = "Currently I support the following commands: "
        for command in self.commands:
            response += command
        return response

    def test(self):
        return "This is a test!"


class Event:
    def __init__(self, bot):
        self.bot = bot
        self.command = Command()

    def wait_for_event(self):
        __allMessages = list(group.messages.list().autopage())  # Fetching all messages
        mostRecentMessage = None
        event = False
        if __allMessages:
            while True:
                __recentMessage = list(group.messages.list_since(message_id=__allMessages[0].id))  ## Tracks most recent message
                if __recentMessage != mostRecentMessage:
                    event = True
                    mostRecentMessage = __recentMessage
                    return mostRecentMessage

        if not __allMessages:
            exit("Error, Connection Failed")


class Bot(object):
    def __init__(self):
        self.bot_name = "SmartBot"
        self.bot_id = bot_id

    def listen(self):
        state = True
        while state:
            if not self.event.wait_for_event().event:
                time.sleep(3)
            else:
                Command.handle_command(self.event.wait_for_event().mostRecentMessage)







def listen():
    listen = True
    __allMessages = list(group.messages.list().autopage())  # Fetching all messages
    mostRecentMessage = None
    if __allMessages:
        print("Successfully connected, listening for commands")
        while listen:
            __recentMessage = list(group.messages.list_since(message_id=__allMessages[0].id))  ## Tracks most recent message

            if __recentMessage != mostRecentMessage:
                mostRecentMessage = __recentMessage

                for item in mostRecentMessage:
                    print(item)
                    time.sleep(3)

            else:
                time.sleep(3)








from groupy.client import Client
from config import api_token
from config import group_id
client = Client.from_token(api_token)
group = client.groups.get(group_id)

shoppingList = []

def commands():
    itemRequest = "!itemrequest"
    listRequest = "!shoppinglist"
    commandRequest = "!commands"

    all_messages = list(group.messages.list().autopage())  # creates a page of recent messages
    last_message = all_messages[0]  # variable stores the latest message in list
    recent_messages = list(group.messages.list_since(
        message_id=last_message.id))  # creates new list of messages only after most recent message


    for message in recent_messages:
        currentMessage = message.text.lower()
        print(currentMessage)

        ### REQUESTING ITEM FOR LIST###
        if itemRequest in currentMessage:
            item = currentMessage.split(itemRequest, 1)[1]
            item += " "
            shoppingList.append(item)
            Response = item + " has been added to the shopping list."
            client.bots.post(bot_id="199b4198cf92f44506557e07f2", text=Response)
            print(shoppingList)
            break


        ### Checking SHOPPING LIST#
        elif listRequest in currentMessage:
            Response = "The items on the shopping list are: "
            counter = 1
            for item in shoppingList:
                Response += str(counter) + "." + " " + item + ""
                counter += 1

            client.bots.post(bot_id="199b4198cf92f44506557e07f2", text=Response)

        ###REQUESTING COMMANDS ###
        elif commandRequest in currentMessage:
            Response = "The usable commands are: "
            counter = 1

'''
'''
bot = Bot("SmartBot", bot_id)
#stop = Stop("!stop")
#help = Help("!help")

#stop.handleCommand()
#help.handleCommand()

'''


recentFive = list(group.messages.list(limit=5))
for item in recentFive:
    print(item.name)