class Command:
    def __init__(self):
        self.commands = {
            "!stop": self.stop,
            "help": self.help
        }

    def handle_command(self, command):
        response= ""
        if command in self.commands:
            response += self.commands[command]()
        else:
            response += "Sorry I don't understand the command: " + command + ". " + self.help()
        print("handle command returning: " + response)
        return response

    def stop(self):
        return "!stop"

    def help(self):
        response = "help:\r\n"

        for command in self.commands:
            response += command + "\r\n"

        return response