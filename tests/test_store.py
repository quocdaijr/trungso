"""The append-only guard. This is what makes the scoreboard trustworthy."""

from __future__ import annotations

import pytest

from conftest import make_draw, make_prophecy
from trungso import store
from trungso.games import MEGA645, POWER655


def test_reading_missing_files_returns_empty():
    assert store.read_draws("mega645") == ()
    assert store.read_prophecies() == ()
    assert store.read_scoreboard() is None


def test_draws_round_trip():
    draws = [make_draw(MEGA645, i) for i in (3, 1, 2)]
    written = store.write_draws("mega645", draws)

    loaded = store.read_draws("mega645")
    assert written == 3
    assert [d.draw_id for d in loaded] == ["00001", "00002", "00003"]
    assert loaded[0].main == draws[0].main


def test_power655_bonus_survives_round_trip():
    original = make_draw(POWER655, 1386, main=(3, 15, 18, 38, 41, 48), bonus=30)
    store.write_draws("power655", [original])

    assert store.read_draws("power655")[0].bonus == 30


def test_write_draws_rejects_foreign_game():
    with pytest.raises(ValueError, match="refusing to write"):
        store.write_draws("mega645", [make_draw(POWER655, 1)])


def test_write_draws_rejects_duplicate_ids():
    duplicate = [make_draw(MEGA645, 1), make_draw(MEGA645, 1)]
    with pytest.raises(ValueError, match="duplicate draw_ids"):
        store.write_draws("mega645", duplicate)


def test_merge_draws_adds_only_new_rows():
    store.write_draws("mega645", [make_draw(MEGA645, 1)])
    added, total = store.merge_draws("mega645", [make_draw(MEGA645, 1), make_draw(MEGA645, 2)])

    assert (added, total) == (1, 2)


def test_merge_draws_never_rewrites_history():
    """A changed past result would silently rewrite the scoreboard - so it cannot happen."""
    original = make_draw(MEGA645, 1, main=(1, 2, 3, 4, 5, 6))
    store.write_draws("mega645", [original])

    tampered = make_draw(MEGA645, 1, main=(7, 8, 9, 10, 11, 12))
    added, _ = store.merge_draws("mega645", [tampered])

    assert added == 0
    assert store.read_draws("mega645")[0].main == (1, 2, 3, 4, 5, 6)


def test_prophecy_round_trip():
    prophecy = make_prophecy(MEGA645, 1550)
    store.append_prophecy(prophecy)

    loaded = store.read_prophecies("mega645")
    assert len(loaded) == 1
    assert loaded[0].numbers == prophecy.numbers
    assert loaded[0].seed == prophecy.seed


def test_prophecy_append_only():
    """Writing twice for the same draw must fail - no retroactive edits."""
    store.append_prophecy(make_prophecy(MEGA645, 1550))

    with pytest.raises(store.ProphecyConflict, match="already exists"):
        store.append_prophecy(make_prophecy(MEGA645, 1550, numbers=tuple(range(2, 14))))

    assert len(store.read_prophecies("mega645")) == 1


def test_prophecy_rejected_if_draw_already_settled():
    """Prophesying a draw that already has a result is cheating."""
    store.write_draws("mega645", [make_draw(MEGA645, 1549)])

    with pytest.raises(store.ProphecyConflict, match="already been drawn"):
        store.append_prophecy(make_prophecy(MEGA645, 1549))


def test_prophecies_for_different_games_do_not_collide():
    store.append_prophecy(make_prophecy(MEGA645, 1550))
    store.append_prophecy(make_prophecy(POWER655, 1550))

    assert len(store.read_prophecies()) == 2
    assert len(store.read_prophecies("mega645")) == 1


def test_corrupt_jsonl_reports_location():
    """A malformed line must name its line number, not fail somewhere downstream."""
    import json

    valid = json.dumps(make_draw(MEGA645, 1).to_dict())
    path = store.draws_path("mega645")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{valid}\nnot json at all\n", encoding="utf-8")

    with pytest.raises(ValueError, match=":2 is not valid JSON"):
        store.read_draws("mega645")


def test_scoreboard_round_trip():
    store.write_scoreboard({"per_game": {}, "note": "xin chào"})
    assert store.read_scoreboard()["note"] == "xin chào"


def test_data_dir_honours_env_override(tmp_path, monkeypatch):
    monkeypatch.setenv(store.ENV_DATA_DIR, str(tmp_path / "elsewhere"))
    assert store.data_dir() == tmp_path / "elsewhere"
