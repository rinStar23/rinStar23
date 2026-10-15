SELECT subcategory, COUNT(*) AS lines, ROUND(SUM(sales),2) AS revenue, ROUND(SUM(profit),2) AS profit, ROUND(100.0*SUM(profit)/NULLIF(SUM(sales),0),2) AS margin_pct FROM orders GROUP BY subcategory ORDER BY profit;

-- Weighted margin, not the average of line margins.
SELECT region,SUM(sales) revenue,SUM(profit) profit,100.0*SUM(profit)/NULLIF(SUM(sales),0) margin_pct FROM orders GROUP BY region;

SELECT substr(order_date,1,7) month,SUM(sales) revenue,SUM(profit) profit FROM orders GROUP BY month ORDER BY month;
