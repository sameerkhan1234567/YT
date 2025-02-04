from telethon import TelegramClient, events
import asyncio
import aria2p
import os
import aiofiles
from config import "API_ID" "29755489", "API_HASH" "05e0d957751c827aa03494f503ab54fe", PHONE_NUMBER, ARIA2_RPC_URL

# Telegram Client सेट करें
client = TelegramClient("session_name", API_ID, API_HASH)

# Aria2 Client सेट करें
aria2 = aria2p.Client(host="http://localhost", port=8000, secret="")

async def main():
    await client.start(PHONE_NUMBER)
    print("Bot Started...")

# जब कोई TXT फ़ाइल प्राप्त हो, तो उसे तेज़ी से डाउनलोड करें
@client.on(events.NewMessage)
async def handler(event):
    if event.file and event.file.name.endswith('.txt'):
        file_path = await event.download_media(file="temp.txt")
        print(f"Downloaded: {file_path}")

        # Multi-threading और Aria2 से डाउनलोड करें
        async with aiofiles.open(file_path, "r") as file:
            urls = await file.readlines()

        for url in urls:
            url = url.strip()
            if url:
                print(f"Downloading: {url}")
                aria2.add_uris([url])

# क्लाइंट रन करें
with client:
    client.loop.run_until_complete(main())
    client.run_until_disconnected()