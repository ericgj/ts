CREATE TEMPORARY VIEW byall AS
  SELECT category, sum(tot_mins) as tot_mins, 
         printf("%d:%02d", sum(tot_mins)/60, sum(tot_mins)%60) as time 
    FROM timesheets
    GROUP BY category
;

CREATE TEMPORARY VIEW byweek AS
  SELECT category, sum(tot_mins) AS tot_mins,
         printf("%d:%02d", sum(tot_mins)/60, sum(tot_mins)%60) as time 
    FROM timesheets
    GROUP BY category
    HAVING start_weeks_ago < 1
;

CREATE TEMPORARY VIEW bytoday AS
  SELECT category, sum(tot_mins) AS tot_mins,
         printf("%d:%02d", sum(tot_mins)/60, sum(tot_mins)%60) as time 
    FROM timesheets
    GROUP BY category
    HAVING start_days_ago = 0
;

SELECT byall.category, byall.time as time_all, byweek.time as time_week, bytoday.time as time_today
FROM byall LEFT OUTER JOIN (
  byweek LEFT OUTER JOIN bytoday ON byweek.category = bytoday.category
) ON byall.category = byweek.category
ORDER BY byall.tot_mins DESC;


