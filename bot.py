#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
import os
import pyrogram


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

logging.getLogger("pyrogram").setLevel(logging.WARNING)

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
   # print(Config.TG_BOT_TOKEN)
   
    # Adding an authorized user
    #Config.AUTH_USERS.add(829623994)

    #@app.on_message(pyrogram.filters.command(["start"]))
   # async def start_command(client, message):
    #    await message.reply("Hello! I am a bot.")

    # Run the bot
    app.run()
