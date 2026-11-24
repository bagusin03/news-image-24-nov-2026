# The World Today — 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/bagusin03/news-image-24-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/bagusin03/news-image-24-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One front-page image summing up Tuesday 24 November 2026's world news, drawn entirely in code.

## The day

- **COP31 collapses** — nearly 200 nations fail to agree a climate pact in Antalya, Türkiye; no mention of fossil fuels in the final text.
- **Warship sunk off Libya** — Ukrainian sea drones sink the Russian corvette *Merkury* in Benghazi.
- **Iran vows to fight a US naval blockade** in the Strait of Hormuz.
- **Factory fire kills 24+** in Banten, Indonesia; the rescue search goes on.
- **Lisbon marches on prices** — thousands protest the cost of living.
- **NATO sends AWACS to Poland** after Russian missiles land on NATO soil.
- Also: the India–Nepal Saryu-Kamala Express rolls, Gukesh begins his chess title defence in Geneva, and Asian regulators step in as the AI stock sell-off calms.

## Run it

```sh
python3 main.py
```

Writes one 1024×1024 PNG to `/output/entry.png` (about 25 KB, well under the 1 MiB cap).

## How it works

Pure Python 3.13 standard library only — no image libraries, no network, no API keys, no randomness, no clock:

- A hand-rolled PNG encoder (`zlib` + CRC32, filter 0, RGB8).
- Pixel drawing primitives (rects, circles, ellipses, lines, filled polygons) for the globe, warship, tanker, factory, protest crowd, AWACS jet, train, chessboard and market chart.
- A small 5×7 bitmap font drawn by hand for all the text.

Fully deterministic: two runs produce byte-identical PNGs.

---

<sub>Entered on [make.fun](https://make.fun/?ref=0d6e5fs5&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
