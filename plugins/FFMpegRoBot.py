#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @LegendBoy_XD

import os
import time
import logging
import pyrogram
from translation import Translation
# the logging things
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from helper_funcs.display_progress import progress_for_pyrogram
from helper_funcs.help_Nekmo_ffmpeg import cult_small_video, take_screen_shot


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

# the Strings used for this "thing"

logging.getLogger("pyrogram").setLevel(logging.WARNING)


@pyrogram.Client.on_message(pyrogram.filters.command(["info"]))
async def ffmpegrobot_ad(bot, update):
    if update.from_user.id not in Config.AUTH_USERS:
        await bot.send_messages(
            chat_id=update.chat.id,
            text="Buy The Subscriptions From @LegendBoy_XD To Use This Command",
            reply_to_message_id=update.message_id,
        )
        return
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.INFO,
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id,
    )


@pyrogram.Client.on_message(pyrogram.filters.command(["trim"]))
async def trim(bot, update):
    if update.from_user.id not in Config.AUTH_USERS:
        await bot.send_messages(
            chat_id=update.chat.id,
            text="Buy The Subscriptions From @LegendBoy_XD To Use This Command",
            reply_to_message_id=update.message_id,
        )
        return
    saved_file_path = (
        Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".FFMpegRoBot.mkv"
    )
    if os.path.exists(saved_file_path):
        a = await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.DOWNLOAD_START,
            reply_to_message_id=update.message_id,
        )
        commands = update.command
        if len(commands) == 3:
            # output should be video
            cmd, start_time, end_time = commands
            o = await cult_small_video(
                saved_file_path, Config.DOWNLOAD_LOCATION, start_time, end_time
            )
            logger.info(o)
            if o is not None:
                await bot.edit_message_text(
                    chat_id=update.chat.id,
                    text=Translation.UPLOAD_START,
                    message_id=a.message_id,
                )
                c_time = time.time()
                await bot.send_video(
                    chat_id=update.chat.id,
                    video=o,
                    # caption=description,
                    # duration=duration,
                    # width=width,
                    # height=height,
                    supports_streaming=True,
                    # reply_markup=reply_markup,
                    # thumb=thumb_image_path,
                    reply_to_message_id=update.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(Translation.UPLOAD_START, a, c_time),
                )
                os.remove(o)
                await bot.edit_message_text(
                    chat_id=update.chat.id,
                    text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG,
                    disable_web_page_preview=True,
                    message_id=a.message_id,
                )
        elif len(commands) == 2:
            # output should be screenshot
            cmd, start_time = commands
            o = await take_screen_shot(
                saved_file_path, Config.DOWNLOAD_LOCATION, start_time
            )
            logger.info(o)
            if o is not None:
                await bot.edit_message_text(
                    chat_id=update.chat.id,
                    text=Translation.UPLOAD_START,
                    message_id=a.message_id,
                )
                c_time = time.time()
                await bot.send_document(
                    chat_id=update.chat.id,
                    document=o,
                    # thumb=thumb_image_path,
                    # caption=description,
                    # reply_markup=reply_markup,
                    reply_to_message_id=update.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(Translation.UPLOAD_START, a, c_time),
                )
                c_time = time.time()
                await bot.send_photo(
                    chat_id=update.chat.id,
                    photo=o,
                    # caption=Translation.CUSTOM_CAPTION_UL_FILE,
                    reply_to_message_id=update.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(Translation.UPLOAD_START, a, c_time),
                )
                os.remove(o)
                await bot.edit_message_text(
                    chat_id=update.chat.id,
                    text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG,
                    disable_web_page_preview=True,
                    message_id=a.message_id,
                )
        else:
            await bot.edit_message_text(
                chat_id=update.chat.id,
                text=Translation.FF_MPEG_RO_BOT_RE_SURRECT_ED,
                message_id=a.message_id,
            )
    else:
        # reply help message
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.FF_MPEG_RO_BOT_STEP_TWO_TO_ONE,
            reply_to_message_id=update.message_id,
        )


@pyrogram.Client.on_message(pyrogram.filters.command(["storageinfo"]))
async def storage_info(bot, update):
    if update.from_user.id not in Config.AUTH_USERS:
        await bot.send_messages(
            chat_id=update.chat.id,
            text="Buy The Subscriptions From @LegendBoy_XD To Use This Command",
            reply_to_message_id=update.message_id,
        )
        return
    saved_file_path = (
        Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".FFMpegRoBot.mkv"
    )
    if os.path.exists(saved_file_path):
        metadata = extractMetadata(createParser(saved_file_path))
        duration = None
        if metadata.has("duration"):
            duration = metadata.get("duration")
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.FF_MPEG_RO_BOT_STOR_AGE_INFO.format(duration),
            reply_to_message_id=update.message_id,
        )
    else:
        # reply help message
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.FF_MPEG_RO_BOT_STEP_TWO_TO_ONE,
            reply_to_message_id=update.message_id,
        )


@pyrogram.Client.on_message(pyrogram.filters.command(["cleardownloadmedia"]))
async def clear_media(bot, update):
    if update.from_user.id not in Config.AUTH_USERS:
        await bot.send_messages(
            chat_id=update.chat.id,
            text="Buy The Subscriptions From @LegendBoy_XD To Use This Command",
            reply_to_message_id=update.message_id,
        )
        return
    saved_file_path = (
        Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".FFMpegRoBot.mkv"
    )
    if os.path.exists(saved_file_path):
        os.remove(saved_file_path)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.FF_MPEG_DEL_ETED_CUSTOM_MEDIA,
        reply_to_message_id=update.message_id,
    )


@pyrogram.Client.on_message(pyrogram.filters.command(["downloadmedia"]))
async def download_media(bot, update):
    if update.from_user.id not in Config.AUTH_USERS:
        await bot.send_messages(
            chat_id=update.chat.id,
            text="Buy The Subscriptions From @LegendBoy_XD To Use This Command",
            reply_to_message_id=update.message_id,
        )
        return
    saved_file_path = (
        Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".FFMpegRoBot.mkv"
    )
    if not os.path.exists(saved_file_path):
        a = await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.DOWNLOAD_START,
            reply_to_message_id=update.message_id,
        )
        try:
            c_time = time.time()
            await bot.download_media(
                message=update.reply_to_message,
                file_name=saved_file_path,
                progress=progress_for_pyrogram,
                progress_args=(Translation.DOWNLOAD_START, a, c_time),
            )
        except (ValueError) as e:
            await bot.edit_message_text(
                chat_id=update.chat.id, text=str(e), message_id=a.message_id
            )
        else:
            await bot.edit_message_text(
                chat_id=update.chat.id,
                text=Translation.SAVED_RECVD_DOC_FILE,
                message_id=a.message_id,
            )
    else:
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.FF_MPEG_RO_BOT_STOR_AGE_ALREADY_EXISTS,
            reply_to_message_id=update.message_id,
        )
