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