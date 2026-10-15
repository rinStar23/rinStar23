# Harin Pinnamaneni — Data Analyst Portfolio

Three reproducible case studies: retail profitability, customer retention, and NBA salary efficiency. These are portfolio exercises, not client engagements or claims of business impact. Built with AI assistance; interview preparation includes reviewing, running, and explaining the work.

## Run

Python 3.10+; no third-party packages required.

```bash
python build.py
python -m http.server 8000
```

Open `http://localhost:8000/retail-sales/dashboard.html` (or either other project folder). `build.py` downloads the two source files if absent, validates the data, executes SQLite queries, and regenerates result CSVs/JSON and `analysis.sqlite`. The committed dashboards embed the corresponding generated results; open them directly without a server. To refresh embedded dashboards after updating data, run `python make_dashboards.py`.

## Projects

| Project | Decision | Main methods |
|---|---|---|
| [Retail sales](retail-sales/) | Where should a retailer investigate lost profit? | Data validation, aggregation, weighted margins, SQLite |
| [Customer retention](customer-retention/) | How frequently do customers return after first observed purchase? | Cohorts, joins, CTEs, right censoring |
| [NBA player value](nba-player-value/) | Which eligible Lakers players have high scoring per salary dollar? | Salary parsing, eligibility filters, metric limitations |

Read [INTERVIEW_GUIDE.md](INTERVIEW_GUIDE.md) before presenting these projects.

## Data provenance

Retail: [leonism/sample-superstore](https://github.com/leonism/sample-superstore), `data/superstore.csv`. This is a sample dataset, not a verified production retailer. The downloaded CSV concatenates orders and auxiliary tables; nonnumeric Row IDs are excluded. Dates in this mirror differ from some other Superstore versions. Use the actual date range in `results.json`, not assumptions about the original dataset.

NBA: [AggieSportsAnalytics/NBASalaryAnalysis](https://github.com/AggieSportsAnalytics/NBASalaryAnalysis), `LakersMergedData.csv`. This project uses the existing published data, not their analysis code. 2023–24 salary fields and partial-season box-score averages; exact snapshot cutoff and upstream scrape alignment are unverified. No claim of current NBA performance.

Source data is downloaded rather than redistributed; review upstream terms before reuse. SHA-256 fingerprints in results identify the analyzed input bytes. URLs track upstream default branches, so a future download can change. Retain the original local files to reproduce an identical snapshot and compare hashes. Generated summaries are included. No proprietary or patient data is used.

## Validation

The build checks unique retail line IDs, parses all included dates/numbers, checks cohort month-zero retention equals 100%, checks active customers do not exceed cohort size, and checks unique NBA player names. These checks establish internal consistency, not upstream factual accuracy. SQL is SQLite-compatible.
