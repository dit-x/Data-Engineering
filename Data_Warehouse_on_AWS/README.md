# Implementing Data Warehouse on AWS
# Sparkify Database Warehouse
# Project Overview
This project is about a music streaming startup, `Sparkify` that want to move their processes and data into cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

This project ETL and data warehouse has been built on AWS, staging table hosted on AWS Redshift and with a PostgreSQL. I have provided the schema and ETL that extract the data from AWS S3, stages them in Redshift and transfroms data into a set of dimensional tables. Star Schema was used for the dimension modeling to allow Sparkify team to easily run queries to find insights in what songs their users are listening to. The scripts used in the project have been created in Python.

# The schema for the Song Play Analysis
Using the song and log datasets, I’ve created a star schema optimized for queries on song play analysis. This includes the following tables.

## Fact Table
**songplays —** records in log data associated with song plays i.e. records with page `NextSong`
*songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent*

## Dimension Tables
**users —** users in the app
*user_id, first_name, last_name, gender, level*

**songs —** songs in the music database
*song_id, title, artist_id, year, duration*

**artists —** artists in the music database
*artist_id, name, location, latitude, longitude*

**time —** timestamps of records in songplays broken down into the specific unit
*start_time, hour, day, week, month, year, weekday*

I added constrains and condition on the columns when creating the relational database. Below is the schema diagram for `Sparkify Database`

![Screenshot (148)](https://user-images.githubusercontent.com/55639062/78468855-5e654300-7713-11ea-835a-54c1f0cdf048.png)

# Project Structure
The project contains five files:
1. `test.ipynb` displays the first few rows of each table to check the database.
1. `create_tables.py` drops and creates all tables in Redshift (i.e, the staging table and the Analytics table). I run this file to reset my tables before each time I run my ETL scripts.
1. `etl.py` defines the ETL pipeline that extract data from S3, loads it into the staging table on Redshift and transfrom into the analytics table on Redshift
1. `sql_queries.py` defines SQL queries that creates the tables and ETL pipeline
1. `connectToCluster.ipynb` makes connection to Reddhift to execute the ETL and run queries

# Project Parameters
You will need to create a configuration file with the file name `dwh.cfg` and the following structure:

```
[CLUSTER]
HOST=<your_host>
DB_NAME=<your_db_name>
DB_USER=<your_db_user>
DB_PASSWORD=<your_db_password>
DB_PORT=<your_db_port>
DB_REGION=<your_db_region>
CLUSTER_IDENTIFIER=<your_cluster_identifier>

[IAM_ROLE]
ARN=<your_iam_role_arn>

[S3]
LOG_DATA='s3://udacity-dend/log_data'
LOG_JSONPATH='s3://udacity-dend/log_json_path.json'
SONG_DATA='s3://udacity-dend/song_data'

[AWS]
ACCESS_KEY=<your_access_key>
SECRET_KEY=<your_secret_key>
```

# Project Procedure
1. Define your parameter in `dwh.cfg file`
1. Write the neccessary SQL to get the ETL processes done in `sql_queries.py`
    * start with the staging tabele creation
    * Be sure data is loaded in the staging table from S3 without error
    * Then create the analytics/dimension table
    * `Best practice, use .ipynb file to do this step by step. It helps in error troubleshooting`
1. Run `create_tables.py` every time before running etl.py to clean and create daabase
1. Run `etl.py` to start ETL pipeline

# Create Table and SQL queries
The major focus of this project is on the `sql_queries.py`, this is where all tables are created and where the ETL pipeline processes are written. To start, I created and connected to AWS Redshift and S3. After connection, I loaded data from the S3 to staging table on Redshift. 

It is `important` to know that the stage table was created knowing fully well what kind of data is in the file (in this case, JSON files). This is to avoid error when loading data into the stage tables.

Once the tables were created (staging and analytics table), I wrote the ETL to load the data into stage table and transform into analytics table.

## Query Examples
Here is the code that `creates staging_events_table`
``` sql
CREATE TABLE  staging_events_table (
            artist varchar,
            auth varchar NOT NULL,
            first_name varchar,
            gender char (1),
            itemInSession int NOT NULL,
            last_name varchar,
            length numeric,
            level varchar NOT NULL,
            location varchar,
            method varchar NOT NULL,
            page varchar NOT NULL,
            registration numeric,
            session_id int NOT NULL,
            song varchar,
            status int NOT NULL,
            ts numeric NOT NULL,
            user_agent varchar,
            user_id int
        )
```

Here is the code that `load data into staging_events_table`
``` python
"""
    copy staging_events_table from {}
    iam_role '{}'
    format as json {}
""".format(
    config.get("S3", "LOG_DATA"),
    ARN,
    config.get("S3", "LOG_JSONPATH")
    )
)
```

Here is the code that `extract from staging_events_table to users table`
```sql
INSERT INTO users(User_id, first_name, 
    last_name, gender, level )
SELECT    
    se.user_id,
    se.first_name,
    se.last_name,
    se.gender,
    se.level
FROM staging_events_table se
WHERE se.page = 'NextSong'
```

