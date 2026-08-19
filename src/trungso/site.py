"""Builds the single JSON bundle the static site reads.

Why a bundle instead of fetching data/ directly: GitHub Pages serves one directory, and
the raw history is megabytes of JSONL the browser has no use for. This writes exactly
what the page renders - and nothing else - next to the HTML, so the site is
self-contained and loads in one request.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from . import astrology, scoreboard, stats, store, wheel
from .games import PROPHECY_GAMES, GameSpec
from .models import Draw, Prophecy, utc_now
from .sources import xsmb

SITE_DIR = Path(__file__).resolve().parents[2] / "site"
BUNDLE_NAME = "data.json"
RECENT_DRAWS = 12
TOP_N = 8
# Starts a year before the earliest supported birth year: someone born in January
# before Tết belongs to the PREVIOUS lunar year, so that year's row must exist too.
EARLIEST_BIRTH_YEAR = 1930
LUNAR_TABLE_START = EARLIEST_BIRTH_YEAR - 1
LUNAR_TABLE_END = 2035

DISCLAIMER = (
    "Xổ số là biến cố độc lập. Mỗi kỳ quay reset về 0. Không có số nóng, không có số "
    "lạnh. Phần mềm này không dự đoán được gì — nó chỉ tự tin quá mức và tự chấm điểm "
    "độ sai của chính mình. Bảng Phong Thần là paper-trading: tiền đốt trên giấy."
)


def _game_payload(
    spec: GameSpec,
    draws: Sequence[Draw],
    prophecies: Sequence[Prophecy],
    score: scoreboard.GameScore,
) -> dict[str, Any]:
    chi = stats.chi_square_uniform(draws, spec) if draws else None
    frequencies = stats.frequency(draws, spec) if draws else {}
    settled = {d.draw_id for d in draws}
    pending = [p for p in prophecies if p.game == spec.key and p.draw_id not in settled]

    return {
        "key": spec.key,
        "display": spec.display,
        "pool": spec.pool,
        "pick": spec.pick,
        "has_bonus": spec.has_bonus,
        "wheel": {
            "combinations": wheel.total_combinations(spec),
            "cost_vnd": wheel.wheel_cost_vnd(spec),
            "expected_roi": round(wheel.expected_roi(spec), 6),
            "expected_roi_excluding_jackpot": round(
                wheel.expected_roi(spec, include_jackpot=False), 6
            ),
        },
        "draw_count": len(draws),
        "latest": draws[-1].to_dict() if draws else None,
        "recent": [d.to_dict() for d in draws[-RECENT_DRAWS:]],
        "frequency": {str(n): c for n, c in frequencies.items()},
        "chi_square": (
            {
                "statistic": round(chi.statistic, 3),
                "degrees_of_freedom": chi.degrees_of_freedom,
                "p_value": round(chi.p_value, 4),
                "observations": chi.observations,
                "rejects_uniform": chi.rejects_uniform,
                "verdict": stats.verdict(chi),
            }
            if chi
            else None
        ),
        "pending_prophecy": pending[0].to_dict() if pending else None,
        "score": score.to_dict(),
    }


def _xsmb_payload() -> dict[str, Any] | None:
    draws = store.read_xsmb()
    if not draws:
        return None
    chi = xsmb.chi_square_uniform(draws)
    frequencies = xsmb.frequency(draws)
    report = xsmb.summarise(draws)
    return {
        "display": "XSMB Miền Bắc",
        "draw_count": len(draws),
        "first_date": report["first_date"],
        "last_date": report["last_date"],
        "frequency": {f"{n:02d}": c for n, c in frequencies.items()},
        "chi_square": {
            "statistic": round(chi.statistic, 3),
            "degrees_of_freedom": chi.degrees_of_freedom,
            "p_value": round(chi.p_value, 4),
            "observations": chi.observations,
            "rejects_uniform": chi.rejects_uniform,
            "verdict": stats.verdict(chi),
        },
    }


def _astrology_payload() -> dict[str, Any]:
    """Every constant and table the browser needs to read a fortune.

    The browser gets DATA, not a second implementation: the lunar algorithm, the
    sexagenary cycle and the nạp âm table are all resolved here in Python and shipped
    as a lookup, so a birth date can be placed in its lunar year with one date
    comparison. That keeps the two sides from drifting apart, and keeps the birth date
    itself on the device.
    """
    table = astrology.lunar_year_table(LUNAR_TABLE_START, LUNAR_TABLE_END)
    return {
        "lunar_years": {str(year): entry for year, entry in table.items()},
        "zodiac_bounds": [
            {"month": month, "day": day, "name": name}
            for month, day, name in astrology.ZODIAC_BOUNDS
        ],
        "stars_male": list(astrology.STARS_MALE),
        "stars_female": list(astrology.STARS_FEMALE),
        "star_base_age": astrology.STAR_BASE_AGE,
        "tam_hop": [list(group) for group in astrology.TAM_HOP],
        "tu_hanh_xung": [list(group) for group in astrology.TU_HANH_XUNG],
        "pythagorean_rows": list(astrology.PYTHAGOREAN_ROWS),
        "master_numbers": list(astrology.MASTER_NUMBERS),
        "elements": list(astrology.ELEMENTS),
    }


def build_bundle() -> dict[str, Any]:
    """Assemble everything the page needs from stored data."""
    prophecies = store.read_prophecies()
    games = []
    for spec in PROPHECY_GAMES.values():
        draws = store.read_draws(spec.key)
        score = scoreboard.build(spec, prophecies, draws)
        games.append(_game_payload(spec, draws, prophecies, score))

    return {
        "generated_at": utc_now().isoformat(),
        "disclaimer": DISCLAIMER,
        "games": games,
        "xsmb": _xsmb_payload(),
        "top_n": TOP_N,
        "astrology": _astrology_payload(),
        "privacy": (
            "Ngày sinh, tên và giới tính chỉ nằm trong trình duyệt của bạn "
            "(localStorage). Không có server, không có tài khoản, không request nào "
            "mang dữ liệu đó đi. Xoá lúc nào cũng được."
        ),
    }


def write_bundle(bundle: Mapping[str, Any], *, site_dir: Path | None = None) -> Path:
    import json

    target = (site_dir or SITE_DIR) / BUNDLE_NAME
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(bundle, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    tmp.replace(target)
    return target
