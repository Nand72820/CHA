import asyncio
import logging
import random
import time
import psutil
import config
from ChampuChatBot import _boot_
from ChampuChatBot import get_readable_time
from ChampuChatBot import ChampuChatBot, mongo
from datetime import datetime
from pymongo import MongoClient
from pyrogram.enums import ChatType
from pyrogram import Client, filters
from config import OWNER_ID, MONGO_URL, OWNER_USERNAME
from pyrogram.errors import FloodWait, ChatAdminRequired
from ChampuChatBot.database.chats import get_served_chats, add_served_chat
from ChampuChatBot.database.users import get_served_users, add_served_user
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from ChampuChatBot.modules.helpers import (
    START,
    START_BOT,
    PNG_BTN,
    CLOSE_BTN,
    HELP_BTN,
    HELP_BUTN,
    HELP_READ,
    HELP_START,
    SOURCE_READ,
)

GSTART = """**ʜᴇʏ ᴅᴇᴀʀ {}**\n\n**ᴛʜᴀɴᴋs ғᴏʀ sᴛᴀʀᴛ ᴍᴇ ɪɴ ɢʀᴏᴜᴘ ʏᴏᴜ ᴄᴀɴ ᴄʜᴀɴɢᴇ ʟᴀɴɢᴜᴀɢᴇ ʙʏ ᴄʟɪᴄᴋ ᴏɴ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs.**\n**ᴄʟɪᴄᴋ ᴀɴᴅ sᴇʟᴇᴄᴛ ʏᴏᴜʀ ғᴀᴠᴏᴜʀɪᴛᴇ ʟᴀɴɢᴜᴀɢᴇ ᴛᴏ sᴇᴛ ᴄʜᴀᴛ ʟᴀɴɢᴜᴀɢᴇ ғᴏʀ ʙᴏᴛ ʀᴇᴘʟʏ.**\n\n**ᴛʜᴀɴᴋ ʏᴏᴜ ᴘʟᴇᴀsᴇ ᴇɴɪᴏʏ.**"""
STICKER = [
        "CAACAgUAAx0Ccg5OnAACO7Zmsgyr0PLz9JWrMk3Qq_nMVGgGfAACIQoAAkCj8Fdxa8YvGPC9nx4E" , 
        "CAACAgUAAx0Ccg5OnAACO7lmsgy3AUQHAW7G05yl_rf6Pb469gACZQgAAj3k-Vfsu_WmA6PiUx4E" , 
        "CAACAgUAAx0Ccg5OnAACO7xmsgzKSD0pzxgH8KFGaSQ9zifkJgACBAgAAgz1-Fdx5iMD0Bh8mR4E" , 
        "CAACAgUAAx0Ccg5OnAACO79msgzapLLbvhL2GZUX1ZPAs3QnwgACbQcAAj5O-Vfacb2S2B5RQB4E" , 
        "CAACAgUAAx0Ccg5OnAACO8JmsgztO7-hwSVQUuxKdjMeSglEqwACsAYAAgMG-Vd0t6HAhNHB5x4E" , 
        "CAACAgUAAx0Ccg5OnAACO8Vmsgz9z6YrW7xWS2cE9UsdbZvvRAACIwkAAlmS8FcdZ3xHfo764h4E" ,
        "CAACAgUAAx0Ccg5OnAACO8hmsg0TIO_DQ4FdyyMmtvqIp5g4FgAC1wcAAjJP-Vdg1wymsgazNB4E" , 
        "CAACAgEAAx0Ccg5OnAACO85msg1m3fnsbowqLGzlVblcH-7XsQAC1AUAAklTqUQlhMqMLBaIzR4E" , 
        "CAACAgEAAx0Ccg5OnAACO9Fmsg2MKg4OyLYRS_m3HaAazbIfngACYQQAAoD4qER5uOGwdDS1Nh4E"
        ]


EMOJIOS = [
    "💣",
    "💥",
    "🪄",
    "🧨",
    "⚡",
    "🤡",
    "👻",
    "🎃",
    "🎩",
    "🕊",
]

BOT = "https://envs.sh/ahC.jpg"
IMG = [
    "https://telegra.ph/file/010c936d41e9da782780f.jpg",
    "https://telegra.ph/file/e17740f22da1fe4162e43.jpg",
    "https://telegra.ph/file/38ae0f7b919a8995c7f29.jpg",
    "https://telegra.ph/file/9fbc748ad0d552e403ba6.jpg",
    "https://telegra.ph/file/2433c1b98d2621623ead3.jpg",
    "https://telegra.ph/file/62f26ca46103beee9a0d5.jpg",
    "https://telegra.ph/file/d3e855bc548a1ce9649e7.jpg",
    "https://telegra.ph/file/b860df3e144c2208a7e5a.jpg",
    "https://telegra.ph/file/33591be403ae3eaae7217.jpg",
    "https://telegra.ph/file/a9d91437d795b0ae55af8.jpg",
    "https://telegra.ph/file/1891e318996f393e0aebc.jpg",
    "https://telegra.ph/file/84492c50c7a8a8d2603dc.jpg",
    "https://telegra.ph/file/ae843fb1e51218521e95b.jpg",
    "https://telegra.ph/file/0b98ff58d75e85438d3a0.jpg"
    ]



from ChampuChatBot import db

chatai = db.Word.WordDb
lang_db = db.ChatLangDb.LangCollection
status_db = db.ChatBotStatusDb.StatusCollection


async def bot_sys_stats():
    bot_uptime = int(time.time() - _boot_)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    UP = f"{get_readable_time((bot_uptime))}"
    CPU = f"{cpu}%"
    RAM = f"{mem}%"
    DISK = f"{disk}%"
    return UP, CPU, RAM, DISK
    

async def set_default_status(chat_id):
    try:
        if not await status_db.find_one({"chat_id": chat_id}):
            await status_db.insert_one({"chat_id": chat_id, "status": "enabled"})
    except Exception as e:
        print(f"Error setting default status for chat {chat_id}: {e}")


@ChampuChatBot.on_message(filters.new_chat_members)
async def welcomejej(client, message: Message):
    chat = message.chat
    await add_served_chat(message.chat.id)
    await set_default_status(message.chat.id)
    users = len(await get_served_users())
    chats = len(await get_served_chats())
    try:
        for member in message.new_chat_members:
            
            if member.id == ChampuChatBot.id:
                try:
                    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("sᴇʟᴇᴄᴛ ʟᴀɴɢᴜᴀɢᴇ", callback_data="choose_lang")]])    
                    await message.reply_text(text="**тнαикѕ ꜰᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴩ.**\n\n**ᴋɪɴᴅʟʏ  ꜱᴇʟᴇᴄᴛ  ʙᴏᴛ  ʟᴀɴɢᴜᴀɢᴇ  ꜰᴏʀ  ᴛʜɪꜱ  ɢʀᴏᴜᴩ  ʙʏ  ᴛʏᴩᴇ  ☞  /lang**", reply_markup=reply_markup)
                except Exception as e:
                    print(f"{e}")
                    pass
                try:
                    invitelink = await ChampuChatBot.export_chat_invite_link(message.chat.id)
                                                                        
                    link = f"[ɢᴇᴛ ʟɪɴᴋ]({invitelink})"
                except ChatAdminRequired:
                    link = "No Link"
                    
                try:
                    groups_photo = await ChampuChatBot.download_media(
                        chat.photo.big_file_id, file_name=f"chatpp{chat.id}.png"
                    )
                    chat_photo = (
                        groups_photo if groups_photo else "https://envs.sh/IL_.jpg"
                    )
                except AttributeError:
                    chat_photo = "https://envs.sh/IL_.jpg"
                except Exception as e:
                    pass

                count = await ChampuChatBot.get_chat_members_count(chat.id)
                chats = len(await get_served_chats())
                username = chat.username if chat.username else "𝐏ʀɪᴠᴀᴛᴇ 𝐆ʀᴏᴜᴘ"
                msg = (
                    f"**📝𝐁ᴏᴛ 𝐀ᴅᴅᴇᴅ 𝐈ɴ 𝐀 #𝐍ᴇᴡ_𝐆ʀᴏᴜᴘ**\n\n"
                    f"**📌𝐂ʜᴀᴛ 𝐍ᴀᴍᴇ:** {chat.title}\n"
                    f"**🍂𝐂ʜᴀᴛ 𝐈ᴅ:** `{chat.id}`\n"
                    f"**🔐𝐂ʜᴀᴛ 𝐔sᴇʀɴᴀᴍᴇ:** @{username}\n"
                    f"**🖇️𝐆ʀᴏᴜᴘ 𝐋ɪɴᴋ:** {link}\n"
                    f"**📈𝐆ʀᴏᴜᴘ 𝐌ᴇᴍʙᴇʀs:** {count}\n"
                    f"**🤔𝐀ᴅᴅᴇᴅ 𝐁ʏ:** {message.from_user.mention}\n\n"
                    f"**ᴛᴏᴛᴀʟ ᴄʜᴀᴛs :** {chats}"
                )

                try:
                    OWNER = config.OWNER_ID
                    if OWNER:
                        await ChampuChatBot.send_photo(
                            int(OWNER_ID),
                            photo=chat_photo,
                            caption=msg,
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{message.from_user.first_name}", user_id=message.from_user.id)]]))
                                
                    
                except Exception as e:
                    print(f"Please Provide me correct owner id for send logs")
                    await ChampuChatBot.send_photo(
                        int(OWNER_ID),
                        photo=chat_photo,
                        caption=msg,
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"{message.from_user.first_name}", user_id=message.from_user.id)]]))
    except Exception as e:
        print(f"Err: {e}")


from pathlib import Path
import os
import time
import io

@ChampuChatBot.on_cmd(["ls"])
async def ls(_, m: Message):
    "To list all files and folders."

    cat = "".join(m.text.split(maxsplit=1)[1:])
    path = cat or os.getcwd()
    if not os.path.exists(path):
        await m.reply_text(
            f"There is no such directory or file with the name `{cat}`. Check again."
        )
        return

    path = Path(cat) if cat else os.getcwd()
    if os.path.isdir(path):
        if cat:
            msg = f"Folders and Files in `{path}`:\n"
        else:
            msg = "Folders and Files in Current Directory:\n"
        lists = os.listdir(path)
        files = ""
        folders = ""
        for contents in sorted(lists):
            catpath = os.path.join(path, contents)
            if not os.path.isdir(catpath):
                size = os.stat(catpath).st_size
                if str(contents).endswith((".mp3", ".flac", ".wav", ".m4a")):
                    files += f"🎵`{contents}`\n"
                elif str(contents).endswith((".opus")):
                    files += f"🎙`{contents}`\n"
                elif str(contents).endswith((".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")):
                    files += f"🎞`{contents}`\n"
                elif str(contents).endswith((".zip", ".tar", ".tar.gz", ".rar")):
                    files += f"🗜`{contents}`\n"
                elif str(contents).endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico")):
                    files += f"🖼`{contents}`\n"
                else:
                    files += f"📄`{contents}`\n"
            else:
                folders += f"📁`{contents}`\n"
        msg = msg + folders + files if files or folders else f"{msg}__empty path__"
    else:
        size = os.stat(path).st_size
        msg = "The details of the given file:\n"
        if str(path).endswith((".mp3", ".flac", ".wav", ".m4a")):
            mode = "🎵"
        elif str(path).endswith((".opus")):
            mode = "🎙"
        elif str(path).endswith((".mkv", ".mp4", ".webm", ".avi", ".mov", ".flv")):
            mode = "🎞"
        elif str(path).endswith((".zip", ".tar", ".tar.gz", ".rar")):
            mode = "🗜"
        elif str(path).endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ico")):
            mode = "🖼"
        else:
            mode = "📄"
        time2 = time.ctime(os.path.getmtime(path))
        time3 = time.ctime(os.path.getatime(path))
        msg += f"**Location:** `{path}`\n"
        msg += f"**Icon:** `{mode}`\n"
        msg += f"**Size:** `{humanbytes(size)}`\n"
        msg += f"**Last Modified Time:** `{time2}`\n"
        msg += f"**Last Accessed Time:** `{time3}`"

    if len(msg) > 4096:
        with io.BytesIO(str.encode(msg)) as out_file:
            out_file.name = "ls.txt"
            await m.reply_document(
                out_file,
                caption=path,
            )
    else:
        await m.reply_text(msg)


@ChampuChatBot.on_cmd(["start", "aistart"])
async def start(_, m: Message):
    users = len(await get_served_users())
    chats = len(await get_served_chats())
    if m.chat.type == ChatType.PRIVATE:
        accha = await m.reply_text(
            text=random.choice(EMOJIOS),
        )
        await asyncio.sleep(0.5)
        
     
        await accha.edit("**__ꨄ︎ ѕ__**")
        await asyncio.sleep(0.01)
        await accha.edit("**__ꨄ sт__**")
        await asyncio.sleep(0.01)
        await accha.edit("**__ꨄ︎ ѕтα__**")
        await asyncio.sleep(0.01)
        await accha.edit("**__ꨄ︎ ѕтαя__**")
        await asyncio.sleep(0.01)
        await accha.edit("**__ꨄ sтαят__**")
        await asyncio.sleep(0.01)
        await accha.edit("**__ꨄ︎ sтαятι__**")
        await asyncio.sleep(0.01)
        await accha.edit("**__ꨄ︎ sтαятιи__**")
        await asyncio.sleep(0.01)
        await accha.edit("**__ꨄ sтαятιиg__**")
        await asyncio.sleep(0.01)
        await accha.edit("**__ꨄ︎ ѕтαятιиg.__**")
        await asyncio.sleep(0.1)
        await accha.edit("**__ꨄ sтαятιиg.....__**")
        await asyncio.sleep(0.1)
        await accha.edit("**__ꨄ︎ ѕтαятιиg.__**")
        await asyncio.sleep(0.1)
        await accha.edit("**__ꨄ sтαятιиg.....__**")
        await accha.delete()
        
        umm = await m.reply_sticker(sticker=random.choice(STICKER))
        chat_photo = BOT  
        if m.chat.photo:
            try:
                userss_photo = await ChampuChatBot.download_media(m.chat.photo.big_file_id)
                await umm.delete()
                if userss_photo:
                    chat_photo = userss_photo
            except AttributeError:
                chat_photo = BOT  

        users = len(await get_served_users())
        chats = len(await get_served_chats())
        UP, CPU, RAM, DISK = await bot_sys_stats()
        await m.reply_photo(photo=chat_photo, caption=START.format(ChampuChatBot.mention or "can't mention", users, chats, UP), reply_markup=InlineKeyboardMarkup(START_BOT))
        await add_served_user(m.chat.id)
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(f"{m.chat.first_name}", user_id=m.chat.id)]])
        await ChampuChatBot.send_photo(int(OWNER_ID), photo=chat_photo, caption=f"{m.from_user.mention} ʜᴀs sᴛᴀʀᴛᴇᴅ ʙᴏᴛ. \n\n**ɴᴀᴍᴇ :** {m.chat.first_name}\n**ᴜsᴇʀɴᴀᴍᴇ :** @{m.chat.username}\n**ɪᴅ :** {m.chat.id}\n\n**ᴛᴏᴛᴀʟ ᴜsᴇʀs :** {users}", reply_markup=keyboard)
        
    else:
        await m.reply_photo(
            photo=random.choice(IMG),
            caption=GSTART.format(m.from_user.mention or "can't mention"),
            reply_markup=InlineKeyboardMarkup(HELP_START),
        )
        await add_served_chat(m.chat.id)


@ChampuChatBot.on_cmd("help")
async def help(client: ChampuChatBot, m: Message):
    if m.chat.type == ChatType.PRIVATE:
        hmm = await m.reply_photo(
            photo=random.choice(IMG),
            caption=HELP_READ,
            reply_markup=InlineKeyboardMarkup(HELP_BTN),
        )

    else:
        await m.reply_photo(
            photo=random.choice(IMG),
            caption="**ʜᴇʏ, ᴘᴍ ᴍᴇ ғᴏʀ ʜᴇʟᴘ ᴄᴏᴍᴍᴀɴᴅs!**",
            reply_markup=InlineKeyboardMarkup(HELP_BUTN),
        )
        await add_served_chat(m.chat.id)


@ChampuChatBot.on_cmd("repo")
async def repo(_, m: Message):
    await m.reply_text(
        text=SOURCE_READ,
        reply_markup=InlineKeyboardMarkup(CLOSE_BTN),
        disable_web_page_preview=True,
    )



@ChampuChatBot.on_cmd("ping")
async def ping(_, message: Message):
    start = datetime.now()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    loda = await message.reply_photo(
        photo=random.choice(IMG),
        caption="ᴘɪɴɢɪɴɢ...",
    )

    ms = (datetime.now() - start).microseconds / 1000
    await loda.edit_text(
        text=f"нey вαву!!\n{ChampuChatBot.name} ᴄʜᴀᴛʙᴏᴛ ιѕ alιve  αnd worĸιng ғιne wιтн a pιng oғ\n\n**➥** `{ms}` ms\n**➲ ᴄᴘᴜ:** {CPU}\n**➲ ʀᴀᴍ:** {RAM}\n**➲ ᴅɪsᴋ:** {DISK}\n**➲ ᴜᴘᴛɪᴍᴇ »** {UP}\n\n<b>||** ⋆ʟᴏᴠᴇ ᴡɪᴛʜ⋆ [ʏᴏ ᴍʏsᴛᴇʀɪᴏᴜs ™](https://t.me/{OWNER_USERNAME}) **||</b>",
        reply_markup=InlineKeyboardMarkup(PNG_BTN),
    )
    if message.chat.type == ChatType.PRIVATE:
        await add_served_user(message.from_user.id)
    else:
        await add_served_chat(message.chat.id)


@ChampuChatBot.on_message(filters.command("stats"))
async def stats(cli: Client, message: Message):
    users = len(await get_served_users())
    chats = len(await get_served_chats())
    await message.reply_text(
        f"""{(await cli.get_me()).mention} ᴄʜᴀᴛʙᴏᴛ sᴛᴀᴛs:

➻ **ᴄʜᴀᴛs :** {chats}
➻ **ᴜsᴇʀs :** {users}"""
    )


from pyrogram.enums import ParseMode

from ChampuChatBot import ChampuChatBot


@ChampuChatBot.on_cmd("id")
async def getid(client, message):
    chat = message.chat
    your_id = message.from_user.id
    message_id = message.id
    reply = message.reply_to_message

    text = f"**[ᴍᴇssᴀɢᴇ ɪᴅ:]({message.link})** `{message_id}`\n"
    text += f"**[ʏᴏᴜʀ ɪᴅ:](tg://user?id={your_id})** `{your_id}`\n"

    if not message.command:
        message.command = message.text.split()

    if not message.command:
        message.command = message.text.split()

    if len(message.command) == 2:
        try:
            split = message.text.split(None, 1)[1].strip()
            user_id = (await client.get_users(split)).id
            text += f"**[ᴜsᴇʀ ɪᴅ:](tg://user?id={user_id})** `{user_id}`\n"

        except Exception:
            return await message.reply_text("ᴛʜɪs ᴜsᴇʀ ᴅᴏᴇsɴ'ᴛ ᴇxɪsᴛ.", quote=True)

    text += f"**[ᴄʜᴀᴛ ɪᴅ:](https://t.me/{chat.username})** `{chat.id}`\n\n"

    if (
        not getattr(reply, "empty", True)
        and not message.forward_from_chat
        and not reply.sender_chat
    ):
        text += f"**[ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ɪᴅ:]({reply.link})** `{reply.id}`\n"
        text += f"**[ʀᴇᴘʟɪᴇᴅ ᴜsᴇʀ ɪᴅ:](tg://user?id={reply.from_user.id})** `{reply.from_user.id}`\n\n"

    if reply and reply.forward_from_chat:
        text += f"ᴛʜᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴄʜᴀɴɴᴇʟ, {reply.forward_from_chat.title}, ʜᴀs ᴀɴ ɪᴅ ᴏғ `{reply.forward_from_chat.id}`\n\n"
        print(reply.forward_from_chat)

    if reply and reply.sender_chat:
        text += f"ɪᴅ ᴏғ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴄʜᴀᴛ/ᴄʜᴀɴɴᴇʟ, ɪs `{reply.sender_chat.id}`"
        print(reply.sender_chat)

    await message.reply_text(
        text,
        disable_web_page_preview=True,
        parse_mode=ParseMode.DEFAULT,
    )


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AUTO_SLEEP = 5
IS_BROADCASTING = False
broadcast_lock = asyncio.Lock()


@ChampuChatBot.on_message(
    filters.command(["broadcast", "gcast"]) & filters.user(int(OWNER_ID))
)
async def broadcast_message(client, message):
    global IS_BROADCASTING
    async with broadcast_lock:
        if IS_BROADCASTING:
            return await message.reply_text(
                "A broadcast is already in progress. Please wait for it to complete."
            )

        IS_BROADCASTING = True
        try:
            query = message.text.split(None, 1)[1].strip()
        except IndexError:
            query = message.text.strip()
        except Exception as eff:
            return await message.reply_text(
                f"**Error**: {eff}"
            )
        try:
            if message.reply_to_message:
                broadcast_content = message.reply_to_message
                broadcast_type = "reply"
                flags = {
                    "-pin": "-pin" in query,
                    "-pinloud": "-pinloud" in query,
                    "-nogroup": "-nogroup" in query,
                    "-user": "-user" in query,
                }
            else:
                if len(message.command) < 2:
                    return await message.reply_text(
                        "**Please provide text after the command or reply to a message for broadcasting.**"
                    )
                
                flags = {
                    "-pin": "-pin" in query,
                    "-pinloud": "-pinloud" in query,
                    "-nogroup": "-nogroup" in query,
                    "-user": "-user" in query,
                }

                for flag in flags:
                    query = query.replace(flag, "").strip()

                if not query:
                    return await message.reply_text(
                        "Please provide a valid text message or a flag: -pin, -nogroup, -pinloud, -user"
                    )

                
                broadcast_content = query
                broadcast_type = "text"
            

            await message.reply_text("**Started broadcasting...**")

            if not flags.get("-nogroup", False):
                sent = 0
                pin_count = 0
                chats = await get_served_chats()

                for chat in chats:
                    chat_id = int(chat["chat_id"])
                    if chat_id == message.chat.id:
                        continue
                    try:
                        if broadcast_type == "reply":
                            m = await ChampuChatBot.forward_messages(
                                chat_id, message.chat.id, [broadcast_content.id]
                            )
                        else:
                            m = await ChampuChatBot.send_message(
                                chat_id, text=broadcast_content
                            )
                        sent += 1

                        if flags.get("-pin", False) or flags.get("-pinloud", False):
                            try:
                                await m.pin(
                                    disable_notification=flags.get("-pin", False)
                                )
                                pin_count += 1
                            except Exception as e:
                                continue

                    except FloodWait as e:
                        flood_time = int(e.value)
                        logger.warning(
                            f"FloodWait of {flood_time} seconds encountered for chat {chat_id}."
                        )
                        if flood_time > 200:
                            logger.info(
                                f"Skipping chat {chat_id} due to excessive FloodWait."
                            )
                            continue
                        await asyncio.sleep(flood_time)
                    except Exception as e:
                        
                        continue

                await message.reply_text(
                    f"**Broadcasted to {sent} chats and pinned in {pin_count} chats.**"
                )

            if flags.get("-user", False):
                susr = 0
                users = await get_served_users()

                for user in users:
                    user_id = int(user["user_id"])
                    try:
                        if broadcast_type == "reply":
                            m = await ChampuChatBot.forward_messages(
                                user_id, message.chat.id, [broadcast_content.id]
                            )
                        else:
                            m = await ChampuChatBot.send_message(
                                user_id, text=broadcast_content
                            )
                        susr += 1

                    except FloodWait as e:
                        flood_time = int(e.value)
                        logger.warning(
                            f"FloodWait of {flood_time} seconds encountered for user {user_id}."
                        )
                        if flood_time > 200:
                            logger.info(
                                f"Skipping user {user_id} due to excessive FloodWait."
                            )
                            continue
                        await asyncio.sleep(flood_time)
                    except Exception as e:
                        
                        continue

                await message.reply_text(f"**Broadcasted to {susr} users.**")

        finally:
            IS_BROADCASTING = False


    
