# design.md — trungso

Locked design system. Written by Hallmark on 2026-08-19. Any later page in this project
follows this file rather than rotating to a new look.

## Voice

A street fortune-teller. Says **thầy**, calls the reader **con**. Overconfident, never
responsible, always leaves an exit ("trúng là phúc nhà con, trượt là do con đi ngang qua
đám ma"). He is **never** allowed to say the numbers will win — that sentence belongs to
the scam sites this project is mocking.

He is also **silent** in one place: stage `04 · SỰ THẬT`, the disclaimer, and every
statistical label. The joke is the gap between four stages of shouting and one stage of
cold arithmetic. Collapse that gap and the project loses both its punchline and its
honesty.

## Macrostructure — Narrative Workflow

A fortune-telling session is an ordered thing, so the page is too:

| stage | content |
|---|---|
| `00 · KHAI` | birth-date form, local-only, with the privacy block |
| `01 · TƯỚNG` | the fortune: can chi, nạp âm, cung, số chủ đạo, sao, tam hợp / tứ hành xung |
| `02 · PHÁN` | twelve numbers for the wheel and six for a plain ticket, house oracle and personal oracle side by side, then the pot |
| `03 · SỔ NỢ` | scoreboard, ROI, ROI-excluding-jackpot, head-to-head, "cạn phước" |
| `04 · SỰ THẬT` | chi-square across five lotteries, heatmaps, recent draws, XSMB |

Stage numbers sit **above** their titles in the same column. Number-left / title-right is
the most reliable templated-editorial tell and is not used here.

Nav: **N7 brutal slab** — thick sticky bar, wordmark left, four rubber stamps right.
Footer: **Ft5 statement** — one sentence, no link columns.

## Shape language

- `--radius: 0` everywhere. The only round thing on the page is a lottery ball (`--ball: 50%`).
- Blocks are divided by **uneven rules** — a `--rule-slab` on one edge, `--rule-hair` on the
  others. Never an even 1px box on four sides; that is the card look this redesign removed.
- Torn ticket edge via `repeating-linear-gradient`, no image asset.
- Full-page grain overlay, `mix-blend-mode` per skin. The page should feel printed.
- Stamps: display type, rotated `-4deg`, thick border. Used for the skin picker and for
  the "CẠN PHƯỚC" verdict.

## Four skins

One macrostructure, four skins, switchable at runtime and remembered in `localStorage`.

| key | paper | display | body | accent | axes |
|---|---|---|---|---|---|
| `veso` (default) | cream `#F2E8D5` | Bungee | Be Vietnam Pro | brick red | light · display-heavy · warm |
| `thantai` | lacquer red `#7A1414` | Playfair Display | Be Vietnam Pro | gilt gold | dark · high-contrast-serif · warm-gold |
| `viahe` | near-black `#0A0A0A` | Anton | JetBrains Mono | phosphor green | dark · display-condensed · chromatic-other |
| `y2k` | violet `#1A0B2E` | Bungee Shade | Grandstander | cyan + magenta | dark · display-3D · cool |

`Sriracha` (handwriting) runs across all four for the fortune-teller's own lines. It is the
thread that ties the skins together, and the clearest anti-AI-slop detail on the page.

## Two rules learned the hard way

**1. Every display face must carry Vietnamese glyphs.** Verified against the Google Fonts
API. These are safe: Bungee · Bungee Shade · Anton · Alfa Slab One · Playfair Display ·
Bricolage Grotesque · Be Vietnam Pro · JetBrains Mono · Baloo 2 · Oswald · Merriweather ·
Sriracha · Grandstander. These are **not**, and will shred every diacritic on the page:
Archivo Black · Bebas Neue · Instrument Serif · DM Serif Display · Lilita One · Fredoka ·
Passion One · Rubik Mono One.

**2. A 3D display face is illegible below ~20px.** Data values use `--font-body` at weight
800, never `--font-display`. "ĐẠI LÂM MỘC" in Bungee Shade at 16px is a smudge.

## Contrast floor — measured, not assumed

Every text surface clears **AA 4.5:1 in all four skins**; the lowest on the page is 4.56.
Two tokens exist purely to hold that line:

- `--color-on-accent-2` — the dark colour to place on a solid `--color-accent-2` fill.
  Accent-2 is a loud colour in every skin, so `--color-ink` on top fails (1.01:1 in `viahe`).
- `veso`'s `--color-accent` was deepened from `oklch(60.4%)` to `oklch(54%)`. Cream-on-red
  was 3.53:1, short of AA for the 14px bold UI text that uses it.

Measure with a canvas, not by parsing `getComputedStyle().color` — it returns `oklch(...)`
verbatim, and string-parsing that as RGB produces confident nonsense.

## Motion

Four primitives, all `transform` / `opacity`: `stamp-press`, `ball-in` (staggered),
`reveal` (on scroll), and `thay-idle`. Named easings only. `prefers-reduced-motion: reduce`
collapses everything to a 150ms opacity fade.

`thay-idle` is the one infinite loop on the page, and it was added on an explicit request
for a real looping animation rather than a one-shot. It cross-fades two frames of the
hand-drawn fortune-teller over 4s using `opacity` only, so it stays GPU-composited and
never touches layout. It exists in exactly one place - the head of stage 02 - and it ships
with two conditions that are part of the primitive, not options attached to it:

1. **It pauses when it is not on screen.** `render.js` observes the figure and toggles
   `.is-paused`, which sets `animation-play-state: paused`. An infinite animation running
   behind the fold is battery cost with nothing to show for it. Verified by reading
   `animation-play-state`, not by trusting the class.
2. **`prefers-reduced-motion: reduce` removes it entirely** - `animation: none`, second
   frame hidden. Not slowed, not shortened. Removed. This is an accessibility requirement,
   so it is not subject to taste.

A fifth primitive would need the same treatment, or it does not get added.

## Exports

`site/tokens.css` is the single source for every colour, face, space, and duration. No page
CSS declares a raw colour or a `font-family` string; everything references a token by name.
