from GroupMe.Bot import Bot
from GroupMe.Command import client
from Token import bot_id


while True:
    try:
        bot = Bot("SmartBot", bot_id)
    except:
        client.bots.post(bot_id=bot_id, text="--Bot Crashed--")

