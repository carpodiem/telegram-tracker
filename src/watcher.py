# src/watcher.py
from telethon import TelegramClient
from telethon.tl.types import Message
from typing import List, Dict
import asyncio
import logging
from src.config import Config
from datetime import datetime, timedelta, timezone


logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] %(levelname)s: %(message)s")


class TelegramWatcher:
    """Handles reading messages from Telegram channels using Telethon."""

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.client = TelegramClient("session", cfg.api_id, cfg.api_hash)

    async def fetch_recent_messages(self, channel: str, hours: int = 8) -> List[Message]:
        """Fetch messages from a channel within the specified time window."""
        await self.client.connect()
        if not await self.client.is_user_authorized():
            raise RuntimeError(
                "Session not authorized. Run initial login first.")

        # Calculate the time threshold
        from datetime import datetime, timedelta, timezone
        time_threshold = datetime.now(timezone.utc) - timedelta(hours=hours)

        # Fetch messages until we go beyond the time threshold
        messages = []
        offset_id = 0
        batch_size = 100  # Process in batches of 100

        while True:
            batch = await self.client.get_messages(
                channel,
                limit=batch_size,
                offset_id=offset_id
            )

            if not batch:
                break

            # Filter messages within time window
            recent_messages = [
                msg for msg in batch if msg.date >= time_threshold]
            messages.extend(recent_messages)

            # If we found messages older than threshold, we can stop
            if any(msg.date < time_threshold for msg in batch):
                break

            # Update offset for next batch
            offset_id = batch[-1].id

        await self.client.disconnect()
        logging.info(
            f"Fetched {len(messages)} messages from {channel} within {hours} hours")
        return messages

    def filter_messages(self, messages: List[Message], keywords: List[str]) -> List[Dict]:
        """Filter messages by keywords only (time filtering is done in fetch_recent_messages)."""
        results = []

        for msg in messages:
            if not msg.message:
                continue

            text = (msg.message or msg.text or "").lower()
            if any(kw.lower() in text for kw in keywords):
                results.append({
                    "id": msg.id,
                    "text": msg.message,
                    "link": f"https://t.me/{msg.chat.username}/{msg.id}" if msg.chat else "",
                    "date": msg.date.isoformat(),
                })
        return results

    async def run(self):
        """Main polling loop."""
        logging.info("Starting Telegram watcher...")
        for channel in self.cfg.channels:
            messages = await self.fetch_recent_messages(channel, self.cfg.check_interval_hours)
            group_name = channel.replace("@", "")
            keywords = self.cfg.keywords.get(group_name, [])
            matches = self.filter_messages(messages, keywords)
            if matches:
                logging.info(f"Found {len(matches)} matches in {channel}")
            else:
                logging.info(f"No matches in {channel}")
