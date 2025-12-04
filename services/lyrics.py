import requests

def get_lyrics(artist, title):
    url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
    r = requests.get(url)
    if r.status_code == 200:
        return r.json().get("lyrics")
    return None
