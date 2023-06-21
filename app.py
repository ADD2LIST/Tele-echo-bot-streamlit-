import streamlit as st
import logging
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import Update, ForceReply
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# Set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Your Streamlit code here
    st.title("Telegram Bot Demo")
    st.write("Enter /start or /help commands to interact with the bot.")

    # Create the bot handlers
    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", help_command)
    echo_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)

    # Get the Streamlit session state
    session_state = st.session_state

    # Check if the bot has been started
    if "bot_started" not in session_state:
        # Start the bot and add the handlers
        application = Application.builder().token("YOUR_BOT_TOKEN").build()
        application.add_handler(start_handler)
        application.add_handler(help_handler)
        application.add_handler(echo_handler)
        session_state["bot_started"] = True

        # Run the bot until the user presses Ctrl-C
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    # Display success or failure message
    if "bot_response" in session_state:
        response = session_state.pop("bot_response")
        st.success(response)
    elif "bot_error" in session_state:
        error = session_state.pop("bot_error")
        st.error(error)


if __name__ == "__main__":
    main()
