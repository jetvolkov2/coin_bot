import time
import logging

from telegram.ext import (
    Filters,
    Updater,
    MessageHandler,
    CommandHandler,
    CallbackQueryHandler,
)

from coin.simple import send_price
from settings import TOKEN, UPDATE_TIME
from utils.cmd import Command, Callback
from handlers import commands, callbacks

updater = Updater(token=TOKEN)
job_queue = updater.job_queue
dispatcher = updater.dispatcher

# dispatcher.add_handler(MessageHandler(Filters.text, ping, run_async=True))

# callbacks
dispatcher.add_handler(
    CallbackQueryHandler(
        callbacks.settings,
        pattern=rf"^{Callback.SETTINGS[1]}$",
        run_async=True,
    )
)
dispatcher.add_handler(
    CallbackQueryHandler(
        callbacks.show_coin_list,
        pattern=r"^coin_list_\w$",
        run_async=True,
    )
)
dispatcher.add_handler(
    CallbackQueryHandler(
        callbacks.show_coin_list_menu,
        pattern=r"^coin_list_menu$",
        run_async=True,
    )
)
dispatcher.add_handler(
    CallbackQueryHandler(
        callbacks.manage_coin_list,
        pattern=r"^next_coin_list$|^previous_coin_list$",
        run_async=True,
    )
)
dispatcher.add_handler(
    CallbackQueryHandler(
        callbacks.coin_settings,
        pattern=rf"^{Callback.COIN_ID}_",
        run_async=True,
    )
)
dispatcher.add_handler(
    CallbackQueryHandler(
        callbacks.currencies_list,
        pattern=r"^currencies_list$|^next_currencies$|^previous_currencies$",
        run_async=True,
    )
)

# commands
dispatcher.add_handler(CommandHandler(Command.START, commands.start, run_async=True))

logging.info("Start bot.")
updater.start_polling()

job_minute = job_queue.run_repeating(send_price, interval=UPDATE_TIME)

updater.idle()
