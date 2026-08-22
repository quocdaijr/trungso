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
| `vietlott.vn` (same page) | Jackpot value and prize tiers per draw | 2 games |
| [`khiemdoan/vietnam-lottery-xsmb-analysis`](https://github.com/khiemdoan/vietnam-lottery-xsmb-analysis) (MIT) | XSMB — honest layer + a cosmic signal | 7,526 draws since 2005 |
| [`jbaranski/jeffs-lottery-utils`](https://github.com/jbaranski/jeffs-lottery-utils) (MIT) | Powerball & Mega Millions — statistics only | 1,395 + 918 draws |
| CoinGecko / Open-Meteo | cosmic signals (BTC, weather) | — |

`data.ny.gov` — the "official" source usually recommended — is **unusable**: the entire domain
returns 403 from this network, including its plain HTML pages, with or without browser headers.

The US games are **statistics-only**: no prophecies, no wheel, no scoreboard. Wheel-12 is a
Vietlott product; the sole purpose of the US data is to let The Honest Layer show that American
lotteries are exactly as random.

### What the jackpot figure is, and is not

The results page states the jackpot **as at a completed draw**, and that is the only jackpot
figure a plain HTTP request can get: vietlott.vn serves its estimate for the *upcoming* draw
through JavaScript, and the landing pages return an 18 KB shell with no data in it at all.

So when nobody won, the site says **"ít nhất X"** — at least X — because the next draw's pot
is that figure plus whatever the new tickets add. It never says "the jackpot is X". It also
always names the draw the money belongs to, because if the prize fetch failed on the last
run the stored figure describes an older draw, and a stale number wearing a current label is
the one thing this repository is built not to print.

The scoreboard's arithmetic did not change. The fixed tiers really are fixed — the live page
confirms 40.000.000 / 500.000 / 50.000 for Power, matching `games.py` — and the jackpot was
already excluded from `roi_excluding_jackpot` precisely because it varies. A test now asserts
the static table still matches the live one, so a silent upstream change would fail loudly.

### Six numbers or twelve? Both, and the page now says which

A plain Vietlott ticket - "Cách chơi: Cơ bản" in the app - is **six numbers for 10,000d**.
Bao 12 is a real alternative, not an invention: Vietlott's own product pages list eleven bao
sizes (5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 18) and price a single combination at 10,000d, so
`C(12,6) = 924` combinations for 9,240,000d is correct. Third-party summaries routinely get
this wrong - one lists seven sizes and then says "eleven types" in the same article - so the
official page is the only source used here.

The page used to show only the twelve, which meant anyone buying the basic ticket had to guess
which six. It now shows both, and shows the **split**: a typical draw boosts one to three of
the twelve and leaves the rest at exactly the same weight, so only that many of the six were
chosen for a reason. The rest come out of a tie, and the page says so.

Ties break on the prophecy's seed, not by ascending number. That was measured, not styled:
sorting ties ascending made the six-number pick average 20.79 against the wheel's 28.52 over
300 draws - a 7.7 skew toward low numbers created entirely by the tie-break. Shipping a
spurious pattern would defeat the whole point of the repository.

### If it comes in tonight, what do you actually get?

The estimated pot for the *next* draw is not published anywhere a plain request can reach.
This is, and it is the question the jackpot figure makes people ask anyway - so the page
answers it from arithmetic instead of from a number it does not have.

For Mega 6/45, a bao-12 ticket costs 9,240,000đ:

| hits | 1 in | pays | net |
|---|---|---|---|
| 3 | 7 | 2,520,000đ | −6,720,000đ |
| 4 | 31 | 15,120,000đ | **+5,880,000đ** |
| 5 | 312 | 112,000,000đ | **+102,760,000đ** |
| 6 | 8,815 | 24,946,610,500đ | **+24,937,370,500đ** |

The table has to carry both halves. The money column alone reads as an argument *for*
playing - four hits already clears the stake, and it does. The probability column alone
reads as though the prizes were stingy, and they are not. Only together do they say the
true thing: the payouts are real, and the odds are what take them back. Four-or-better
happens about once in 28 draws, which is where the −71.57% goes.

## The finance page — `/tai-chinh.html`

A second page with the same two layers: the fortune-teller reads the market, then the page
states what that reading is worth. Gold (SJC bars and plain rings), the three exchange
indices, foreign net flows, and crypto.

It differs from the lottery page in exactly one way: **no Python is involved**. No source
module, no store, no bundle, no cron. The browser calls five APIs directly, and **no figure
is committed to the repository**.

| Block | Source | Actual freshness |
|---|---|---|
| Domestic gold | PNJ | Quoted price, changes a few times a day |
| World gold | gold-api.com | Realtime |
| Indices + foreign flows | VNDIRECT | **End of session (EOD)** |
| Crypto | CoinGecko | Realtime, 24/7 |

Three things the page states rather than hides:

**It is not realtime.** The real HOSE/HNX realtime feeds run over SignalR websockets and are
sold under vendor contracts; the only documented source (SSI FastConnect) requires signing up
in person at a branch. So the equity figures are end-of-session, and the page prints the
API's own timestamp rather than the page load time. At weekends it says *"latest session"*.

**Nothing is stored.** Every usable price endpoint is an internal API with no terms attached.
The repo already has a rule: *what has no verifiable licence does not get checked in*. So the
page fetches in the browser and commits nothing. The cost is real: **a dead source is an
empty block**, and no stale number is substituted. Each block degrades on its own — one
silent API never takes the page down.

**There is no land price.** It was planned, then dropped, and the reason is printed on the
page: Vietnam's residential property price index exists only as a **2019 indicator
specification that has never published a figure**; the national real-estate database portal
mandated by Decree 94/2024 **does not resolve**; and BIS, OECD, FRED, and the IMF Global
Housing Watch all **exclude Vietnam**. Inventing a number would be easy. Saying it does not
exist is correct.

> This page is **not investment advice**. The reading in stage 00 is a digit sum; its
> predictive value is **zero**, exactly like the lottery oracle's. See
> [DISCLAIMER.md](DISCLAIMER.md) section 2.

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

## Image assets

Everything is **self-hosted in the repository** — the page makes no outbound request for an
image or an emoji. Per-file provenance, download dates, and the list of sources that were
considered and rejected are in [`site/img/CREDITS.md`](site/img/CREDITS.md).

| Asset | Source | Licence |
|---|---|---|
| Đông Hồ woodblock print *Đại Cát* | [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Dong_Ho_painting_-_Dai_cat.jpg) | Public domain |
| 13 emoji | [jdecked/twemoji](https://github.com/jdecked/twemoji) — © Twitter/X | graphics **CC-BY 4.0**, code MIT |
| Fortune-teller figures (7 poses) | drawn by hand in this repo, `site/thay.js` | MIT, same repo |

This repository is MIT, which means anyone who clones it is granted the right to redistribute
it. So it cannot contain anything it does not own: copyrighted meme characters, film stills,
and images taken from social media were all ruled out — not because they were hard to find,
but because there was no licence. **OpenMoji** was ruled out too: it is CC-BY-**SA**, and
copyleft conflicts with MIT.

## Licence & disclaimer

[MIT](LICENSE) — the software is provided **AS IS**, without warranty of any kind. The MIT
grant covers the **code**; third-party assets keep their own licences, listed above.

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
