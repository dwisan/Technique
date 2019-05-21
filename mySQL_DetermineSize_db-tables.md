> database size
```
SELECT table_schema AS "Database", 
ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS "Size (MB)" 
FROM information_schema.TABLES 
GROUP BY table_schema;
```
> database size with engine MyISAM
```
SELECT table_schema AS "Database", 
ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS "Size (MB)" 
FROM information_schema.TABLES
WHERE ENGINE='MyISAM'
GROUP BY table_schema;
```
> tables size in a databases
```
SELECT table_name AS "Table",
ROUND(((data_length + index_length) / 1024 / 1024), 2) AS "Size (MB)"
FROM information_schema.TABLES
WHERE table_schema = "database_name"
ORDER BY (data_length + index_length) DESC;
```
> calculate key buffer size of myisam
```
SELECT CONCAT(ROUND(KBS/POWER(1024,
IF(PowerOf1024<0,0,IF(PowerOf1024>3,0,PowerOf1024)))+0.4999),
SUBSTR(' KMG',IF(PowerOf1024<0,0,
IF(PowerOf1024>3,0,PowerOf1024))+1,1))
recommended_key_buffer_size FROM
(SELECT LEAST(POWER(2,32),KBS1) KBS
FROM (SELECT SUM(index_length) KBS1
FROM information_schema.tables
WHERE engine='MyISAM' AND
table_schema NOT IN ('information_schema','mysql')) AA ) A,
(SELECT 2 PowerOf1024) B;
```
