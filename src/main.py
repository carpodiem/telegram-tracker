# src/main.py
import asyncio
import logging
import time
from src.config import load_config
from src.watcher import TelegramWatcher
from src.sender import WebhookSender


logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] %(levelname)s: %(message)s")


async def main():
    """Main entrypoint — runs watcher, filters messages, sends matches."""
    cfg = load_config()
    watcher = TelegramWatcher(cfg)
    sender = WebhookSender(cfg)

    while True:
        logging.info("Starting new polling cycle...")
        for channel in cfg.channels:
            try:
                messages = await watcher.fetch_recent_messages(channel, cfg.check_interval_hours)
                group_key = channel.replace("@", "").lower()
                keywords = cfg.keywords.get(group_key, [])
                if not keywords:
                    logging.info(f"No keywords configured for {channel}")
                    continue

                logging.info(
                    f"Searching for keywords in {channel}: {keywords}")

                matches = watcher.filter_messages(messages, keywords)
                logging.info(
                    f"Found {len(matches)} messages with keywords in {channel}")
                for m in matches:
                    m["channel"] = channel
                sender.send(matches)
            except Exception as e:
                logging.error(f"Error while processing {channel}: {e}")

        logging.info(f"Sleeping for {cfg.check_interval_hours} hours...")
        await asyncio.sleep(cfg.check_interval_hours * 3600)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Watcher stopped by user.")
