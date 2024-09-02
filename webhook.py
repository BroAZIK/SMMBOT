from telegram import Bot
from settings import *

bot = Bot(token=TOKEN)

def get_info():
    print(bot.get_webhook_info())


def delete():
    print(bot.delete_webhook())


def set():
    url = 'https://SMMBOTwithAZIZBEK.pythonanywhere.com/webhook'
    print(bot.set_webhook(url=url))

set()
