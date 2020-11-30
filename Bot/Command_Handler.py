from datetime import datetime
from Bot.Lastfm_Commands import Lastfm_Commands
from Database.Database import Database
from Token import bot_id, groupyToken, groupy_id
from groupy.client import Client

client = Client.from_token(groupyToken)
group = client.groups.get(groupy_id)


class Command_Handler:
    """The Command_Handler Class

    The command handler class is responsible for connecting the bot to API's and
    executing the commands. It contains the list of commands and their given
    descriptions; it also contains some default commands for controlling the bot.


    """
    def __init__(self):
        self.commands = {
            "!reboot": self.reboot,
            "!commands": self.list_commands,

        }

        self.commandDescriptions = {
            "!reboot": "restarts bot",
            "!commands": "Lists all commands",
        }

        self.database = Database('GroupMe')

        self.Lastfm = Lastfm_Commands()
        self.commands.update(self.Lastfm.commands)
        self.commandDescriptions.update(self.Lastfm.commandDescriptions)



    def execute(self, command, user, groupme_id):
        """
        Executes commands by accessing the command list which links the !{command}
        keyword with their given methods. It parses the contents of the message
        containing the command and splits them into seperate substrings to allow
        for parameters.


        :param command:  {String} the message content containing the !{command}
        :param user:  {String} the name of the user who sent the message
        :param groupme_id: {Integer} the user's groupme id
        :return: None
        """
        botResponse = ""
        if command == "!reboot":
            return "!reboot"

        splitCommandList = command.split()
        if splitCommandList[0] in self.commands:
            if len(splitCommandList) == 1:
                print(
                    str(datetime.now().hour) + ":" + str(datetime.now().minute) + " " + user + ": " + splitCommandList[
                        0])
                # TODO mention = attachments.Mentions(loci=[(3,4)], user_ids=[user_id])
                botResponse += str(self.commands[splitCommandList[0]](groupme_id))
                client.bots.post(bot_id=bot_id, text=str(botResponse))
                return botResponse

            elif len(splitCommandList) == 2:
                print(
                    str(datetime.now().hour) + ":" + str(datetime.now().minute) + " " + user + ": " + splitCommandList[
                        0] + " " + splitCommandList[1])
                botResponse += str(self.commands[splitCommandList[0]](groupme_id, splitCommandList[1]))
                client.bots.post(bot_id=bot_id, text=str(botResponse))
                return botResponse

            elif len(splitCommandList) == 3:
                print(
                    str(datetime.now().hour) + ":" + str(datetime.now().minute) + " " + user + ": " + splitCommandList[
                        0] + " " + splitCommandList[1] + " " + splitCommandList[2])
                botResponse += str(
                    self.commands[splitCommandList[0]](groupme_id, splitCommandList[1], splitCommandList[2]))
                client.bots.post(bot_id=bot_id, text=str(botResponse))

            elif len(splitCommandList) == 4:
                print(
                    str(datetime.now().hour) + ":" + str(datetime.now().minute) + " " + user + ": " + splitCommandList[
                        0] + " " + splitCommandList[1] + " " + splitCommandList[2] + " " + splitCommandList[3])
                botResponse += str(self.commands[splitCommandList[0]](groupme_id, splitCommandList[1], splitCommandList[2],
                                                                      splitCommandList[3]))
                client.bots.post(bot_id=bot_id, text=str(botResponse))



    def reboot(self):
        """

        :return: {String} returns the command !reboot
        """
        reboot = "!reboot"
        return reboot



    def list_commands(self, user):
        """

        :param user: a blank parameter for execute()
        :return: {String} A list of current commands
        """
        botResponse = "Commands:\r\n"

        for command in self.commandDescriptions:
            botResponse += "-" + command + ": " + self.commandDescriptions[command] + "\r\n"

        return botResponse
