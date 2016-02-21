
import sys
import csv

def _sql(rec):
  return """
INSERT INTO ts_data (start,stop,category,desc,adj) 
  VALUES (%s, %s, \"%s\", \"%s\", %s); 
""" % tuple(rec)

sqlfile = sys.argv[1] if len(sys.argv)>0 else None

infields = ('start','stop','category','desc','adj')
inrecs = csv.reader(sys.stdin, delimiter='|')

print "BEGIN TRANSACTION;"
print """
CREATE TABLE IF NOT EXISTS ts_data (
  start INT(10), 
  stop INT(10), 
  category VARCHAR(255), 
  desc VARCHAR(255), 
  adj INT(10)
);
CREATE INDEX IF NOT EXISTS ts_data_category ON ts_data (category);

DROP VIEW IF EXISTS timesheets;
CREATE VIEW timesheets AS 
  SELECT *,
         (((stop-start)/60.0) + adj)/60.0 as tot_hrs,
         ((stop-start)/60.0) + adj  as tot_mins,
         (((stop-start)/60) + adj)/60 as hrs,
         (((stop-start)/60) + adj)%60 as mins,
         date(start,'unixepoch','localtime') as start_date,
         date(stop,'unixepoch','localtime') as stop_date,
         date(start,'unixepoch','localtime','weekday 0','-6 days') as start_week,
         date(start,'unixepoch','localtime','start of month') as start_month,
         cast(julianday('now','localtime','start of day') - 
              julianday(start,'unixepoch','localtime','start of day') as int)
           as start_days_ago,
         cast(julianday('now','localtime','start of day','weekday 0','-6 days') - 
              julianday(start,'unixepoch','localtime','start of day','weekday 0','-6 days') as int)/7
           as start_weeks_ago
  FROM ts_data
;
"""

print "DELETE FROM ts_data;"

for stmt in map(_sql, inrecs):
  print stmt

print "COMMIT TRANSACTION;"

if sqlfile:
  with open(sqlfile,'rb') as f:
    print f.read()

