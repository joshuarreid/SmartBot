from GroupMe.Bot import Bot
from GroupMe.Command import client
from Token import bot_id
from traceback import format_exc

while True:
    try:
        bot = Bot("SmartBot", bot_id)
    except :
        client.bots.post(bot_id=bot_id, text="Uh Oh! Something went wrong!")
        exceptiondata = format_exc().splitlines()
        exceptiondata = exceptiondata[len(exceptiondata)-3:]
        print("----------- CRASH REPORT -----------")
        for item in exceptiondata:
            print(item)
        print("------------------------------------")





