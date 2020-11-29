from datetime import datetime
from groupy.client import Client
from Token import groupyToken, groupy_id, bot_id
from Bot.Lastfm import Lastfm
from Database.Database import Database
import Database_old

client = Client.from_token(groupyToken)
group = client.groups.get(groupy_id)


class Command_Handler:
    def __init__(self):


        self.commands = {
            "!reboot": self.reboot,
            "!commands": self.listCommands,

        }


        self.commandDescriptions = {
            "!reboot": "restarts bot",
            "!commands": "Lists all commands",
        }


        ### TODO update command descriptions in the class file
        self.Lastfm = Lastfm()
        self.commands.update(self.Lastfm.commands)
        self.commandDescriptions.update(self.Lastfm.commandDescriptions)

        self.database = Database('GroupMe')

    ### Function handles each command and creates the correct response ###
    def execute(self, command, user, user_id):
        ### TODO get user_id from groupme api
        botResponse = ""
        if command == "!reboot":
            return "!reboot"

        splitCommandList = command.split()
        if splitCommandList[0] in self.commands:
            if len(splitCommandList) == 1:
                print(
                    str(datetime.now().hour) + ":" + str(datetime.now().minute) + " " + user + ": " + splitCommandList[
                        0])
                botResponse += str(self.commands[splitCommandList[0]](user_id))
                client.bots.post(bot_id=bot_id, text=str(botResponse))
                return botResponse

            elif len(splitCommandList) == 2:
                print(
                    str(datetime.now().hour) + ":" + str(datetime.now().minute) + " " + user + ": " + splitCommandList[
                        0] + " " + splitCommandList[1])
                botResponse += str(self.commands[splitCommandList[0]](user_id, splitCommandList[1]))
                client.bots.post(bot_id=bot_id, text=str(botResponse))
                return botResponse

            elif len(splitCommandList) == 3:
                print(
                    str(datetime.now().hour) + ":" + str(datetime.now().minute) + " " + user + ": " + splitCommandList[
                        0] + " " + splitCommandList[1] + " " + splitCommandList[2])
                botResponse += str(self.commands[splitCommandList[0]](user_id, splitCommandList[1], splitCommandList[2]))
                client.bots.post(bot_id=bot_id, text=str(botResponse))

            elif len(splitCommandList) == 4:
                print(
                    str(datetime.now().hour) + ":" + str(datetime.now().minute) + " " + user + ": " + splitCommandList[
                        0] + " " + splitCommandList[1] + " " + splitCommandList[2] + " " + splitCommandList[3])
                botResponse += str(self.commands[splitCommandList[0]](user_id, splitCommandList[1], splitCommandList[2],
                                                                      splitCommandList[3]))
                client.bots.post(bot_id=bot_id, text=str(botResponse))

    def reboot(self):
        reboot = "!reboot"
        return reboot

    ### Command lists all of the available commands ###
    def listCommands(self, user):
        botResponse = "Commands:\r\n"

        for command in self.commandDescriptions:
            botResponse += "-" + command + ": " + self.commandDescriptions[command] + "\r\n"

        return botResponse