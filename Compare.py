```sql
CREATE TABLE
    data_interrogation.test_table_myisam
    (
        index_col BIGINT NOT NULL AUTO_INCREMENT,
        value1 DOUBLE,
        value2 DOUBLE,
        value3 DOUBLE,
        value4 DOUBLE,
        PRIMARY KEY (index_col)
    )
    ENGINE=MyISAM DEFAULT CHARSET=utf8

CREATE TABLE
    subselect_myisam
    (
        index_col bigint NOT NULL,
        non_index_col bigint,
        PRIMARY KEY (index_col)
    )
    ENGINE=MyISAM DEFAULT CHARSET=utf8;
```
>Vanilla selects

```python
import timeit
import MySQLdb
import MySQLdb.cursors
import random
from random import randint

db = MySQLdb.connect(host="...", user="...", passwd="...", db="...", cursorclass=MySQLdb.cursors.DictCursor)
cur = db.cursor()

lengthOfTable = 100000

# Fill up the tables with random data
for x in xrange(lengthOfTable):
    rand1 = random.random()
    rand2 = random.random()
    rand3 = random.random()
    rand4 = random.random()

    insertString = "INSERT INTO test_table_innodb (value1,value2,value3,value4) VALUES (" + str(rand1) + "," + str(rand2) + "," + str(rand3) + "," + str(rand4) + ")"
    insertString2 = "INSERT INTO test_table_myisam (value1,value2,value3,value4) VALUES (" + str(rand1) + "," + str(rand2) + "," + str(rand3) + "," + str(rand4) + ")"
    insertString3 = "INSERT INTO test_table_memory (value1,value2,value3,value4) VALUES (" + str(rand1) + "," + str(rand2) + "," + str(rand3) + "," + str(rand4) + ")"

    cur.execute(insertString)
    cur.execute(insertString2)
    cur.execute(insertString3)

db.commit()

# Define a function to pull a certain number of records from these tables
def selectRandomRecords(testTable,numberOfRecords):

    for x in xrange(numberOfRecords):
        rand1 = randint(0,lengthOfTable)

        selectString = "SELECT * FROM " + testTable + " WHERE index_col = " + str(rand1)
        cur.execute(selectString)

setupString = "from __main__ import selectRandomRecords"

# Test time taken using timeit
myisam_times = []
innodb_times = []
memory_times = []

for theLength in [3,10,30,100,300,1000,3000,10000]:

    innodb_times.append( timeit.timeit('selectRandomRecords("test_table_innodb",' + str(theLength) + ')', number=100, setup=setupString) )
    myisam_times.append( timeit.timeit('selectRandomRecords("test_table_myisam",' + str(theLength) + ')', number=100, setup=setupString) )
    memory_times.append( timeit.timeit('selectRandomRecords("test_table_memory",' + str(theLength) + ')', number=100, setup=setupString) )
```
>Counts
```python
myisam_times = []
innodb_times = []
memory_times = []

# Define a function to count the records
def countRecords(testTable):

    selectString = "SELECT count(*) FROM " + testTable
    cur.execute(selectString)

setupString = "from __main__ import countRecords"

# Truncate the tables and re-fill with a set amount of data
for theLength in [3,10,30,100,300,1000,3000,10000,30000,100000]:

    truncateString = "TRUNCATE test_table_innodb"
    truncateString2 = "TRUNCATE test_table_myisam"
    truncateString3 = "TRUNCATE test_table_memory"

    cur.execute(truncateString)
    cur.execute(truncateString2)
    cur.execute(truncateString3)

    for x in xrange(theLength):
        rand1 = random.random()
        rand2 = random.random()
        rand3 = random.random()
        rand4 = random.random()

        insertString = "INSERT INTO test_table_innodb (value1,value2,value3,value4) VALUES (" + str(rand1) + "," + str(rand2) + "," + str(rand3) + "," + str(rand4) + ")"
        insertString2 = "INSERT INTO test_table_myisam (value1,value2,value3,value4) VALUES (" + str(rand1) + "," + str(rand2) + "," + str(rand3) + "," + str(rand4) + ")"
        insertString3 = "INSERT INTO test_table_memory (value1,value2,value3,value4) VALUES (" + str(rand1) + "," + str(rand2) + "," + str(rand3) + "," + str(rand4) + ")"

        cur.execute(insertString)
        cur.execute(insertString2)
        cur.execute(insertString3)

    db.commit()

    # Count and time the query
    innodb_times.append( timeit.timeit('countRecords("test_table_innodb")', number=100, setup=setupString) )
    myisam_times.append( timeit.timeit('countRecords("test_table_myisam")', number=100, setup=setupString) )
    memory_times.append( timeit.timeit('countRecords("test_table_memory")', number=100, setup=setupString) )
```
>Conditional selects
```python
myisam_times = []
innodb_times = []
memory_times = []

# Define a function to perform conditional selects
def conditionalSelect(testTable):
    selectString = "SELECT * FROM " + testTable + " WHERE value1 < 0.5 AND value2 < 0.5 AND value3 < 0.5 AND value4 < 0.5"
    cur.execute(selectString)

setupString = "from __main__ import conditionalSelect"

# Truncate the tables and re-fill with a set amount of data
for theLength in [3,10,30,100,300,1000,3000,10000,30000,100000]:

    truncateString = "TRUNCATE test_table_innodb"
    truncateString2 = "TRUNCATE test_table_myisam"
    truncateString3 = "TRUNCATE test_table_memory"

    cur.execute(truncateString)
    cur.execute(truncateString2)
    cur.execute(truncateString3)

    for x in xrange(theLength):
        rand1 = random.random()
        rand2 = random.random()
        rand3 = random.random()
        rand4 = random.random()

        insertString = "INSERT INTO test_table_innodb (value1,value2,value3,value4) VALUES (" + str(rand1) + "," + str(rand2) + "," + str(rand3) + "," + str(rand4) + ")"
        insertString2 = "INSERT INTO test_table_myisam (value1,value2,value3,value4) VALUES (" + str(rand1) + "," + str(rand2) + "," + str(rand3) + "," + str(rand4) + ")"
        insertString3 = "INSERT INTO test_table_memory (value1,value2,value3,value4) VALUES (" + str(rand1) + "," + str(rand2) + "," + str(rand3) + "," + str(rand4) + ")"

        cur.execute(insertString)
        cur.execute(insertString2)
        cur.execute(insertString3)

    db.commit()

    # Count and time the query
    innodb_times.append( timeit.timeit('conditionalSelect("test_table_innodb")', number=100, setup=setupString) )
    myisam_times.append( timeit.timeit('conditionalSelect("test_table_myisam")', number=100, setup=setupString) )
    memory_times.append( timeit.timeit('conditionalSelect("test_table_memory")', number=100, setup=setupString) )
```
>Sub-selects
```python
myisam_times = []
innodb_times = []
myisam_times_2 = []
innodb_times_2 = []

def subSelectRecordsIndexed(testTable,testSubSelect):
    selectString = "SELECT * FROM " + testTable + " WHERE index_col in ( SELECT index_col FROM " + testSubSelect + " )"
    cur.execute(selectString)

setupString = "from __main__ import subSelectRecordsIndexed"

def subSelectRecordsNotIndexed(testTable,testSubSelect):
    selectString = "SELECT * FROM " + testTable + " WHERE index_col in ( SELECT non_index_col FROM " + testSubSelect + " )"
    cur.execute(selectString)

setupString2 = "from __main__ import subSelectRecordsNotIndexed"

# Truncate the old tables, and re-fill with 1000000 records
truncateString = "TRUNCATE test_table_innodb"
truncateString2 = "TRUNCATE test_table_myisam"

cur.execute(truncateString)
cur.execute(truncateString2)

lengthOfTable = 1000000

# Fill up the tables with random data
for x in xrange(lengthOfTable):
    rand1 = random.random()
    rand2 = random.random()
    rand3 = random.random()
    rand4 = random.random()

    insertString = "INSERT INTO test_table_innodb (value1,value2,value3,value4) VALUES (" + str(rand1) + "," + str(rand2) + "," + str(rand3) + "," + str(rand4) + ")"
    insertString2 = "INSERT INTO test_table_myisam (value1,value2,value3,value4) VALUES (" + str(rand1) + "," + str(rand2) + "," + str(rand3) + "," + str(rand4) + ")"

    cur.execute(insertString)
    cur.execute(insertString2)

for theLength in [3,10,30,100,300,1000,3000,10000,30000,100000]:

    truncateString = "TRUNCATE subselect_innodb"
    truncateString2 = "TRUNCATE subselect_myisam"

    cur.execute(truncateString)
    cur.execute(truncateString2)

    # For each length, empty the table and re-fill it with random data
    rand_sample = sorted(random.sample(xrange(lengthOfTable), theLength))
    rand_sample_2 = random.sample(xrange(lengthOfTable), theLength)

    for (the_value_1,the_value_2) in zip(rand_sample,rand_sample_2):
        insertString = "INSERT INTO subselect_innodb (index_col,non_index_col) VALUES (" + str(the_value_1) + "," + str(the_value_2) + ")"
        insertString2 = "INSERT INTO subselect_myisam (index_col,non_index_col) VALUES (" + str(the_value_1) + "," + str(the_value_2) + ")"

        cur.execute(insertString)
        cur.execute(insertString2)

    db.commit()

    # Finally, time the queries
    innodb_times.append( timeit.timeit('subSelectRecordsIndexed("test_table_innodb","subselect_innodb")', number=100, setup=setupString) )
    myisam_times.append( timeit.timeit('subSelectRecordsIndexed("test_table_myisam","subselect_myisam")', number=100, setup=setupString) )

    innodb_times_2.append( timeit.timeit('subSelectRecordsNotIndexed("test_table_innodb","subselect_innodb")', number=100, setup=setupString2) )
    myisam_times_2.append( timeit.timeit('subSelectRecordsNotIndexed("test_table_myisam","subselect_myisam")', number=100, setup=setupString2) )
```
