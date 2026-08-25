"""The 10×10 heatmap's width is arithmetic, and this is where it gets checked.

`.cell` asks for a fixed `--tap` square. `.heat--matrix` lays out exactly ten columns as
`minmax(0,1fr)`, and `minmax(0,…)` lets a track shrink BELOW its item's minimum — at which
point every cell overflows its track and paints on top of its neighbour. Measured before
the fix: 15.7px of overlap per cell in a three-block row, 13.4px on a 390px phone, where it
had been shipping unnoticed since the matrix landed.

Two rules keep it from coming back, and both are source-level because layout cannot be
asserted without a real browser:

  * `.heat--matrix .cell` clears the floor, so a cell can never exceed its track.
  * `.block--heat` states the width ten `--tap` cells actually need, so the grid keeps the
    full tap target wherever the row has room and anything else in the row wraps below.

The second is written as a `calc()` over the tokens rather than a number, and this file
evaluates it. Change `--tap` to 48px without touching the basis and the arithmetic stops
agreeing, which is the whole point.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

SITE = Path(__file__).resolve().parents[1] / "site"
PAGE_CSS = (SITE / "page.css").read_text(encoding="utf-8")
TOKENS_CSS = (SITE / "tokens.css").read_text(encoding="utf-8")
RENDER_JS = (SITE / "render.js").read_text(encoding="utf-8")

MATRIX_COLUMNS = 10


def token_px(name: str) -> float:
    """The :root value of a length token, in px."""
    root = TOKENS_CSS[TOKENS_CSS.index(":root") :]
    match = re.search(rf"--{re.escape(name)}:\s*([\d.]+)px", root)
    assert match, f"--{name} is not defined as a px length in tokens.css"
    return float(match.group(1))


def rule(selector: str) -> str:
    """The declaration block of a selector, whitespace collapsed.

    Anchored at the start of a line, or `.cell` would match inside `.heat--matrix .cell`
    and quietly test the wrong rule. Duplicate selectors are an error rather than a
    first-match: page.css had a dead `.heat` block that every later rule overrode, and a
    lenient reader here is how that survives.
    """
    found = re.findall(r"(?m)^" + re.escape(selector) + r"\s*\{([^}]*)\}", PAGE_CSS)
    assert found, f"{selector} is gone from page.css"
    assert len(found) == 1, f"{selector} is declared {len(found)} times in page.css"
    return re.sub(r"\s+", " ", found[0]).strip()


# --- the floor that caused the overlap ----------------------------------------------


def test_matrix_cells_do_not_carry_a_minimum_height():
    """A `--tap` floor inside a `minmax(0,1fr)` track is exactly what made cells overlap."""
    assert "min-height:0" in rule(".heat--matrix .cell").replace(" ", "")


def test_the_generic_cell_still_asks_for_a_full_tap_target():
    """Only the matrix relaxes it. The pool heatmap auto-fills, so it never overflowed."""
    assert "min-height:var(--tap)" in rule(".cell").replace(" ", "")


def test_the_matrix_is_still_ten_columns():
    """Rows are the tens digit. Auto-fill would read faster and mean less."""
    assert f"repeat({MATRIX_COLUMNS},minmax(0,1fr))" in rule(".heat--matrix").replace(" ", "")


# --- the width that keeps the tap target --------------------------------------------


def test_the_heat_block_states_the_width_ten_tap_cells_need():
    """Evaluate the shipped calc() and compare it against the geometry it claims to be."""
    basis = re.search(r"\.block--heat\{flex-basis:calc\((.*?)\)\}",
                      re.sub(r"\s+", "", PAGE_CSS))
    assert basis, ".block--heat no longer states a flex-basis"

    expression = basis.group(1)
    for name in ("tap", "heat-gap", "space-md", "rule-slab"):
        expression = expression.replace(f"var(--{name})", str(token_px(name)))
    assert "var(" not in expression, f"unresolved token in {expression!r}"

    declared = eval(expression, {"__builtins__": {}})  # noqa: S307 - arithmetic from our own CSS
    # ten cells, the gaps between them, the block's padding, and its slab border
    needed = (
        MATRIX_COLUMNS * token_px("tap")
        + (MATRIX_COLUMNS - 1) * token_px("heat-gap")
        + 2 * token_px("space-md")
        + token_px("rule-slab")
    )
    assert declared == needed


def test_the_heat_basis_beats_the_default_row_basis():
    """Otherwise flex would still hand the grid the same 320px every other block gets."""
    default = float(re.search(r"\.row > \*\{flex:1 1 (\d+)px", PAGE_CSS).group(1))
    needed = MATRIX_COLUMNS * token_px("tap") + (MATRIX_COLUMNS - 1) * token_px("heat-gap")
    assert needed > default


def test_the_heat_gap_is_a_token_not_a_literal():
    """The basis is computed from it, so a literal here would drift the two apart."""
    assert "gap:var(--heat-gap)" in rule(".heat").replace(" ", "")


# --- the renderer has to ask for it -------------------------------------------------


def test_the_kienthiet_heatmap_block_carries_the_modifier():
    """CSS alone cannot help a block that never gets the class."""
    assert "'block block--heat'" in RENDER_JS


@pytest.mark.parametrize("selector", (".heat--matrix .cell", ".block--heat"))
def test_each_fix_explains_itself(selector):
    """Both rules look arbitrary without the measurement that produced them."""
    before = PAGE_CSS[: PAGE_CSS.index(selector)]
    comment = before.rindex("/*")
    assert "overlap" in before[comment:].lower() or "squeez" in before[comment:].lower()
