"""Invariants on the design tokens that a browser check would only catch by luck.

These are the values that were chosen by measurement, so they are the values most likely
to be changed later by someone who does not know what they were measured against.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

TOKENS = (Path(__file__).resolve().parents[1] / "site" / "tokens.css").read_text(
    encoding="utf-8"
)
PAGE_CSS = (Path(__file__).resolve().parents[1] / "site" / "page.css").read_text(
    encoding="utf-8"
)

SKINS = ("veso", "thantai", "viahe", "y2k")

# The largest tint each skin can carry with the cell label still clearing WCAG AA 4.5:1,
# swept in 1% steps against the composited cell in a real browser on 2026-08-20.
MEASURED_CEILING = {"veso": 60, "thantai": 37, "viahe": 40, "y2k": 60}


def _skin_block(skin: str) -> str:
    match = re.search(
        rf'\[data-theme="{skin}"\]\s*\{{(.*?)\n\}}', TOKENS, re.S
    )
    assert match, f"no token block for {skin}"
    return match.group(1)


def _root_block() -> str:
    match = re.search(r"\n:root\s*\{(.*?)\n\}", TOKENS, re.S)
    assert match
    return match.group(1)


def _heat_max(skin: str) -> int:
    """The cap that applies to a skin: its own override, else the :root default."""
    block = _skin_block(skin)
    own = re.search(r"--heat-max:\s*(\d+)%", block)
    if own:
        return int(own.group(1))
    root = re.search(r"--heat-max:\s*(\d+)%", _root_block())
    assert root, "no --heat-max anywhere"
    return int(root.group(1))


@pytest.mark.parametrize("skin", SKINS)
def test_heat_cap_stays_under_the_measured_contrast_ceiling(skin):
    """A tint above the ceiling drops the cell label under AA. The heat is decoration;
    the number is the data, and the data must stay readable."""
    assert _heat_max(skin) <= MEASURED_CEILING[skin], (
        f"{skin}: --heat-max {_heat_max(skin)}% exceeds the measured "
        f"{MEASURED_CEILING[skin]}% ceiling"
    )


def test_the_heat_fallback_is_safe_for_every_skin():
    """render.js sets only a unitless ratio, so the cap comes from CSS. If a skin ever
    loses its override the fallback in the calc() applies - and that fallback has to be
    survivable on the *strictest* skin, not the most forgiving one."""
    fallback = re.search(r"var\(--heat-max,\s*(\d+)%\)", PAGE_CSS)
    assert fallback, "the .cell background no longer carries a --heat-max fallback"

    assert int(fallback.group(1)) <= min(MEASURED_CEILING.values())


def test_heat_is_a_background_tint_not_a_text_opacity():
    """The whole point of the rewrite: opacity faded the label with the cell, and no
    contrast check could see it because opacity never touches the computed colour."""
    render = (Path(__file__).resolve().parents[1] / "site" / "render.js").read_text(
        encoding="utf-8"
    )
    heat_lines = [line for line in render.splitlines() if "--heat" in line and "//" not in line]

    assert heat_lines, "render.js no longer sets --heat"
    assert not any("opacity" in line for line in heat_lines)
    assert "cell.style.opacity" not in render


@pytest.mark.parametrize("skin", SKINS)
def test_every_skin_defines_a_display_leading(skin):
    """Vietnamese tone marks sit above the cap line, so display leading is per skin.
    A skin without one inherits :root, which is correct only if :root has one."""
    block = _skin_block(skin)
    assert re.search(r"--lh-display:", block) or re.search(
        r"--lh-display:", _root_block()
    )


def test_display_leading_never_goes_below_one():
    """Below 1.0 a wrapped heading's tone marks collide with the line above - measured
    at 320/390/414px on all four skins."""
    values = [float(v) for v in re.findall(r"--lh-display:\s*([\d.]+)", TOKENS)]

    assert values, "no --lh-display token"
    assert min(values) >= 1.0


@pytest.mark.parametrize("skin", SKINS)
def test_every_skin_defines_ink_for_its_accent_fill(skin):
    """accent-2 is used as a solid fill under text in several places. Whenever it is,
    the ink on top has to be named, or the page inherits body ink onto a bright fill."""
    assert "--color-on-accent-2:" in _skin_block(skin)
