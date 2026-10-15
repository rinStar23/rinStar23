# Customer cohort retention

## Business question

A return visit needs the right denominator.

## Explore

Open [dashboard.html](dashboard.html) in a browser. The dashboard works offline. See [results.json](results.json) for full generated results and [analysis.sql](analysis.sql) for queries.

## Method

Deduplicate customer-month activity → determine first-observed month → build eligible cohort-offset grid → left join activity → divide by cohort size. Observable zero-activity cells are retained.

## Observed finding

79 of 793 eligible customers purchased in month 1 (9.96%). At month 12, 91 of 782 eligible customers purchased (11.64%). These different denominators reflect observation eligibility. The rates measure exact-month activity, so they need not decline monotonically.

## Interpretation

Monthly purchasing is intermittent. Exact-month retention is not subscription survival or cumulative repeat purchase.

## Limitations

First purchase means first observed in this file. Previous purchases are unknown. Future cells are omitted, not treated as zero. The final December observation ends on December 30. No acquisition-channel attribution is available.

## Reproduce

From the parent portfolio folder, run `python build.py` then `python make_dashboards.py`. Python 3.10+, standard library only. Source data and fingerprints are documented in the parent README and results JSON.

## Provenance

https://raw.githubusercontent.com/leonism/sample-superstore/master/data/superstore.csv

This is an AI-assisted portfolio exercise. No claim of implemented business impact.
