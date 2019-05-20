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
/MemTotal/{
$3="GB"
$2=sprintf("%.0f",$2/1048576)
print
$1="  Mem80%:"
$2=sprintf("%.0f",$2*.8)
print
}' /proc/meminfo
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
```

