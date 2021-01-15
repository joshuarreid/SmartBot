from Bot.Bot import Bot
from Bot.Command_Handler import client
from Token import bot_id
from traceback import format_exc
from groupy.exceptions import BadResponse

while True:
    try:
        bot = Bot("SmartBot", bot_id)

    except BadResponse:
        print("Bad Response")
    except:
        exceptiondata = format_exc().splitlines()
        exceptiondata = exceptiondata[len(exceptiondata) - 3:]
        botResponse = "-----CRASH REPORT------\r\n"
        for error in exceptiondata:
            botResponse += error + "\r\n"
        botResponse += "-----------------------"
        client.bots.post(bot_id=bot_id, text=botResponse)
