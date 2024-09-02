from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler
)
from settings import *
from details.handlers import *

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def register_handlers():
    dispatcher.add_handler(CommandHandler("start", start)),
    dispatcher.add_handler(CallbackQueryHandler(button_callback))
    dispatcher.add_handler(MessageHandler(Filters.text, text))
    dispatcher.add_handler(MessageHandler(Filters.video, video))
    dispatcher.add_handler(MessageHandler(Filters.photo, photo))
    dispatcher.add_handler(MessageHandler(Filters.document, document))
    dispatcher.add_handler(MessageHandler(Filters.audio, music))

    updater.start_polling()
    updater.idle()
register_handlers()
