import streamlit as st
import logging
from telegram import __version__ as TG_VER
from telegram import Bot, Update, ForceReply
from telegram.ext import CommandHandler, MessageHandler, filters, Updater

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# Set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and context.
def start(update: Update, context) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("Help!")


def echo(update: Update, context) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Your Streamlit code here
    st.title("Telegram Bot Demo")
    st.write("Enter /start or /help commands to interact with the bot.")

    # Create the bot and updater
    bot = Bot(token="6262427395:AAF9cX0_nxPYKPNlW8Kwy6BcocFnkTRIQ-A")
    updater = Updater(bot=bot, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Register message handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the bot
    updater.start_polling()

    # Display success or failure message
    if updater.running:
        st.success("Bot started successfully!")
    else:
        st.error("Failed to start the bot.")


if __name__ == "__main__":
    main()

