from Bot.Bot import Bot
from Bot.Command_Handler import client
from Token import bot_id
from traceback import format_exc

while True:
    try:
        bot = Bot("SmartBot", bot_id)
    except:
        client.bots.post(bot_id=bot_id, text="Uh Oh! Something went wrong!")
        exceptiondata = format_exc().splitlines()
        exceptiondata = exceptiondata[len(exceptiondata) - 3:]
        botResponse = "-----CRASH REPORT------\r\n"
        for error in exceptiondata:
            botResponse += error + "\r\n"
        botResponse += "-----------------------"
