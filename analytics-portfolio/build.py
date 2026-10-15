"""Reproduce all analyses with Python 3.10+; standard library only."""
from pathlib import Path
import csv, json, sqlite3, hashlib, urllib.request, datetime, shutil
ROOT=Path(__file__).resolve().parent
SOURCES={'retail-sales':'https://raw.githubusercontent.com/leonism/sample-superstore/master/data/superstore.csv','nba-player-value':'https://raw.githubusercontent.com/AggieSportsAnalytics/NBASalaryAnalysis/main/LakersMergedData.csv'}
def source(name):
 p=ROOT/name/'source.csv'
 if not p.exists():
  with urllib.request.urlopen(SOURCES[name],timeout=45) as r:p.write_bytes(r.read())
 return p
def writecsv(path,rows):
 if rows:
  with path.open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def query(db,sql):return [dict(r) for r in db.execute(sql)]
def save(name,report,tables):
 p=ROOT/name;p.mkdir(exist_ok=True)
 (p/'results.json').write_text(json.dumps(report,indent=2))
 for n,rows in tables.items():writecsv(p/(n+'.csv'),rows)
 return report
p=source('retail-sales');raw=list(csv.DictReader(p.open()))
rows=[];excluded=0;seen=set()
for r in raw:
 if not (r['Row ID'] or '').isdigit():excluded+=1;continue
 if r['Row ID'] in seen:raise ValueError('Duplicate line ID')
 seen.add(r['Row ID']);dt=datetime.datetime.strptime(r['Order Date'],'%m/%d/%Y').date()
 rows.append((int(r['Row ID']),r['Order ID'],dt.isoformat(),r['Customer ID'],r['Region'],r['Category'],r['Sub-Category'],float(r['Sales']),float(r['Profit']),float(r['Discount']),int(r['Quantity'])))
db=sqlite3.connect(':memory:');db.row_factory=sqlite3.Row
db.execute('CREATE TABLE orders(line_id INTEGER PRIMARY KEY,order_id TEXT,order_date TEXT,customer_id TEXT,region TEXT,category TEXT,subcategory TEXT,sales REAL,profit REAL,discount REAL,quantity INTEGER)')
db.executemany('INSERT INTO orders VALUES(?,?,?,?,?,?,?,?,?,?,?)',rows)
retail_sql='''SELECT subcategory, COUNT(*) AS lines, ROUND(SUM(sales),2) AS revenue, ROUND(SUM(profit),2) AS profit, ROUND(100.0*SUM(profit)/NULLIF(SUM(sales),0),2) AS margin_pct FROM orders GROUP BY subcategory ORDER BY profit;'''
(ROOT/'retail-sales'/'analysis.sql').write_text(retail_sql+'\n\n-- Weighted margin, not the average of line margins.\nSELECT region,SUM(sales) revenue,SUM(profit) profit,100.0*SUM(profit)/NULLIF(SUM(sales),0) margin_pct FROM orders GROUP BY region;\n\nSELECT substr(order_date,1,7) month,SUM(sales) revenue,SUM(profit) profit FROM orders GROUP BY month ORDER BY month;\n')
sub=query(db,retail_sql);region=query(db,'SELECT region,ROUND(SUM(sales),2) revenue,ROUND(SUM(profit),2) profit FROM orders GROUP BY region');monthly=query(db,"SELECT substr(order_date,1,7) month,ROUND(SUM(sales),2) revenue,ROUND(SUM(profit),2) profit FROM orders GROUP BY month ORDER BY month")
k=query(db,'SELECT COUNT(*) lines,COUNT(DISTINCT order_id) orders,COUNT(DISTINCT customer_id) customers,ROUND(SUM(sales),2) revenue,ROUND(SUM(profit),2) profit,ROUND(100.0*SUM(profit)/SUM(sales),2) margin_pct,MIN(order_date) start,MAX(order_date) end FROM orders')[0]
retail=save('retail-sales',{'title':'Retail profit diagnostic','source':SOURCES['retail-sales'],'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'quality':{'parsed_rows':len(raw),'excluded_non_order_rows':excluded,'valid_lines':len(rows),'unique_line_ids':len(seen)},'metrics':k,'subcategories':sub,'regions':region,'monthly':monthly},{'subcategory_results':sub,'monthly_results':monthly})
# Months since first observed purchase; collapse multiple lines and orders per customer-month.
cohort_sql='''WITH active AS (SELECT DISTINCT customer_id,CAST(substr(order_date,1,4) AS INTEGER)*12+CAST(substr(order_date,6,2) AS INTEGER)-1 AS month FROM orders), first_seen AS (SELECT customer_id,MIN(month) cohort FROM active GROUP BY customer_id), sizes AS (SELECT cohort,COUNT(*) cohort_size FROM first_seen GROUP BY cohort), cutoff AS (SELECT MAX(month) last_month FROM active), offsets AS (SELECT 0 n UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 6 UNION ALL SELECT 12), counts AS (SELECT f.cohort,a.month-f.cohort month_offset,COUNT(*) active_customers FROM active a JOIN first_seen f USING(customer_id) GROUP BY f.cohort,month_offset) SELECT s.cohort,o.n month_offset,s.cohort_size,COALESCE(c.active_customers,0) active_customers,ROUND(100.0*COALESCE(c.active_customers,0)/s.cohort_size,2) retention_pct FROM sizes s CROSS JOIN offsets o CROSS JOIN cutoff t LEFT JOIN counts c ON c.cohort=s.cohort AND c.month_offset=o.n WHERE s.cohort+o.n<=t.last_month ORDER BY s.cohort,o.n;'''
(ROOT/'customer-retention'/'analysis.sql').write_text('-- SQLite. First-observed cohort; right-censored cells omitted.\n'+cohort_sql)
coh=query(db,cohort_sql)
for r in coh:r['cohort']=f"{r['cohort']//12:04d}-{r['cohort']%12+1:02d}"
summary=[]
for n in [0,1,2,3,6,12]:
 a=[r for r in coh if r['month_offset']==n];den=sum(r['cohort_size'] for r in a);num=sum(r['active_customers'] for r in a)
 summary.append({'month_offset':n,'eligible_customers':den,'active_customers':num,'retention_pct':round(100*num/den,2)})
ret=save('customer-retention',{'title':'Customer cohort retention','source':SOURCES['retail-sales'],'metrics':{'customers':k['customers'],'cohorts':len({r['cohort'] for r in coh}),'definition':'Purchase in exact month N after first observed purchase; not cumulative repeat rate.','observation_end':k['end']},'summary':summary,'cohorts':coh},{'cohort_results':coh,'retention_summary':summary})
# Validate cohort identity and bounds; catches repeated-order inflation and censoring errors.
assert all(r['active_customers']<=r['cohort_size'] for r in coh)
assert all(r['retention_pct']==100 for r in coh if r['month_offset']==0)
assert k['lines']==len(seen) and k['orders']<k['lines']
np=source('nba-player-value');nr=list(csv.DictReader(np.open()));players=[];dropped=[]
for r in nr:
 try:
  salary=float(r['2023-24'].replace('$','').replace(',',''));g=int(r['G']);mp=float(r['MP']);pts=float(r['PTS'])
  if salary<=0 or g<20 or mp<15: dropped.append(r['Player']);continue
  players.append({'player':r['Player'],'salary':salary,'games':g,'minutes_per_game':mp,'points_per_game':pts,'rebounds_per_game':float(r['TRB']),'assists_per_game':float(r['AST']),'points_per_salary_million':round(pts/(salary/1e6),3)})
 except (ValueError,KeyError):dropped.append(r['Player'])
players.sort(key=lambda x:x['points_per_salary_million'],reverse=True)
assert len({x['player'] for x in players})==len(players)
nba=save('nba-player-value',{'title':'Lakers scoring per salary dollar','source':SOURCES['nba-player-value'],'sha256':hashlib.sha256(np.read_bytes()).hexdigest(),'metrics':{'input_players':len(nr),'eligible_players':len(players),'excluded_players':len(dropped),'season':'2023–24 salary / partial-season stats snapshot; exact cutoff unverified'},'players':players,'excluded':dropped},{'player_results':players})
(ROOT/'nba-player-value'/'analysis.sql').write_text('-- Optional SQLite query after importing player_results.csv as players.\nSELECT player,salary,points_per_game,ROUND(points_per_game/(salary/1000000.0),3) AS points_per_salary_million FROM players WHERE games>=20 AND minutes_per_game>=15 AND salary>0 ORDER BY points_per_salary_million DESC;\n')
# Store cleaned SQLite data locally for inspection (ignored; regenerate with build.py).
db.commit()
backup=sqlite3.connect(ROOT/'analysis.sqlite');db.backup(backup);backup.close()
all_reports={'retail':retail,'retention':ret,'nba':nba}
(ROOT/'reports.json').write_text(json.dumps(all_reports))
print(json.dumps({'retail':k,'quality':retail['quality'],'retention':summary,'nba':players[:3]},indent=2))
