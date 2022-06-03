#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @LegendBoy_XD

import os
import time
import shutil
import logging
import pyrogram
from PIL import Image
import moviepy.editor as pp
from translation import Translation
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from helper_funcs.ran_text import random_char
from helper_funcs.display_progress import progress_for_pyrogram


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config



logging.getLogger("pyrogram").setLevel(logging.WARNING)


@pyrogram.Client.on_message(pyrogram.filters.command(["c2a"]))
async def convert_to_audio(bot, update):
    if update.from_user.id not in Config.AUTH_USERS:
        await bot.send_messages(
            chat_id=update.chat.id,
            text="Buy The Subscriptions From @LegendBoy_XD To Get Access Of Advanced Features Of This Bot",
            reply_to_message_id=update.message_id,
        )
        return
    if (update.reply_to_message is not None) and (
        update.reply_to_message.media is not None
    ):
        rnom = random_char(5)
        download_location = Config.DOWNLOAD_LOCATION + "/" + f"{rnom}" + "/"
        ab = await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.DOWNLOAD_FILE,
            reply_to_message_id=update.message_id,
        )
        c_time = time.time()
        the_real_download_location = await bot.download_media(
            message=update.reply_to_message,
            file_name=download_location,
            progress=progress_for_pyrogram,
            progress_args=(Translation.DOWNLOAD_FILE, ab, c_time),
        )
        if the_real_download_location is not None:
            a = await bot.edit_message_text(
                text=f"Video Download Successfully, now trying to convert into Audio. \n\n⌛️Wait for some time.",
                chat_id=update.chat.id,
                message_id=ab.message_id,
            )
            f_name = the_real_download_location.rsplit("/", 1)[-1]
            clip = pp.VideoFileClip(the_real_download_location)
            clip.audio.write_audiofile(f_name + ".mp3")
            audio_file_location = f_name + ".mp3"
            logger.info(audio_file_location)
            metadata = extractMetadata(createParser(audio_file_location))
            if metadata.has("duration"):
                duration = metadata.get("duration").seconds
            """thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
            if not os.path.exists(thumb_image_path):
                thumb_image_path = None
            else:
                metadata = extractMetadata(createParser(thumb_image_path))
                if metadata.has("width"):
                    width = metadata.get("width")
                if metadata.has("height"):
                    height = metadata.get("height")
                # get the correct width, height, and duration for videos greater than 10MB
                # resize image
                # ref: https://t.me/PyrogramChat/44663
                # https://stackoverflow.com/a/21669827/4723940
                Image.open(thumb_image_path).convert("RGB").save(thumb_image_path)
                img = Image.open(thumb_image_path)
                # https://stackoverflow.com/a/37631799/4723940
                # img.thumbnail((90, 90))
                img.resize((90, height))
                img.save(thumb_image_path, "JPEG")"""
            # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
            # try to upload file
            await a.delete()
            c_time = time.time()
            up = await bot.send_message(
                text=Translation.UPLOAD_START,
                chat_id=update.chat.id,
            )
            c_time = time.time()
            await bot.send_audio(
                chat_id=update.chat.id,
                audio=audio_file_location,
                duration=duration,
                # performer="",
                # title="",
                # reply_markup=reply_markup,
                reply_to_message_id=update.reply_to_message.message_id,
                progress=progress_for_pyrogram,
                progress_args=(Translation.UPLOAD_START, up, c_time),
            )
            try:
                os.remove(thumb_image_path)
                os.remove(the_real_download_location)
                os.remove(audio_file_location)
            except BaseException:
                pass
            await bot.edit_message_text(
                text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG,
                chat_id=update.chat.id,
                message_id=up.message_id,
                disable_web_page_preview=True,
            )
    else:
        await bot.send_message(
            chat_id=update.chat.id,
            text=f"Reply with a telegram Video file to convert To Audiology",
            reply_to_message_id=update.message_id,
        )
