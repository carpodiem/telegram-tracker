from telethon import TelegramClient
from src.config import load_config

cfg = load_config()
client = TelegramClient("session", cfg.api_id, cfg.api_hash)

with client:
    print(">>> Sending login code to your Telegram account...")
    client.start()
    print(">>> Session initialized successfully.")
