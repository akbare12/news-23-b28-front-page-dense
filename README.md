# THE WORLD TODAY — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b28-front-page-dense/rank.svg)](https://make.fun/competitions/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b28-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image summing up 23 November 2026's world news: the AI rout that hit Asian
markets (Kospi −3.3%), Guterres' call to regulate AI before it's too late at the
Bridgetown summit, and the US lead over China at a record low in the Asia Power
Index — plus 28 more stories, a world map with numbered pins, and a DATE CHECK
box separating what happened on 23 November from what did not.

## How it is built

`draw.py` (Pillow) renders `entry.png` (1024×1024, under 1 MiB). `main.py`
(stdlib only — it parses the PNG header by hand with `struct`, no image
library) copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` and verifies
the output is byte-identical. Run it with:

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

## Stories (31)

**Heroes:** AI rout hits Asia · Guterres: regulate AI before it's too late ·
US lead over China at record low. **10 cards:** Bessent demands Nvidia
answers · FBI probes NCIC police-database hack · Trump: Iran strikes may
resume in New Year · Nasdaq futures +3% · Skubal's $450M Mets deal ·
Tom Jackson dies at 75 · States sue SpaceX over AI safety claims ·
Anthropic IPO $107.3B · Poland: 3 Russian Kh-101 missiles crossed airspace
(CLAIM) · Intel warns of Russian nuclear satellite (CLAIM). **Also:**
Paris 2% billionaire tax · Manchester 12,000 cleared · 165 Russian missiles
in a week · COP31: the day after · Israel unity talks · Gaza strike ·
West Bank settler attacks · Iran war: no deal in sight · Lebanon 264 kg
explosives · Bahrain strike · Benghazi probe · Sudan drones · DRC Ebola
teams trapped · Bangladesh: Hasina jailed if she returns · Seoul minister
quits · SK Telecom −7.3% · China eases margin rules · Seoul 10T-won fund.

**DATE CHECK — left out (not 23 Nov):** Democrats reach 258 seats (22 Nov) ·
Sparta II fire (22 Nov) · El Chapo Isidro captured (22 Nov) · EU–Indonesia
pact (21 Nov) · Nigeria boat (21 Nov) · ICJ Myanmar ruling (19 Nov).

Scenes are drawn illustrations, not photographs. Chips: REPORTED = confirmed
by wires; CLAIM = one side's claim, not independently confirmed.
