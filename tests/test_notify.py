"""Telegram delivery. The contract that matters: it can fail without breaking anything."""

from __future__ import annotations

import pytest

from conftest import make_draw, make_prophecy
from trungso import notify, scoreboard
from trungso.games import MEGA645, POWER655


@pytest.fixture(autouse=True)
def no_telegram_env(monkeypatch):
    monkeypatch.delenv(notify.ENV_TOKEN, raising=False)
    monkeypatch.delenv(notify.ENV_CHAT_ID, raising=False)


def test_unconfigured_send_returns_false_without_network():
    """No token, no request, no exception - just a False."""
    assert notify.send_message("xin chào") is False


@pytest.mark.parametrize(
    "token,chat", [("", "123"), ("abc", ""), ("", ""), ("   ", "123")]
)
def test_partial_config_is_treated_as_unconfigured(monkeypatch, token, chat):
    monkeypatch.setenv(notify.ENV_TOKEN, token)
    monkeypatch.setenv(notify.ENV_CHAT_ID, chat)
    assert notify.read_config() is None
    assert notify.send_message("x") is False


def test_full_config_is_read(monkeypatch):
    monkeypatch.setenv(notify.ENV_TOKEN, "tok")
    monkeypatch.setenv(notify.ENV_CHAT_ID, "42")
    assert notify.read_config() == ("tok", "42")


def test_require_config_raises_when_absent():
    with pytest.raises(notify.TelegramNotConfigured, match="TELEGRAM_BOT_TOKEN"):
        notify.require_config()


def test_send_swallows_network_errors(monkeypatch):
    """A dead Telegram must never propagate into the pipeline."""
    import requests

    monkeypatch.setenv(notify.ENV_TOKEN, "tok")
    monkeypatch.setenv(notify.ENV_CHAT_ID, "42")

    def boom(*args, **kwargs):
        raise requests.ConnectionError("telegram is down")

    monkeypatch.setattr(requests, "post", boom)
    assert notify.send_message("x") is False


def test_send_returns_false_on_api_not_ok(monkeypatch):
    import requests

    monkeypatch.setenv(notify.ENV_TOKEN, "tok")
    monkeypatch.setenv(notify.ENV_CHAT_ID, "42")

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"ok": False, "description": "chat not found"}

    monkeypatch.setattr(requests, "post", lambda *a, **k: FakeResponse())
    assert notify.send_message("x") is False


def test_message_is_truncated_to_telegram_limit(monkeypatch):
    import requests

    monkeypatch.setenv(notify.ENV_TOKEN, "tok")
    monkeypatch.setenv(notify.ENV_CHAT_ID, "42")
    captured = {}

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"ok": True}

    def capture(url, json, timeout):
        captured.update(json)
        return FakeResponse()

    monkeypatch.setattr(requests, "post", capture)
    assert notify.send_message("x" * 9000) is True
    assert len(captured["text"]) == notify.MAX_MESSAGE_CHARS


def test_prophecy_message_carries_numbers_and_disclaimer():
    prophecy = make_prophecy(MEGA645, 1551, numbers=tuple(range(1, 13)))
    text = notify.format_prophecy(MEGA645, prophecy)

    assert "Mega 6/45" in text
    assert "01551" in text
    assert "<b>07</b>" in text
    assert "biến cố độc lập" in text


def test_prophecy_message_includes_running_roi_when_scored():
    prophecies = [make_prophecy(MEGA645, i, numbers=tuple(range(1, 13))) for i in (1, 2)]
    draws = [make_draw(MEGA645, 1, main=(1, 2, 3, 40, 41, 42))]
    score = scoreboard.build(MEGA645, prophecies, draws)

    text = notify.format_prophecy(MEGA645, prophecies[1], score)
    assert "ROI" in text
    assert "bỏ jackpot" in text


def test_result_message_reports_hits_against_chance():
    prophecy = make_prophecy(POWER655, 1, numbers=tuple(range(1, 13)))
    draw = make_draw(POWER655, 1, main=(1, 2, 3, 50, 51, 52), bonus=55)
    row = scoreboard.score_one(POWER655, prophecy, draw)

    text = notify.format_result(POWER655, draw, row)
    assert "3/12" in text
    assert "Power 6/55" in text
    assert "phụ <b>55</b>" in text
    assert "biến cố độc lập" in text


def test_result_message_says_zero_when_nothing_won():
    prophecy = make_prophecy(MEGA645, 1, numbers=tuple(range(1, 13)))
    draw = make_draw(MEGA645, 1, main=(20, 21, 22, 23, 24, 25))
    row = scoreboard.score_one(MEGA645, prophecy, draw)

    text = notify.format_result(MEGA645, draw, row)
    assert "0đ trên" in text
    assert "💀" in text


def test_pending_prophecies_excludes_settled_draws():
    prophecies = [make_prophecy(MEGA645, i) for i in (1, 2, 3)]
    draws = [make_draw(MEGA645, 1), make_draw(MEGA645, 2)]

    pending = notify.pending_prophecies(prophecies, draws)
    assert [p.draw_id for p in pending] == ["00003"]
