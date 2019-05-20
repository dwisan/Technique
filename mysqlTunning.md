```
Key : innodb_buffer_pool_size

Catagory: Innodb Engine
Description : used for caching data and indexes in memory
Value : On a dedicated box, value of 60%-70% of RAM
Example:
  innodb_buffer_pool_size=1G
```

```
Key : max_connections

Catagory: Global
Description : how many concurrent connections are permitted.
Value : apply depends on your particular MySQL/MariaDB usage.
Example:
  max_connections = 300
```
