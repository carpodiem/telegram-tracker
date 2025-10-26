from src.config import load_config, Config
import os


def test_load_config(monkeypatch):
    monkeypatch.setenv("API_ID", "12345")
    monkeypatch.setenv("API_HASH", "abcd")
    monkeypatch.setenv("MAKE_WEBHOOK_URL", "https://hook.us2.make.com/test")
    monkeypatch.setenv("CHANNELS", "@test1,@test2")
    monkeypatch.setenv("KEYWORDS_NEWS", "news,update")
    monkeypatch.setenv("CHECK_INTERVAL_HOURS", "6")

    cfg = load_config()
    assert isinstance(cfg, Config)
    assert cfg.api_id == 12345
    assert cfg.channels == ["@test1", "@test2"]
    assert "news" in cfg.keywords["news"]
