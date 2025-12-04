import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("LASTFM_API_KEY")
API_URL = "http://ws.audioscrobbler.com/2.0/"

async def search_track(query, limit=5):
    params = {
        "method": "track.search",
        "track": query,
        "api_key": API_KEY,
        "format": "json",
        "limit": limit
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, params=params) as resp:
            response = await resp.json()
    tracks = response.get("results", {}).get("trackmatches", {}).get("track", [])
    
    results = []
    for t in tracks:
        results.append({
            "title": t.get("name"),
            "artist": t.get("artist"),
            "id": f"{t.get('name')}|{t.get('artist')}"
        })
    return results


async def get_artist_info(artist):
    params = {
        "method": "artist.getinfo",
        "artist": artist,
        "api_key": API_KEY,
        "format": "json"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, params=params) as resp:
            response = await resp.json()

    if "error" in response:
        return "😔 Исполнитель не найден."

    artist_info = response.get("artist", {})
    bio = artist_info.get("bio", {}).get("summary", "Нет описания.")
    tags = [tag["name"] for tag in artist_info.get("tags", {}).get("tag", [])]

    text = f"👤 *{artist_info.get('name', 'Unknown Artist')}*\n"
    text += f"📌 Жанры: {', '.join(tags) if tags else 'Неизвестно'}\n"
    text += f"📄 Описание:\n{bio}"
    
    return text
