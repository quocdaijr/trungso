"""JSONL persistence with an append-only guard on prophecies.

The guard is the integrity of this whole project: a prophecy may only be written
for a draw that has not happened yet, and may never be overwritten. Without that,
the scoreboard is just a number the oracle gets to choose.
"""

from __future__ import annotations

import json
import os
from collections.abc import Iterable, Iterator, Sequence
from pathlib import Path
from typing import TYPE_CHECKING

from .models import Draw, Prophecy

if TYPE_CHECKING:  # pragma: no cover
    from .sources.xsmb import XsmbDraw

ENV_DATA_DIR = "TRUNGSO_DATA_DIR"


class ProphecyConflict(RuntimeError):
    """Raised when a prophecy would overwrite history or predict a settled draw."""


def data_dir() -> Path:
    """Where data lives. Overridable via TRUNGSO_DATA_DIR so tests never touch the repo."""
    override = os.environ.get(ENV_DATA_DIR)
    if override:
        return Path(override)
    return Path(__file__).resolve().parents[2] / "data"


def draws_path(game: str) -> Path:
    return data_dir() / "draws" / f"{game}.jsonl"


def predictions_path() -> Path:
    return data_dir() / "predictions.jsonl"


def scoreboard_path() -> Path:
    return data_dir() / "scoreboard.json"


def _read_jsonl(path: Path) -> Iterator[dict]:
    if not path.exists():
        return
    with path.open(encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, start=1):
            text = line.strip()
            if not text:
                continue
            try:
                yield json.loads(text)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{lineno} is not valid JSON: {exc}") from exc


def _write_atomic(path: Path, payload: str) -> None:
    """Write via temp file + rename so an interrupted run never truncates data."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(payload, encoding="utf-8")
    tmp.replace(path)


def read_draws(game: str) -> tuple[Draw, ...]:
    """All stored draws for a game, sorted by draw_id."""
    draws = tuple(Draw.from_dict(row) for row in _read_jsonl(draws_path(game)))
    return tuple(sorted(draws, key=lambda d: d.draw_id))


def write_draws(game: str, draws: Sequence[Draw]) -> int:
    """Replace the stored draws for a game. Returns how many rows were written."""
    wrong = {d.game for d in draws} - {game}
    if wrong:
        raise ValueError(f"refusing to write {sorted(wrong)} draws into {game}.jsonl")
    ordered = sorted(draws, key=lambda d: d.draw_id)
    ids = [d.draw_id for d in ordered]
    if len(set(ids)) != len(ids):
        raise ValueError(f"duplicate draw_ids for {game}: cannot write")
    body = "".join(json.dumps(d.to_dict(), ensure_ascii=False) + "\n" for d in ordered)
    _write_atomic(draws_path(game), body)
    return len(ordered)


def merge_draws(game: str, incoming: Iterable[Draw]) -> tuple[int, int]:
    """Merge new draws into storage without disturbing existing rows.

    Returns (added, total). Existing draws win on conflict: history is never rewritten
    silently, because a changed past result would silently rewrite the scoreboard too.
    """
    existing = {d.draw_id: d for d in read_draws(game)}
    added = 0
    for draw in incoming:
        if draw.game != game:
            raise ValueError(f"draw {draw.draw_id} is {draw.game}, expected {game}")
        if draw.draw_id not in existing:
            existing[draw.draw_id] = draw
            added += 1
    total = write_draws(game, tuple(existing.values()))
    return added, total


def read_prophecies(game: str | None = None) -> tuple[Prophecy, ...]:
    """All prophecies, optionally filtered to one game, sorted by (game, draw_id)."""
    rows = (Prophecy.from_dict(row) for row in _read_jsonl(predictions_path()))
    items = tuple(p for p in rows if game is None or p.game == game)
    return tuple(sorted(items, key=lambda p: (p.game, p.draw_id)))


def append_prophecy(prophecy: Prophecy) -> None:
    """Append a prophecy, refusing anything that would compromise the audit trail."""
    for existing in read_prophecies(prophecy.game):
        if existing.draw_id == prophecy.draw_id:
            raise ProphecyConflict(
                f"a prophecy for {prophecy.game} draw {prophecy.draw_id} already exists "
                f"(seed {existing.seed[:12]}...). Prophecies are append-only."
            )

    settled = {d.draw_id for d in read_draws(prophecy.game)}
    if prophecy.draw_id in settled:
        raise ProphecyConflict(
            f"{prophecy.game} draw {prophecy.draw_id} has already been drawn. "
            "Prophesying a settled draw is cheating."
        )

    path = predictions_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(prophecy.to_dict(), ensure_ascii=False) + "\n")


def write_scoreboard(payload: dict) -> None:
    _write_atomic(scoreboard_path(), json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def read_scoreboard() -> dict | None:
    path = scoreboard_path()
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def xsmb_path() -> Path:
    return data_dir() / "xsmb.jsonl"


def read_xsmb() -> tuple[XsmbDraw, ...]:
    """Stored XSMB draws, oldest first."""
    from .sources.xsmb import XsmbDraw

    draws = tuple(XsmbDraw.from_dict(row) for row in _read_jsonl(xsmb_path()))
    return tuple(sorted(draws, key=lambda d: d.date))


def write_xsmb(draws: Sequence[XsmbDraw]) -> int:
    """Replace stored XSMB history. Identity is the date, so duplicates are a bug."""
    ordered = sorted(draws, key=lambda d: d.date)
    dates = [d.date for d in ordered]
    if len(set(dates)) != len(dates):
        raise ValueError("duplicate XSMB dates: cannot write")
    body = "".join(json.dumps(d.to_dict(), ensure_ascii=False) + "\n" for d in ordered)
    _write_atomic(xsmb_path(), body)
    return len(ordered)


def latest_xsmb_special() -> int | None:
    """The most recent XSMB special prize, or None when no history is stored.

    Read lazily by the oracle so a missing XSMB file degrades to a silent signal
    rather than breaking the run.
    """
    from .sources.xsmb import latest_special

    return latest_special(read_xsmb())
