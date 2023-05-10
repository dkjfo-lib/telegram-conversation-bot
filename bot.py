import os
from telegram.ext import ApplicationBuilder
from commands import *
from logger import logger


def launch_bot():
    TOKEN = os.getenv('BOT_TOKEN')

    logger.info(f'creating bot with token:"{TOKEN}"...')
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(conv_handler)
    logger.info(f'bot successfully created.')

    logger.info('polling messages...')
    application.run_polling()
