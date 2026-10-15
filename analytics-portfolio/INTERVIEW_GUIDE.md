# Interview preparation

Be accurate about ownership: these are AI-assisted portfolio exercises. Run the scripts, inspect the outputs, and change a query yourself before saying you can explain the implementation. Do not claim the recommendations were adopted or generated real revenue.

## Retail: 45-second explanation

“I looked at whether strong sales were masking weak profit. I validated the file first and found auxiliary tables appended below the order data. I kept valid order lines, checked unique line IDs, and calculated sales-weighted margin by product category. I used the results to prioritize investigation, rather than assume the largest sales category was the healthiest.”

- Why `SUM(profit)/SUM(sales)`? It gives each dollar equal weight; averaging row margins overweights small transactions.
- Why distinct order IDs for average order value? One order can have many product lines.
- Does discount cause losses? This descriptive analysis cannot establish causation. Product mix, geography, and other confounders can explain the relationship.
- What next? Inspect discount and cost policies in weak subcategories, then test a targeted change with revenue and profit guardrails.
- Practice: modify `analysis.sql` to calculate monthly revenue growth using `LAG` and explain the first month's NULL.

## Retention: 45-second explanation

“I grouped customers by their first observed purchase month and measured purchasing in exact later months. I deduplicated customer-month activity so multiple purchases did not inflate retention. I excluded future months from the comparison and included observable zero-activity cells. That makes the denominator defensible.”

- First observed customer is not necessarily a new customer. Purchases before the dataset begins are unknown (left censoring).
- Month-one retention means purchasing in the next calendar month, not within 30 days and not any time in the future.
- Why not average cohort percentages? Use eligible customer counts to calculate a size-weighted aggregate.
- Why not fill future months with zero? They have not happened in the observation window (right censoring).
- No acquisition-channel field exists. Do not invent channel attribution or recommend a channel budget shift.
- Practice: change offsets to include month 4 and explain why eligible denominators differ by horizon.

## NBA: 45-second explanation

“I used a historical Lakers salary and box-score snapshot to build a transparent scoring-per-salary metric. I restricted the analysis to players with at least 20 games and 15 minutes per game. The main lesson was that an easy-to-explain metric can be useful for screening while still missing much of basketball value.”

- Points per game divided by salary in millions is a scoring-cost proxy, not wins added or overall value.
- Rookie/minimum contracts structurally look favorable; veteran maximum salaries reflect many skills beyond scoring.
- Stats are partial-season averages and salary is annual. This is not total points per dollar and does not fully penalize injuries.
- Do not generalize a Lakers-only sample to all NBA players. The exact scrape cutoff is unverified.
- Practice: change the minimum games to 40 and inspect ranking sensitivity. Then propose a better metric including defense and availability, without claiming it is already implemented.

## Questions to prepare for

1. What was the row grain, and how did you avoid double counting?
2. Which quality issue changed your analysis?
3. What decision could this support, and what evidence is still missing?
4. Which assumption would most change the answer?
5. Walk through one SQL CTE and explain the join keys.

## A focused 60-minute review

- 0–15 minutes: run `build.py`, inspect CSVs, reconcile headline totals.
- 15–35: read and modify retail/retention SQL in `analysis.sqlite`.
- 35–45: open dashboards; explain one finding and limitation per project.
- 45–60: deliver each explanation aloud and answer the five questions above.
