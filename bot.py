import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from services.lastfm import search_track, get_artist_info
from services.lyrics import get_lyrics
from services.db import init_db, add_favorite, list_favorites

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Ошибка: TELEGRAM_TOKEN не найден в .env файле!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.reply(
        "🎵 Привет! Я MusicBot — твой помощник в мире музыки.\n\n"
        "Вот что я умею:\n"
        "🔍 /search <название песни>\n"
        "👤 /artist <имя исполнителя>\n"
        "⭐ /fav add <название трека|исполнитель> — добавить в избранное\n"
        "📂 /fav list — показать избранное\n"
    )

@dp.message(F.text.startswith("/search"))
async def cmd_search(message: Message):
    query = message.text.replace("/search", "").strip()
    if not query:
        return await message.reply("❗ Укажи название песни: `/search Shape of You`")
    
    results = await search_track(query)
    if not results:
        return await message.reply("😔 Ничего не найдено.")

    text = "🎶 Найдено:\n\n"
    for r in results[:5]:
        text += f"ID: `{r['id']}`\n🎧 {r['title']} — {r['artist']}\n\n"
    await message.reply(text, parse_mode="Markdown")

@dp.message(F.text.startswith("/artist"))
async def cmd_artist(message: Message):
    artist = message.text.replace("/artist", "").strip()
    if not artist:
        return await message.reply("❗ Укажи имя исполнителя: `/artist Eminem`")
    
    info = await get_artist_info(artist)
    await message.reply(info)

@dp.message(F.text.startswith("/fav"))
async def cmd_fav(message: Message):
    args = message.text.split()
    if len(args) < 2:
        return await message.reply("📝 Используй: `/fav add <название трека|исполнитель>` или `/fav list`")

    if args[1] == "add":
        track_id = message.text.partition("add")[2].strip()
        if not track_id:
            return await message.reply("❗ Укажи ID трека: `/fav add название трека|исполнитель`")
        if "|" not in track_id:
            return await message.reply("❗ ID должен содержать '|' для разделения названия и исполнителя, например: /fav add Shape of You|Ed Sheeran")

        title, artist = [part.strip() for part in track_id.split("|", 1)]

        await add_favorite(track_id, title, artist)
        await message.reply(f"⭐ Трек '{title}' — '{artist}' добавлен в избранное.")

    elif args[1] == "list":
        rows = await list_favorites()
        if not rows:
            return await message.reply("📂 Избранных треков нет.")
        text = "📂 Избранные треки:\n\n"
        for r in rows:
            text += f"ID: {r[0]}, {r[1]} — {r[2]}\n"
        await message.reply(text)

async def main():
    await init_db()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
