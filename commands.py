from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, filters, ConversationHandler, MessageHandler, CommandHandler
from logger import logger

WAIT_FOR_GENDER, PHOTO, LOCATION, BIO = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'command: {update.message}')
    reply_keyboard = [["Boy", "Girl", "Other"]]
    await update.message.reply_text(
        "Hi! My name is Professor Bot. I will hold a conversation with you. "
        "Send /cancel to stop talking to me.\n\n"
        "Are you a boy or a girl?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Boy or Girl?"
        ),
    )
    return WAIT_FOR_GENDER


async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    start_photo(update)


async def start_photo(update: Update):
    await update.message.reply_text(
        "I see! Please send me a photo of yourself, "
        "so I know what you look like, or send /skip if you don't want to.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return PHOTO


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    # await photo_file.download_to_drive("user_photo.jpg")
    logger.info("Photo of %s: %s", user.first_name, "user_photo.jpg")
    await update.message.reply_text(
        "Gorgeous!"
    )
    return LOCATION


async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the photo and asks for a location."""
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    await update.message.reply_text(
        "I bet you look great!"
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        WAIT_FOR_GENDER: [MessageHandler(filters.Regex("^(Boy|Girl|Other)$"), gender)],
        PHOTO: [MessageHandler(filters.PHOTO, photo), CommandHandler("skip", skip_photo)],
        # LOCATION: [
        #     MessageHandler(filters.LOCATION, location),
        #     CommandHandler("skip", skip_location),
        # ],
        # BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
