# src/sender.py
import logging
import requests
from typing import List, Dict
from src.config import Config


class WebhookSender:
    """Sends matched Telegram messages to the Make Webhook."""

    def __init__(self, cfg: Config):
        self.cfg = cfg

    def send(self, messages: List[Dict]) -> None:
        """Send a batch of messages to Make webhook."""
        if not messages:
            logging.info("No messages to send.")
            return

        for msg in messages:
            payload = {
                "channel": msg.get("channel", ""),
                "id": msg.get("id", ""),
                "text": msg.get("text", ""),
                "link": msg.get("link", ""),
            }

            try:
                response = requests.post(
                    self.cfg.make_webhook_url, json=payload, timeout=10)
                response.raise_for_status()
                logging.info(
                    f"Sent message {msg.get('id')} from {msg.get('channel')}")
            except requests.RequestException as e:
                logging.error(f"Failed to send message {msg.get('id')}: {e}")
                # Continue processing other messages even if one fails
