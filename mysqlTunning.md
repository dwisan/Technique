> MySQL Server Hardware and OS Tuning:
```
```
MySQL Schema Optimization:
```
```
Query Optimization:
```
```
> MySQL Configuration:
```
- [x] Key: innodb_buffer_pool_size

Catagory: Innodb Engine
Description : used for caching data and indexes in memory
Value : On a dedicated box, value of 60%-70% of RAM
Example:
  innodb_buffer_pool_size=1G

Calulate:

awk '
/MemAvail/{
$3="G";_=$2
$2=sprintf("% 3.0f",_/1048576)
print
for (i=80;i>=25;i-=10) {
$1="MemAvail_"i"%:"
$2=sprintf("% 3.0f",_*(i/100)/1048576)
$4=sprintf("| %.0f M",_*(i/100)/1024)
print
}
}' /proc/meminfo
```

```
- [x] Key: innodb_buffer_pool_instances

Catagory: Innodb Engine
Description : directive controls the number of memory pages Innodb creates
Value : equal CPU Core (should not exceed Total_IO_Threads)
Example:
  innodb_buffer_pool_instances=8

Calulate:
Total_IO_Threads = (innodb_read_io_threads + innodb_write_io_threads)
```

```
- [x] Key: innodb_read_io_threads , innodb_write_io_threads

Catagory: Innodb Engine
Description : Input/Output threads are sub-processes of MySQL 
              which directly access the IBP memory pages
Value : innodb_read_io_threads + innodb_write_io_threads = CPU Core = innodb_buffer_pool_instances

Example: if have CPU 8 core
  
  case: Write_Heavy:Read_Heavy = 1:1
     innodb_read_io_threads=4
     innodb_write_io_threads=4
  
  case: Write_Heavy:Read_Heavy = 2:1
     innodb_read_io_threads=2
     innodb_write_io_threads=6
  
  case: Write_Heavy:Read_Heavy = 1:2
     innodb_read_io_threads=6
     innodb_write_io_threads=2
     
Calculate:

Total_Reads = Com_select
SHOW GLOBAL STATUS LIKE 'Com_select';

Total_Writes = Com_delete + Com_insert + Com_replace + Com_update
SHOW GLOBAL STATUS WHERE Variable_name IN ('Com_insert', 'Com_update', 'Com_replace', 'Com_delete');

mysql -uroot -p -e 'SHOW GLOBAL STATUS;'|\
awk '
$1~/Com_(delete|insert|update|replace)$/{
w += $2
printf $0 "\t + Total_Writes = " w "\n"
}
$1~/Com_(select)/{
r += $2
printf $0 "\t + Total_Reads = " r "\n"
}
END {
printf "\nRead:Write Ratio:\n\t" r ":" w " "
if (r >= w) {
R=sprintf("%.0f",r/w)
print R ":1"
} else {
W=sprintf("%.0f",w/r)
print "1:" W
}
}'

```

```
- [x] Key: max_connections

Catagory: Global
Description : how many concurrent connections are permitted.
Value : apply depends on your particular MySQL/MariaDB usage.
Example:
  max_connections = 300
```

```
- [x] Key: skip-name-resolve

Catagory: Global
Description : disable the reverse DNS lookup 
Value : -
Example:
  skip-name-resolve
```

```
- [x] Key: tmp_table_size , max_heap_table_size

Catagory: Global
Description : help you prevent disk writes
Value : giving 64M for both values for every GB of RAM on the server
Example:
  tmp_table_size = 64M
  max_heap_table_size = 64M

find Tuning:

*Find out current value of tmp_table_size
mysql> show global variables like 'tmp_table_size';

*Find out percentage of tables created on disk
mysql> show global status like 'created_tmp_disk_tables';
mysql> show global status like 'created_tmp_tables';

Tmp_disk_tables=((created_tmp_disk_tables*100/(created_tmp_tables+created_tmp_disk_tables))


```

