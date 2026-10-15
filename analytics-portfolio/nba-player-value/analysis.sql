-- Optional SQLite query after importing player_results.csv as players.
SELECT player,salary,points_per_game,ROUND(points_per_game/(salary/1000000.0),3) AS points_per_salary_million FROM players WHERE games>=20 AND minutes_per_game>=15 AND salary>0 ORDER BY points_per_salary_million DESC;
