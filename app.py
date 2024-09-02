from flask import Flask, request
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    Dispatcher,
)
from telegram import Bot
from settings import *
from details.handlers import *

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)
app = Flask(__name__)

@app.route('/webhook', methods=['GET', "POST"])
def register_handlers():

    if request.method == "GET":
        return "Webhook is running...!"
    
    if request.method == "POST":

        print("post keldi")
        body = request.get_json()

        update = Update.de_json(body, bot)
        dispatcher.add_handler(CommandHandler("start", start)),
        dispatcher.add_handler(CallbackQueryHandler(button_callback))
        dispatcher.add_handler(MessageHandler(Filters.text, text))
        dispatcher.add_handler(MessageHandler(Filters.video, video))
        dispatcher.add_handler(MessageHandler(Filters.photo, photo))
        dispatcher.add_handler(MessageHandler(Filters.document, document))
        dispatcher.add_handler(MessageHandler(Filters.audio, music))

        dispatcher.process_update(update)

        return {"message": "ok"}
    
if __name__ == "__main__":
    app.run(debug=True)
