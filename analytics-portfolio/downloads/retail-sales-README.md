# Retail profit diagnostic

## Business question

Where revenue hides weak profit.

## Explore

Open [dashboard.html](dashboard.html) in a browser. The dashboard works offline. See [results.json](results.json) for full generated results and [analysis.sql](analysis.sql) for queries.

## Method

Validate line IDs → exclude 806 appended auxiliary rows → parse dates and amounts → aggregate by subcategory → calculate SUM(profit) / SUM(sales).

## Observed finding

Tables generated $206,965.53 in sales but lost $17,725.48 (−8.56% margin). Overall margin was 12.47%. Prioritize a review of pricing, discount levels and cost allocation in Tables; this is a diagnostic recommendation, not an estimate of recoverable profit.

## Interpretation

Profit is uneven across product groups. Investigate loss-making lines before pursuing more revenue in those groups.

## Limitations

Descriptive sample data. Profit uses the source definition; shipping overhead and attribution are unverified. Discount effects are associations, not causal estimates.

## Reproduce

From the parent portfolio folder, run `python build.py` then `python make_dashboards.py`. Python 3.10+, standard library only. Source data and fingerprints are documented in the parent README and results JSON.

## Provenance

https://raw.githubusercontent.com/leonism/sample-superstore/master/data/superstore.csv

This is an AI-assisted portfolio exercise. No claim of implemented business impact.
