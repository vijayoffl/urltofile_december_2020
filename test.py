#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import pyrogram

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import configurations
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# Ensure the download directory exists
if not os.path.isdir(Config.DOWNLOAD_LOCATION):
    os.makedirs(Config.DOWNLOAD_LOCATION)

# Define the bot commands
@pyrogram.Client.on_message(pyrogram.filters.command(["start"]))
async def start(client, message):
    logger.debug("Received /start command from user: %s", message.from_user.id)
    await client.send_message(
        chat_id=message.chat.id,
        text="Hello! I am a bot. How can I assist you?",
        reply_to_message_id=message.id
    )
    logger.debug("Sent start message to user: %s", message.from_user.id)

@pyrogram.Client.on_message(pyrogram.filters.command(["help", "about"]))
async def help_user(client, message):
    logger.debug("Received /help or /about command")
    await client.send_message(
        chat_id=message.chat.id,
        text="Here is some help text",
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=message.id
    )
    logger.debug("Sent help/about message")

@pyrogram.Client.on_message(pyrogram.filters.command(["me"]))
async def get_me_info(client, message):
    logger.debug("Received /me command")
    chat_id = str(message.from_user.id)
    await client.send_message(
        chat_id=message.chat.id,
        text=f"Your chat ID is {chat_id}",
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=message.id
    )
    logger.debug("Sent me info message")

@pyrogram.Client.on_message(pyrogram.filters.command(["upgrade"]))
async def upgrade(client, message):
    logger.debug("Received /upgrade command")
    await client.send_message(
        chat_id=message.chat.id,
        text="Upgrade instructions",
        parse_mode="html",
        reply_to_message_id=message.id,
        disable_web_page_preview=True
    )
    logger.debug("Sent upgrade message")

# Initialize and run the bot
if __name__ == "__main__":
    app = pyrogram.Client(
        "test_bot",
        bot_token=Config.TG_BOT_TOKEN,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH
    )

    # Basic connectivity test
    try:
        app.start()
        logger.info("Bot started successfully.")
        me = app.get_me()
        logger.info("Bot info: %s", me)
        app.send_message("me", "Bot is now online!")
        logger.info("Connectivity test passed.")
    except Exception as e:
        logger.error(f"Connectivity test failed: {e}")
    finally:
        app.run()
        logger.info("Bot stopped.")
