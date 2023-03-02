import logging
import os

BOT_HISTORY_LENGTH = os.getenv("BOT_HISTORY_LENGTH", 20)

# Log configuration
logger = logging.getLogger("ai_summary_bot")
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

# Telegram bot configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logging.error(
        "BOT_TOKEN env var is not found, cannot start the bot without it, create it with @BotFather Telegram bot! "
    )
else:
    logging.info("BOT_TOKEN found, starting the bot")

DEFAULT_MODEL_NAME = "gpt-3.5-turbo"
MODEL_NAME = os.getenv("MODEL_NAME")
if not MODEL_NAME:
    MODEL_NAME = DEFAULT_MODEL_NAME
    logging.info(f"MODEL_NAME env var is not found, using default model {MODEL_NAME}")
else:
    logging.info(f"MODEL_NAME is {MODEL_NAME}")
