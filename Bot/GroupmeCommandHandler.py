from datetime import datetime
from Bot.LastfmCommands import LastfmCommands
from Database.Database import Database
from Token import bot_id, groupyToken, groupy_id
from groupy.client import Client
from groupy.api.attachments import Mentions, Image

client = Client.from_token(groupyToken)
group = client.groups.get(groupy_id)


class GroupmeCommandHandler:
    """The Groupme Command Handler Class.

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

        self.Lastfm = LastfmCommands()
        self.commands.update(self.Lastfm.commands)
        self.commandDescriptions.update(self.Lastfm.commandDescriptions)
        self.client = Client.from_token(groupyToken)

    def run_scheduled_tasks(self):
        """
        method runs tasks on specific days/times
        :return:
        """
        members = self.get_member_ids()
        if (datetime.today().day == 0 and
                datetime.today().hour == 10 and
                datetime.today().min == 0 and
                (datetime.today().second == 0 or datetime.second == 1)):

            for groupme_id in members:
                botResponse = str(self.commands["!rewind"](groupme_id=groupme_id))
                mention = Mentions(loci=[(0, len(botResponse))], user_ids=[groupme_id])
                client.bots.post(bot_id=bot_id, text=str(botResponse), attachments=[mention])






    def get_member_ids(self):
        """
        Fetches the groupme_ids of all of the members in the group
        :return member_ids: {list} member ids
        """
        members = client.groups.get(57087652).members
        member_ids =[]
        for member in members:
            member_ids.append(member.user_id)
        return member_ids

    def get_user_permissions(self, groupme_id):
        """
        Fetches a users command permission
        :param groupme_id: {Int} user's GroupMe id
        :return user_permissions: {Int} the users permission value
        """
        user_permissions = self.database.df.loc[self.database.df['GroupMeID'] == str(groupme_id)]['permission'].tolist()[0]
        return user_permissions

    def execute(self, command, message_user, groupme_id, message_attachments=None):
        """
        Executes commands by accessing the command list which links the !{command}
        keyword with their given methods. It parses the contents of the message
        containing the command and splits them into seperate substrings to allow
        for parameters.


        :param command:  {String} the message content containing the !{command}
        :param message_user:  {String} the name of the user who sent the message
        :param groupme_id: {Integer} the user's groupme id
        :param message_attachments: {list} list of attachment objects
        :return: None
        """
        botResponse = ""
        if command == "!reboot":
            return "!reboot"

        command = command.lower()
        splitCommandList = command.split()

        if splitCommandList[0] in self.commands:
            if message_attachments: ## If command contains an attachment
                if type(message_attachments[0]) is Mentions: # if attachment is a mention
                    other_groupme_id = message_attachments[0].user_ids[0]
                    if len(splitCommandList) == 3: ## If the there are three parameters - "!compareme @joshua reid"
                        print(
                            str(datetime.now().hour) + ":" + str(datetime.now().minute) + " " + message_user + ": " +
                            splitCommandList[
                                0] + " " + splitCommandList[1])
                        botResponse += str(self.commands[splitCommandList[0]](groupme_id, other_groupme_id))
                        mention = Mentions(loci=[[0,len(botResponse)], [0, len(botResponse)]], user_ids=[groupme_id, other_groupme_id])
                        client.bots.post(bot_id=bot_id, text=str(botResponse), attachments=[mention])
                        return botResponse



            else: # if command does not contain an attachment
                if len(splitCommandList) == 1:
                    print(
                        str(datetime.now().hour) + ":" + str(datetime.now().minute) + " " + message_user + ": " + splitCommandList[
                            0])
                    response = self.commands[splitCommandList[0]](groupme_id)
                    if type(response) is str:
                        botResponse += response
                        mention = Mentions(loci=[(0, len(botResponse))], user_ids=[groupme_id])
                        client.bots.post(bot_id=bot_id, text=botResponse, attachments=[mention])
                    elif type(response) is Image:
                        client.bots.post(bot_id=bot_id, text=splitCommandList[0][1:], attachments=[response])



                elif len(splitCommandList) == 2:
                    print(
                        str(datetime.now().hour) + ":" + str(datetime.now().minute) + " " + message_user + ": " + splitCommandList[
                            0] + " " + splitCommandList[1])
                    response = self.commands[splitCommandList[0]](groupme_id, splitCommandList[1])
                    if type(response) is str:
                        botResponse += response
                        mention = Mentions(loci=[(0, len(botResponse))], user_ids=[groupme_id])
                        client.bots.post(bot_id=bot_id, text=botResponse, attachments=[mention])
                    elif type(response) is Image:
                        client.bots.post(bot_id=bot_id, text=splitCommandList[0][1:], attachments=[response])

                elif len(splitCommandList) == 3:
                    print(
                        str(datetime.now().hour) + ":" + str(datetime.now().minute) + " " + message_user + ": " + splitCommandList[
                            0] + " " + splitCommandList[1] + " " + splitCommandList[2])
                    botResponse += str(
                        self.commands[splitCommandList[0]](groupme_id, splitCommandList[1], splitCommandList[2]))
                    mention = Mentions(loci=[(0, len(botResponse))], user_ids=[groupme_id])
                    client.bots.post(bot_id=bot_id, text=str(botResponse), attachments=[mention])

                elif len(splitCommandList) == 4:
                    print(
                        str(datetime.now().hour) + ":" + str(datetime.now().minute) + " " + message_user + ": " + splitCommandList[
                            0] + " " + splitCommandList[1] + " " + splitCommandList[2] + " " + splitCommandList[3])
                    botResponse += str(self.commands[splitCommandList[0]](groupme_id, splitCommandList[1], splitCommandList[2],
                                                                          splitCommandList[3]))
                    mention = Mentions(loci=[0, len(botResponse)], user_ids=[groupme_id])
                    client.bots.post(bot_id=bot_id, text=str(botResponse), attachments=[mention])



    def reboot(self, groupme_id):
        """
        Restarts the bot
        :return: {String} returns the command !reboot
        """
        reboot = "!reboot"
        if self.get_user_permissions(groupme_id) == 1:
            return reboot
        else:
            client.bots.post(bot_id=bot_id, text="You do not have permission to use !reboot")



    def list_commands(self, user):
        """

        :param user: a blank parameter for execute()
        :return: {String} A list of current commands
        """
        botResponse = "Commands:\r\n"
        for command in self.commandDescriptions:
            botResponse += "-" + command + ": " + self.commandDescriptions[command] + "\r\n"

        return botResponse


