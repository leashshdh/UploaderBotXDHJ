#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @LegendBoy_XD

import os
import json
import math
import time
import shutil
import logging
import pyrogram
import subprocess
from PIL import Image
from translation import Translation
from hachoir.parser import createParser
from plugins.dl_button import ddl_call_back
from hachoir.metadata import extractMetadata
from plugins.youtube_dl_button import youtube_dl_call_back
from helper_funcs.display_progress import humanbytes, progress_for_pyrogram


logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

logging.getLogger("pyrogram").setLevel(logging.WARNING)


@pyrogram.Client.on_callback_query()
async def button(bot, update):
    if update.from_user.id not in Config.AUTH_USERS:
        await bot.edit_message_text(
            chat_id=update.message.chat.id,
            text="Buy The Subscriptions From @LegendBoy_XD To Get Access Of Advanced Features Of This Bot",
            reply_to_message_id=update.message.message_id,
        )
        return
    cb_data = update.data
    if ":" in cb_data:
        extract_dir_path = (
            Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + "zipped" + "/"
        )
        if not os.path.isdir(extract_dir_path):
            await bot.delete_messages(
                chat_id=update.message.chat.id,
                message_ids=update.message.message_id,
                revoke=True,
            )
            return False
        zip_file_contents = os.listdir(extract_dir_path)
        type_of_extract, index_extractor, undefined_tcartxe = cb_data.split(":")
        if index_extractor == "NONE":
            try:
                shutil.rmtree(extract_dir_path)
            except BaseException:
                pass
            await bot.edit_message_text(
                chat_id=update.message.chat.id,
                text=Translation.CANCEL_STR,
                message_id=update.message.message_id,
            )
        elif index_extractor == "ALL":
            i = 0
            for file_content in zip_file_contents:
                current_file_name = os.path.join(extract_dir_path, file_content)
                start_time = time.time()
                await bot.send_document(
                    chat_id=update.message.chat.id,
                    document=current_file_name,
                    # thumb=thumb_image_path,
                    caption=file_content,
                    # reply_markup=reply_markup,
                    reply_to_message_id=update.message.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        Translation.UPLOAD_START,
                        update.message,
                        start_time,
                    ),
                )
                i = i + 1
                os.remove(current_file_name)
            try:
                shutil.rmtree(extract_dir_path)
            except BaseException:
                pass
            await bot.edit_message_text(
                chat_id=update.message.chat.id,
                text=Translation.ZIP_UPLOADED_STR.format(i, "0"),
                message_id=update.message.message_id,
            )
        else:
            file_content = zip_file_contents[int(index_extractor)]
            current_file_name = os.path.join(extract_dir_path, file_content)
            start_time = time.time()
            await bot.send_document(
                chat_id=update.message.chat.id,
                document=current_file_name,
                # thumb=thumb_image_path,
                caption=file_content,
                # reply_markup=reply_markup,
                reply_to_message_id=update.message.message_id,
                progress=progress_for_pyrogram,
                progress_args=(Translation.UPLOAD_START, update.message, start_time),
            )
            try:
                shutil.rmtree(extract_dir_path)
            except BaseException:
                pass
            await bot.edit_message_text(
                chat_id=update.message.chat.id,
                text=Translation.ZIP_UPLOADED_STR.format("1", "0"),
                message_id=update.message.message_id,
            )
    elif "|" in cb_data:
        await youtube_dl_call_back(bot, update)
    elif "=" in cb_data:
        await ddl_call_back(bot, update)
    elif "DelMedia" in cb_data:
        saved_file_path = (
            Config.DOWNLOAD_LOCATION
            + "/"
            + str(update.from_user.id)
            + ".FFMpegRoBot.mkv"
        )
        try:
            os.remove(saved_file_path)
            print(saved_file_path, " removed/deleted successfully.")
            await bot.edit_message_text(
                chat_id=update.message.chat.id,
                message_id=update.message.message_id,
                text=f"✅ Media file deleted successfully.",
            )
        except Exception as fc:
            print(fc)
    elif "NO-delM" in cb_data:
        await bot.edit_message_text(
            chat_id=update.message.chat.id,
            message_id=update.message.message_id,
            text=f"Media file is not deleted.",
        )
    elif "//" in cb_data:
        szze, ms_id = cb_data.rsplit("//")
        download_directory = Config.DOWNLOAD_LOCATION + "/" + str(ms_id)
        smze, vtt = 0, 0
        """ToStr = ' •• '.join(map(str, os.listdir(download_directory)))
        await bot.send_message(chat_id = update.message.chat.id, text=ToStr)
        print(os.listdir(download_directory), "cb_buttons")
        print('\n\n', cb_data, 'cb_buttons')"""
        if os.path.isdir(download_directory):
            lsst = os.listdir(download_directory)
            try:
                for vt in lsst:
                    if ".vtt" in vt:
                        vtt += 1
                for ele in os.scandir(download_directory):
                    smze += os.path.getsize(ele)
                    siio = humanbytes(int(smze))
            except Exception as vit:
                print(vit, "Error Exception vtt")
                pass
        if not os.path.isdir(download_directory):
            siio = "This file is not present in the directory!"
            await update.answer(siio)
            """elif:
            for ele in os.scandir(download_directory):
                smze+=os.path.getsize(ele)
            if smze>int(cb_data.split("//")[1])*1.2:
                await update.answer("Video Downloded Successfully. \n\n Now Downloading audio", show_alert="True")
             elif:
            for ele in os.scandir(download_directory):
                smze+=os.path.getsize(ele)
            if smze>int(cb_data.split("//")[1]):
                await update.answer("Video, audio downloaded sucessfully. \n\n Upload starts soon.", show_alert="True")"""
        elif len(lsst) - vtt == 4:
            await update.answer(
                "Video & Audio downloaded sucessfully\n\nUploading starts soon. . .",
                show_alert="True",
            )
        elif "N/A" in cb_data:
            await update.answer(f'Downloaded: {siio} of {"N/A"}', show_alert="True")
        elif "None" in cb_data:
            await update.answer(f'Downloaded: {siio} of {"N/A"}', show_alert="True")
        elif siio and szze:
            if int(smze) < int(szze):
                await update.answer(
                    f"Downloaded: {siio} of {humanbytes(int(szze))}", show_alert="True"
                )
            else:
                diff = smze - szze
                print(lsst, "video downloaded successfully")
                await update.answer(
                    f"Video Downloded Successfully: {humanbytes(int(szze))} \n\n Now Downloading audio: {humanbytes(diff)}",
                    show_alert="True",
                )
        else:
            try:
                await update.answer(
                    f"Downloaded: {siio} Please Wait Patiently", show_alert="True"
                )
            except BaseException:
                pass

            
