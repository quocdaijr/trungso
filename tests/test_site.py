"""The static-site bundle. It must be self-contained, small, and honest."""

from __future__ import annotations

import json

from conftest import make_draw, make_prophecy, random_draw
from trungso import site, store
from trungso.games import MEGA645, POWER655
from trungso.sources import xsmb


def _seed_history(count: int = 30) -> None:
    import random

    rng = random.Random(7)
    for spec in (POWER655, MEGA645):
        store.write_draws(spec.key, [random_draw(spec, i, rng) for i in range(1, count + 1)])


def test_bundle_covers_only_prophecy_games():
    """US games are stats-only and have no wheel, so the page never shows them."""
    _seed_history()
    bundle = site.build_bundle()
    assert [g["key"] for g in bundle["games"]] == ["power655", "mega645"]


def test_bundle_carries_the_disclaimer():
    _seed_history()
    bundle = site.build_bundle()
    assert "biến cố độc lập" in bundle["disclaimer"]
    assert "paper-trading" in bundle["disclaimer"]


def test_bundle_includes_both_roi_figures():
    """The jackpot-free ROI must reach the page, or one lucky draw rewrites the story."""
    _seed_history()
    game = site.build_bundle()["games"][0]

    assert "expected_roi" in game["wheel"]
    assert "expected_roi_excluding_jackpot" in game["wheel"]
    assert game["wheel"]["expected_roi_excluding_jackpot"] < game["wheel"]["expected_roi"] < 0
    assert "roi_excluding_jackpot" in game["score"]


def test_bundle_trims_history_to_recent_draws():
    """The browser has no use for a thousand draws."""
    _seed_history(count=200)
    game = site.build_bundle()["games"][0]

    assert game["draw_count"] == 200
    assert len(game["recent"]) == site.RECENT_DRAWS


def test_bundle_includes_chi_square_and_verdict():
    _seed_history(count=120)
    game = site.build_bundle()["games"][0]

    assert game["chi_square"]["degrees_of_freedom"] == POWER655.pool - 1
    assert 0.0 <= game["chi_square"]["p_value"] <= 1.0
    assert game["chi_square"]["verdict"]


def test_frequency_covers_the_whole_pool():
    _seed_history()
    game = site.build_bundle()["games"][1]
    assert len(game["frequency"]) == MEGA645.pool


def test_pending_prophecy_appears_but_settled_ones_do_not():
    store.write_draws("mega645", [make_draw(MEGA645, 1)])
    store.append_prophecy(make_prophecy(MEGA645, 2))

    game = next(g for g in site.build_bundle()["games"] if g["key"] == "mega645")
    assert game["pending_prophecy"]["draw_id"] == "00002"


def test_no_pending_prophecy_is_null_not_an_error():
    store.write_draws("mega645", [make_draw(MEGA645, 1)])
    game = next(g for g in site.build_bundle()["games"] if g["key"] == "mega645")
    assert game["pending_prophecy"] is None


def test_xsmb_is_null_when_absent():
    _seed_history()
    assert site.build_bundle()["xsmb"] is None


def test_xsmb_section_is_included_when_present():
    header_free = [
        xsmb.XsmbDraw(date=d, special=7, prizes=(7,) + tuple(range(26)))
        for d in (__import__("datetime").date(2026, 8, 17),)
    ]
    store.write_xsmb(header_free)
    _seed_history()

    payload = site.build_bundle()["xsmb"]
    assert payload["draw_count"] == 1
    assert len(payload["frequency"]) == 100
    assert payload["chi_square"]["degrees_of_freedom"] == 99


def test_bundle_is_json_serialisable(tmp_path):
    _seed_history()
    bundle = site.build_bundle()
    target = site.write_bundle(bundle, site_dir=tmp_path)

    assert target.name == site.BUNDLE_NAME
    reloaded = json.loads(target.read_text(encoding="utf-8"))
    assert reloaded["games"][0]["display"] == "Power 6/55"


def test_write_bundle_leaves_no_temp_file(tmp_path):
    site.write_bundle({"games": [], "xsmb": None}, site_dir=tmp_path)
    assert list(p.name for p in tmp_path.iterdir()) == [site.BUNDLE_NAME]


def test_bundle_handles_empty_history():
    """A fresh clone with no data must still produce a renderable bundle."""
    bundle = site.build_bundle()
    for game in bundle["games"]:
        assert game["draw_count"] == 0
        assert game["latest"] is None
        assert game["chi_square"] is None
        assert game["score"]["draws_scored"] == 0


# --------------------------------------------------------- jackpot in the bundle


def _store_prizes(game: str, draw_id: str, top: int = 34_897_731_150, winners: int = 0):
    from trungso.sources.vietlott_prizes import DrawPrizes, PrizeTier

    store.write_prizes(
        DrawPrizes(
            game=game,
            draw_id=draw_id,
            jackpots={"Jackpot 1": top},
            tiers=(PrizeTier("Jackpot 1", winners, top),),
            fetched_at="2026-08-20T07:00:00+00:00",
        )
    )


def test_bundle_carries_the_jackpot_for_the_newest_draw():
    store.write_draws("power655", [make_draw(POWER655, 1386)])
    _store_prizes("power655", "01386")

    payload = site.build_bundle()
    game = next(g for g in payload["games"] if g["key"] == "power655")

    assert game["prizes"]["top_jackpot_vnd"] == 34_897_731_150
    assert game["prizes"]["rolled_over"] is True
    assert game["prizes"]["matches_latest_draw"] is True


def test_a_jackpot_from_an_older_draw_is_flagged_not_hidden():
    """If the prize fetch failed, the stored figure belongs to a draw that is no longer
    the newest. Hiding it loses information; presenting it as current would be a lie.
    The flag lets the page say which draw the money belongs to."""
    store.write_draws("power655", [make_draw(POWER655, 1386), make_draw(POWER655, 1387)])
    _store_prizes("power655", "01386")

    payload = site.build_bundle()
    game = next(g for g in payload["games"] if g["key"] == "power655")

    assert game["prizes"]["matches_latest_draw"] is False
    assert game["prizes"]["draw_id"] == "01386"
    assert game["prizes"]["latest_draw_id"] == "01387"


def test_prizes_are_null_when_never_fetched():
    store.write_draws("power655", [make_draw(POWER655, 1386)])

    payload = site.build_bundle()
    game = next(g for g in payload["games"] if g["key"] == "power655")

    assert game["prizes"] is None
