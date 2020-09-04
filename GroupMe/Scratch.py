"""
def handle_command(self, command, user):
    response = ""
    if command in self.commands:
        if command == "!stop":
            return "!stop"
        else:
            response += str(self.commands[command](user))
            print(str(datetime.now().hour) + ":" + str(datetime.now().minute) + " " + user + ": " + command)
            client.bots.post(bot_id=bot_id, text=str(response))
            return response

"""