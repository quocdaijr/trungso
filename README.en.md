# 🔮 trungso

*The fortune-teller calls the numbers for you. Then mathematics calls the fortune-teller.*

[![Oracle](https://github.com/quocdaijr/trungso/actions/workflows/oracle.yml/badge.svg)](https://github.com/quocdaijr/trungso/actions/workflows/oracle.yml)
[![CI](https://github.com/quocdaijr/trungso/actions/workflows/ci.yml/badge.svg)](https://github.com/quocdaijr/trungso/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue.svg)](pyproject.toml)
[![Ruff](https://img.shields.io/badge/lint-ruff-261230.svg)](https://docs.astral.sh/ruff/)
[![tests](https://img.shields.io/badge/tests-459%20passing-brightgreen.svg)](tests/)
[![draws analysed](https://img.shields.io/badge/draws%20analysed-12%2C578-informational.svg)](#what-the-honest-layer-found)
[![chi-square](https://img.shields.io/badge/chi²%20p--value-0.53%20→%20random-informational.svg)](#what-the-honest-layer-found)
[![prediction accuracy](https://img.shields.io/badge/prediction%20accuracy-0%25-critical.svg)](DISCLAIMER.md)
[![expected ROI](https://img.shields.io/badge/expected%20ROI-−86%25-critical.svg)](DISCLAIMER.md)
[![status](https://img.shields.io/badge/status-satire-ff69b4.svg)](DISCLAIMER.md)

**🇻🇳 Tiếng Việt → [README.md](README.md)**

---

> ## ⚠️ READ THIS SENTENCE FIRST
>
> ### This site cannot predict lottery numbers. No software can.
>
> It is an **AI-token-burning experiment**. Every number here is random, and the site
> publishes the proof against itself — a chi-square test over 12,578 real draws.
>
> - **Nothing is for sale** — no payments, no accounts, no ads
> - **Not affiliated with Vietlott** — not sponsored, not endorsed, not authorised
> - **Third-party data** that can be wrong or incomplete — for authoritative results use [vietlott.vn](https://vietlott.vn)
> - **18+**
> - **Use at your own risk** — provided AS IS; every loss is yours alone
>
> 📄 Full text: [**DISCLAIMER.md**](DISCLAIMER.md)

---

## Why this repository exists

Honestly: **so the AI tokens already burned wouldn't go to waste.**

This is a by-product of an AI-coding experiment. Rather than let millions of tokens evaporate,
they turned into something that runs, has tests, and makes fun of itself.

The only genuine value here is **The Honest Layer** — the statistics showing that lotteries are
random, measured on real data from five lotteries across two countries. Everything else is a
pavement fortune-teller implemented in code.

If you came looking for numbers to play, the fortune-teller will tell you straight: the numbers
here are **exactly** as random as numbers you pick yourself. The only difference is that this
site **admits it**.

### A note on voice

The Vietnamese original is written in the register of a pavement fortune-teller: he calls himself
**thầy** ("master", "teacher") and calls the reader **con** ("child"). It is deliberately
presumptuous — the register of someone who has decided he is the authority in the room.

English has no equivalent pronoun pair, so this translation uses plain "you". The hierarchy is
lost; the presumption survives in the phrasing.

He is silent in three places, in both languages: the disclaimer, the statistics, and the
gambling-support note. That gap is the joke, and it is also what keeps the project honest.

## Two layers

**The Honest Layer** — frequency, gap analysis, and a chi-square goodness-of-fit test against a
uniform distribution. The incomplete gamma function is hand-rolled so the project needs no
scipy. The expected result is `p >> 0.05`, meaning *nothing to see here* — and the site prints
exactly that.

**The Cursed Layer** — an oracle that produces twelve numbers from "cosmic signals": numerology
of the draw date, the Bitcoin price, the temperature in Hanoi, the lunar date and its zodiac
animal, and the karma of the previous draw's bonus ball. Predictive value: zero. Entertainment
value: the entire point.

## What makes this project honest

Every prophecy is generated **deterministically** from
`sha256(version | game | draw_id | date | signals)` and written to `data/predictions.jsonl`
**before** that draw takes place. Run it again and you get the same twelve numbers. It cannot
be edited after the fact.

`ORACLE_VERSION` is part of the seed, so changing the algorithm cannot flatter the past — two
prophecies committed at v1.0.0 are still v1.0.0 even though the oracle is now at v1.3.0.

That is what makes the **Hall of Shame** (*Bảng Phong Thần* — literally "the register of
deified names", used here for a scoreboard of failure) mean anything.

## Usage

```bash
uv sync

uv run trungso ingest --check-gaps      # fetch results; patches from vietlott.vn when the mirror lags
uv run trungso stats                    # The Honest Layer: chi-square + verdict, every source
uv run trungso oracle                   # The Cursed Layer: twelve numbers + the fortune-teller's lines
uv run trungso score                    # rebuild the Hall of Shame
uv run trungso backtest --game mega645  # replay the oracle over all of history → ROI
uv run trungso today                    # dashboard for the next draw
uv run trungso site                     # emit site/data.json for the static page
uv run trungso notify --kind prophecy   # push the twelve numbers to Telegram
```

View the static site:

```bash
uv run trungso site && python3 -m http.server -d site 8000
```

Telegram needs `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` (GitHub Secrets in CI). Without them
`notify` fails loudly, while the data pipeline is **never** affected.

## Wheel-12 arithmetic

The site plays *bao 12* — pick twelve numbers, cover all `C(12,6) = 924` combinations. At
10,000₫ per line that is **9,240,000₫ per draw per game**.

With `k` = how many of your twelve appear among the six drawn:

```
N(j) = C(k, j) · C(12 − k, 6 − j)        Σ N(j) = 924   (Vandermonde; asserted in tests)
```

Power 6/55's Jackpot 2 needs five main numbers **plus** the bonus, so that combination has to be
separated out rather than counted as a first prize.

| | Expected ROI (jackpot at floor) | Excluding jackpot |
|---|---:|---:|
| Mega 6/45 | −71.57% | −86.30% |
| Power 6/55 | −76.20% | −86.55% |

A backtest over 1,353 Mega 6/45 draws hit the jackpot exactly **once**, and ROI jumped to
**+11.35%** — while the hit rate stayed at 1.624 against a chance expectation of 1.600. That is
why *ROI excluding jackpot* is a first-class figure here and not a footnote: one lucky draw
hides everything else, which is precisely how every "lottery system" fools itself.

## Four skins

The page ships four runtime-switchable skins, remembered in `localStorage`:

| | paper | display face | spirit |
|---|---|---|---|
| **Vé Số** (default) | yellowed newsprint | Bungee | street lottery ticket, red riso ink |
| **Thần Tài** | lacquer red | Playfair Display | household shrine, gilt lettering |
| **Vỉa Hè** | near-black | Anton | pavement brutalism, phosphor green |
| **Y2K** | violet | Bungee Shade | early-2000s Vietnamese forum |

One macrostructure, four skins. Every colour and face comes from a token in `site/tokens.css` —
no raw values in the page. Every text surface clears **WCAG AA 4.5:1 in all four skins**
(lowest is 4.56), measured with a canvas rather than estimated.

Every display face was verified to carry **Vietnamese glyphs**. Several attractive faces do not,
and using one shreds every diacritic on the page.

## Personalisation — and why there is no sign-up

Enter a birth date (optionally a name and gender) and the page derives a full *lá số*: sexagenary
year, five-element destiny, Western zodiac sign, life-path number, guardian star, and the
harmony/clash animal groups — then twelve numbers of your own, plus a head-to-head table against
the house oracle and against pure chance.

> **🔒 No sign-up, no accounts, no server.** The birth date, name and gender live only in your
> browser's `localStorage`. No request carries them anywhere. One button wipes them.

This is an architectural decision, not laziness: this repo **commits its data into public git**
as an audit trail, so personal data must never touch the data path — git history cannot be
un-published. And everything enjoyable here is derivable from a birth date alone, so there is
nothing worth collecting.

The browser does **not** reimplement the lunar algorithm. Python generates a lookup table
(Tết dates, sexagenary cycle, five-element names for 1929–2035) embedded in `site/data.json`, and
a parity test drives the real `site/personal.js` through Node to check every value against
Python.

## Data sources

| Source | Used for | Size |
|---|---|---|
| [`thanhnhu/vietlott`](https://github.com/thanhnhu/vietlott) (MIT) | primary — Power 6/55 & Mega 6/45 | 1,386 + 1,353 draws since 2017 |
| `vietlott.vn` | fallback when the mirror lags (latest draw only) | — |
| [`khiemdoan/vietnam-lottery-xsmb-analysis`](https://github.com/khiemdoan/vietnam-lottery-xsmb-analysis) (MIT) | XSMB — honest layer + a cosmic signal | 7,526 draws since 2005 |
| [`jbaranski/jeffs-lottery-utils`](https://github.com/jbaranski/jeffs-lottery-utils) (MIT) | Powerball & Mega Millions — statistics only | 1,395 + 918 draws |
| CoinGecko / Open-Meteo | cosmic signals (BTC, weather) | — |

`data.ny.gov` — the "official" source usually recommended — is **unusable**: the entire domain
returns 403 from this network, including its plain HTML pages, with or without browser headers.

The US games are **statistics-only**: no prophecies, no wheel, no scoreboard. Wheel-12 is a
Vietlott product; the sole purpose of the US data is to let The Honest Layer show that American
lotteries are exactly as random.

## What the Honest Layer found

Chi-square test, H₀ = "every number is equally likely":

| Source | Draws | Observations | χ² | df | p-value | Rejects H₀? |
|---|---:|---:|---:|---:|---:|---|
| Power 6/55 | 1,386 | 8,316 | 52.45 | 54 | **0.5343** | no |
| Mega 6/45 | 1,353 | 8,118 | 32.57 | 44 | **0.8982** | no |
| Powerball (US) | 1,395 | 6,975 | 78.86 | 68 | **0.1731** | no |
| Mega Millions (US) | 918 | 4,590 | 60.17 | 69 | **0.7671** | no |
| XSMB (Northern Vietnam) | 7,526 | **203,202** | 104.26 | 99 | **0.3391** | no |

Five independent lotteries, two countries, **231,201 number observations**, 21 years of data —
and **not one source** rejects the randomness hypothesis. Any number that looks "hot" is noise.

## Draw schedule

- **Power 6/55** — 18:00 Tue / Thu / Sat
- **Mega 6/45** — 18:00 Wed / Fri / Sun
- **XSMB** — 18:15 daily

## Licence & disclaimer

[MIT](LICENSE) — the software is provided **AS IS**, without warranty of any kind.

Full disclaimer (bilingual): [**DISCLAIMER.md**](DISCLAIMER.md)

If you use this to gamble and lose, that was your decision — not the fortune-teller's, and
certainly not the repository's.

### If gambling has become a problem

*The fortune-teller does not speak here. This part is real.*

Vietnam has **no** dedicated gambling-addiction helpline. The nearest real free resource is the
[Ngày Mai hotline](https://duongdaynongngaymai.vn/hotline/) — **+84 96 306 1414**, 13:00–20:30
Wed–Sun. It is **psychological crisis support**, not gambling-specific, but they listen without
judgement. Internationally, [Gamblers Anonymous](https://www.gamblersanonymous.org/) lists groups
by country.
