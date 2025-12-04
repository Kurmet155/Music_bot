import aiosqlite

DB = "favorites.db"

async def init_db():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS favs(id TEXT PRIMARY KEY, title TEXT, artist TEXT)""")
        await db.commit()

async def add_favorite(track_id, title, artist):
    async with aiosqlite.connect(DB) as db:
        await db.execute("INSERT OR REPLACE INTO favs(id,title,artist) VALUES (?,?,?)", (track_id,title,artist))
        await db.commit()

async def list_favorites():
    async with aiosqlite.connect(DB) as db:
        cursor = await db.execute("SELECT id,title,artist FROM favs")
        rows = await cursor.fetchall()
        return rows
