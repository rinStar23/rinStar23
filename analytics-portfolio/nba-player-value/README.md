# Lakers scoring per salary dollar

## Business question

A cheap point is not the whole player.

## Explore

Open [dashboard.html](dashboard.html) in a browser. The dashboard works offline. See [results.json](results.json) for full generated results and [analysis.sql](analysis.sql) for queries.

## Method

Parse salary currency → require positive salary, at least 20 games and 15 minutes/game → divide PPG by annual salary in millions → rank eligible players.

## Observed finding

At the baseline filter, Cam Reddish had the highest PPG per salary million among eligible players (3.095), followed by Max Christie (2.907) and Christian Wood (2.546). This does not establish that they were the best players or best contracts; the result is strongly affected by low salaries and ignores defense.

## Interpretation

Low-salary players lead this scoring-cost proxy. That illustrates the effect of contract structure, not a complete ranking of basketball value.

## Limitations

Lakers only. Partial-season statistics; exact snapshot cutoff unverified. Salary is annual but points are per game. This metric omits defense, availability, playmaking and contract constraints. Controls tighten the base eligibility filter; excluded raw players are not added back.

## Reproduce

From the parent portfolio folder, run `python build.py` then `python make_dashboards.py`. Python 3.10+, standard library only. Source data and fingerprints are documented in the parent README and results JSON.

## Provenance

https://raw.githubusercontent.com/AggieSportsAnalytics/NBASalaryAnalysis/main/LakersMergedData.csv

This is an AI-assisted portfolio exercise. No claim of implemented business impact.
