#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import logging
import os
import pyrogram
from pyrogram.enums import ParseMode
from translation import Translation

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

logging.getLogger("pyrogram").setLevel(logging.WARNING)

def GetExpiryDate(chat_id):
    expires_at = (str(chat_id), "Source Cloned User", "1970.01.01.12.00.00")
    return expires_at

# Define the bot commands with enhanced logging
@pyrogram.Client.on_message(pyrogram.filters.command(["help", "about"]))
async def help_user(client, message):
    logger.debug("Received /help or /about command from user: %s", message.from_user.id)
    await client.send_message(
        chat_id=message.chat.id,
        text=Translation.HELP_USER,
        #parse_mode="markdown",  # Changed to markdown
        disable_web_page_preview=True,
        reply_to_message_id=message.id  # Corrected attribute
    )
    logger.debug("Sent help/about message to user: %s", message.from_user.id)

@pyrogram.Client.on_message(pyrogram.filters.command(["me"]))
async def get_me_info(client, message):
    logger.debug("Received /me command from user: %s", message.from_user.id)
    chat_id = str(message.from_user.id)
    chat_id, plan_type, expires_at = GetExpiryDate(chat_id)
    await client.send_message(
        chat_id=message.chat.id,
        text=Translation.CURENT_PLAN_DETAILS.format(chat_id, plan_type, expires_at),
        parse_mode="markdown",  # Changed to markdown
        disable_web_page_preview=True,
        reply_to_message_id=message.id  # Corrected attribute
    )
    logger.debug("Sent me info message to user: %s", message.from_user.id)

@pyrogram.Client.on_message(pyrogram.filters.command(["start"]))
async def start(client, message):
    logger.debug("Received /start command from user: %s", message.from_user.id)
    await client.send_message(
        chat_id=message.chat.id,
        text=Translation.START_TEXT,
        reply_to_message_id=message.id  # Corrected attribute
    )
    logger.debug("Sent start message to user: %s", message.from_user.id)

@pyrogram.Client.on_message(pyrogram.filters.command(["upgrade"]))
async def upgrade(client, message):
    logger.debug("Received /upgrade command from user: %s", message.from_user.id)
    await client.send_message(
        chat_id=message.chat.id,
        text=Translation.UPGRADE_TEXT,
        parse_mode="markdown",  # Changed to markdown
        reply_to_message_id=message.id,  # Corrected attribute
        disable_web_page_preview=True
    )
    logger.debug("Sent upgrade message to user: %s", message.from_user.id)

if __name__ == "__main__":
    # create download directory, if not exist
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
    
    plugins = dict(
        root="plugins"
    )
    
    app = pyrogram.Client(
        "AnyDLBot",
        bot_token=Config.TG_BOT_TOKEN,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        plugins=plugins
    )
    
    # Adding an authorized user
    Config.AUTH_USERS.add(829623994)

    # Basic connectivity test
    try:
        with app:
            logger.info("Testing connectivity...")
            me = app.get_me()
            logger.info("Bot info: %s", me)
            app.send_message("me", "Bot is now online!")
            logger.info("Connectivity test passed.")
    except Exception as e:
        logger.error(f"Connectivity test failed: {e}")

    logger.info("Starting the bot...")
    app.run()
    logger.info("Bot stopped.")
