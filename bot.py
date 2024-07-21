#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
import os
import pyrogram
from pyrogram.errors import FloodWait
import asyncio

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

logging.getLogger("pyrogram").setLevel(logging.WARNING)

async def start_bot():
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

    try:
        await app.start()
        logger.info("Bot started successfully")
        await pyrogram.idle()  # Correct usage of idle() from pyrogram package
    except FloodWait as e:
        logger.warning(f"FloodWait: Waiting for {e.x} seconds before restarting")
        await asyncio.sleep(e.x)
        await start_bot()  # Retry starting the bot

if __name__ == "__main__":
    # Run the bot
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
