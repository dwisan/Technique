> Databases Size 
```sql
SELECT table_schema AS "Database", 
ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS "Size (MB)" 
FROM information_schema.TABLES 
GROUP BY table_schema;
```
> databases size (MyISAM)
```sql
SELECT table_schema AS "Database", 
ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS "Size (MB)" 
FROM information_schema.TABLES
WHERE ENGINE='MyISAM'
GROUP BY table_schema;
```
> databases size (InnoDB)
```sql
SELECT table_schema AS "Database", 
ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS "Size (MB)" 
FROM information_schema.TABLES
WHERE ENGINE='InnoDB'
GROUP BY table_schema;
```
> tables size in a databases
```sql
SELECT table_name AS "Table",
ROUND(((data_length + index_length) / 1024 / 1024), 2) AS "Size (MB)"
FROM information_schema.TABLES
WHERE table_schema = "database_name"
ORDER BY (data_length + index_length) DESC;
```
> Find current appropriate key buffer size of myisam 
```sql
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
> Find current appropriate buffer pool size of innodb
```sql
SELECT CONCAT(ROUND(KBS/POWER(1024,
IF(PowerOf1024<0,0,IF(PowerOf1024>3,0,PowerOf1024)))+0.49999),
SUBSTR(' KMG',IF(PowerOf1024<0,0,
IF(PowerOf1024>3,0,PowerOf1024))+1,1)) recommended_innodb_buffer_pool_size
FROM (SELECT SUM(data_length+index_length) KBS FROM information_schema.tables
WHERE engine='InnoDB') A,
(SELECT 2 PowerOf1024) B;
```
> Calculate key_buffer_size from Index Lengths
```sql
set @overhead = 5 / 100;
select count(INDEX_LENGTH) as Indexes,
sum(INDEX_LENGTH) as Total_Index_Length,
floor(@overhead * 100) as PCT,
floor(sum(INDEX_LENGTH)*@overhead) as Overhead,
floor(sum(INDEX_LENGTH)*(1+@overhead)) as key_buffer_size
FROM information_schema.TABLES WHERE ENGINE = 'MyISAM';
```
