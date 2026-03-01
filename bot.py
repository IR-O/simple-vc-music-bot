import asyncio
import yt_dlp

from pyrogram import Client, filters, idle
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio

from config import API_ID, API_HASH, BOT_TOKEN, STRING_SESSION

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

assistant = Client(
    STRING_SESSION,
    api_id=API_ID,
    api_hash=API_HASH
)

call = PyTgCalls(assistant)


def yt_audio(query):
    ydl_opts = {"format": "bestaudio", "quiet": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)["entries"][0]
        return info["url"], info["title"]


@bot.on_message(filters.command("play") & filters.group)
async def play(_, message: Message):

    if len(message.command) < 2:
        return await message.reply("❌ Give song name")

    query = message.text.split(None, 1)[1]
    await message.reply("🔎 Searching...")

    url, title = yt_audio(query)

    chat_id = message.chat.id

    try:
        await call.join_group_call(chat_id, AudioPiped(url, HighQualityAudio()))
    except:
        await call.leave_group_call(chat_id)
        await call.join_group_call(chat_id, AudioPiped(url, HighQualityAudio()))

    await message.reply(f"🎵 Playing: **{title}**")


@bot.on_message(filters.command("stop") & filters.group)
async def stop(_, message: Message):
    await call.leave_group_call(message.chat.id)
    await message.reply("⏹ Stopped")


async def main():
    await bot.start()
    await assistant.start()
    await call.start()
    print("✅ Music Bot Started")
    await idle()

asyncio.run(main())
