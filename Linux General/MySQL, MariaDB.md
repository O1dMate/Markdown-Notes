# Using MySQL, MariaDB

## Connecting

##### Connect to DB as root (if allowed)
```sql
sudo mysql
```

##### Connect using specific creds
```sql
mysql -u username -p
```

##### Exit from MySQL
```sql
exit
```


<br>

## Databases

##### Show all databases
```sql
SHOW databases;
```

##### Use a certain database
```sql
USE testdb;
```

##### Create a new Database
```sql
CREATE database testdb;
```

##### Create a new Table
```sql
DROP TABLE IF EXISTS sessions;

CREATE TABLE sessions (
	sessionToken VARCHAR(64) NOT NULL,
	userId INT NOT NULL,
	expirationTime DATETIME NOT NULL,
	
	PRIMARY KEY ( sessionToken ),
	FOREIGN KEY ( userId ) REFERENCES users( userId )
);
```

##### Delete a Database
```sql
DROP database db_name;
```


<br>

## Tables

##### Show all the tables in a database
```sql
SHOW tables;
```

##### Show the attributes of the table
```sql
DESCRIBE table_name;
```

##### Delete a table
```sql
DROP TABLE table_name;
```

##### Show all entries in a table
```sql
SELECT * FROM table_name;
```

##### Show all entries in a table with a constraint
```sql
SELECT * FROM table_name WHERE id > 10;
```

<br>

## Users

##### Create a new user with a password
```sql
CREATE user 'USERNAME'@'localhost' identified by 'PASSWORD';
```

##### Grant that new user full permissions on the new database
```sql
GRANT all on DB_NAME.* to 'testuser' identified by 'PASSWORD';
```

##### Show permissions for a user
```sql
SHOW grants for username;
```


<br>

## Import & Exporting

##### Exporting a DB
```sql
mysqldump -u username -p DB_NAME > output.sql
```

##### Importing a DB
```sql
mysql -u username -p DB_NAME < output.sql
```