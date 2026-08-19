"""Telegram delivery. Never allowed to break the data pipeline.

Every function here swallows its own failures and reports them as a return value. A
dead Telegram API must not cost us an ingest, a prophecy or a scoreboard update - the
data is the product, the notification is a convenience.
"""

from __future__ import annotations

import os
from collections.abc import Sequence

import requests

from .games import GameSpec
from .models import Draw, Prophecy
from .scoreboard import GameScore, ScoreRow

API_TEMPLATE = "https://api.telegram.org/bot{token}/sendMessage"
ENV_TOKEN = "TELEGRAM_BOT_TOKEN"
ENV_CHAT_ID = "TELEGRAM_CHAT_ID"
SEND_TIMEOUT = 15
MAX_MESSAGE_CHARS = 4096

DISCLAIMER = "Xổ số là biến cố độc lập. Đây là giải trí, không phải dự đoán. Paper-trading."


class TelegramNotConfigured(RuntimeError):
    """Raised only by `require_config`, for commands that must fail loudly."""


def read_config() -> tuple[str, str] | None:
    """Bot token and chat id from the environment, or None if either is absent."""
    token = os.environ.get(ENV_TOKEN, "").strip()
    chat_id = os.environ.get(ENV_CHAT_ID, "").strip()
    if not token or not chat_id:
        return None
    return token, chat_id


def require_config() -> tuple[str, str]:
    config = read_config()
    if config is None:
        raise TelegramNotConfigured(
            f"cần cả {ENV_TOKEN} và {ENV_CHAT_ID} trong môi trường "
            "(GitHub Secrets khi chạy trên Actions)"
        )
    return config


def send_message(text: str, *, timeout: int = SEND_TIMEOUT) -> bool:
    """Send one message. Returns whether it went out; never raises."""
    config = read_config()
    if config is None:
        return False
    token, chat_id = config
    try:
        response = requests.post(
            API_TEMPLATE.format(token=token),
            json={
                "chat_id": chat_id,
                "text": text[:MAX_MESSAGE_CHARS],
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
            },
            timeout=timeout,
        )
        response.raise_for_status()
        return bool(response.json().get("ok"))
    except (requests.RequestException, ValueError):
        return False


def format_prophecy(spec: GameSpec, prophecy: Prophecy, score: GameScore | None = None) -> str:
    """The pre-draw message: the numbers, the excuses, and the running humiliation."""
    numbers = "  ".join(f"<b>{n:02d}</b>" for n in prophecy.numbers)
    lines = [
        f"🔮 <b>{spec.display}</b> — kỳ #{prophecy.draw_id}",
        f"Quay {prophecy.draw_date.strftime('%d/%m/%Y')} lúc 18h00",
        "",
        numbers,
        "",
    ]
    # A prophecy stored before sermons existed has none. Degrade to just the numbers
    # rather than crashing on a lookup.
    sermons = [
        f"• <b>{n:02d}</b> — {prophecy.sermon[str(n)]}"
        for n in prophecy.numbers
        if prophecy.sermon.get(str(n))
    ]
    if sermons:
        lines += ["<i>Lời sấm:</i>", *sermons]

    if score and score.draws_scored:
        lines += [
            "",
            f"📉 Thành tích tới giờ: {score.draws_scored} kỳ, "
            f"trúng {score.hits_per_draw_actual:.2f}/kỳ "
            f"(ngẫu nhiên: {score.hits_per_draw_expected:.2f})",
            f"ROI: {score.roi * 100:.1f}% · bỏ jackpot: {score.roi_excluding_jackpot * 100:.1f}%",
        ]

    lines += ["", f"<i>{DISCLAIMER}</i>"]
    return "\n".join(lines)


def format_result(
    spec: GameSpec, draw: Draw, row: ScoreRow, score: GameScore | None = None
) -> str:
    """The post-draw message: what actually came out, and how badly we did."""
    actual = " ".join(f"<b>{n:02d}</b>" for n in draw.main)
    bonus = f" | phụ <b>{draw.bonus:02d}</b>" if draw.bonus is not None else ""
    expected = spec.expected_hits()
    verdict = "may hơn ngẫu nhiên 🍀" if row.hits > expected else "tệ hơn cả ngẫu nhiên 💀"

    lines = [
        f"🎲 <b>{spec.display}</b> — kết quả kỳ #{draw.draw_id}",
        f"{actual}{bonus}",
        "",
        f"Tiên tri trúng <b>{row.hits}/12</b> số "
        f"(kỳ vọng ngẫu nhiên {expected:.2f}) — {verdict}",
    ]
    won = row.prize_counts
    if row.payout_vnd:
        tiers = ", ".join(f"{n}× {tier}" for tier, n in won.items() if n)
        lines.append(f"Thắng (giấy): {row.payout_vnd:,}đ trên {row.cost_vnd:,}đ — {tiers}")
    else:
        lines.append(f"Thắng (giấy): 0đ trên {row.cost_vnd:,}đ đã đốt")

    if score and score.draws_scored:
        lines += [
            "",
            f"📉 Cộng dồn: ROI {score.roi * 100:.1f}% · "
            f"bỏ jackpot {score.roi_excluding_jackpot * 100:.1f}%",
        ]

    lines += ["", f"<i>{DISCLAIMER}</i>"]
    return "\n".join(lines)


def pending_prophecies(
    prophecies: Sequence[Prophecy], draws: Sequence[Draw]
) -> tuple[Prophecy, ...]:
    """Prophecies whose draw has not happened yet - the ones worth announcing."""
    settled = {d.draw_id for d in draws}
    return tuple(p for p in prophecies if p.draw_id not in settled)
