import configparser


# CONFIG
config = configparser.ConfigParser()
config.read("dwh.cfg")
ARN = config.get("IAM_ROLE", "ARN")

# DROP TABLES

staging_events_table_drop = "drop table if exists staging_events_table"
staging_songs_table_drop = "drop table if exists staging_songs_table"
songplay_table_drop = "drop table if exists songplays"
user_table_drop = "drop table if exists users"
song_table_drop = "drop table if exists songs"
artist_table_drop = "drop table if exists artists"
time_table_drop = "drop table if exists time"


# CREATE TABLES

staging_events_table_create= ("""
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
""")

staging_songs_table_create = (""" 
     CREATE TABLE staging_songs_table (
            num_songs int NOT NULL,
            artist_id char (18) NOT NULL,
            artist_latitude varchar,
            artist_longitude varchar,
            artist_location varchar,
            artist_name varchar NOT NULL,
            song_id char (18) NOT NULL,
            title varchar NOT NULL,
            duration numeric NOT NULL,
            year int NOT NULL
        )
""")

songplay_table_create ="""CREATE TABLE IF NOT EXISTS songplays(
                        songplay_id int identity(0, 1) PRIMARY KEY,
                        start_time TIMESTAMP NOT NULL, 
                        user_id INT NOT NULL, 
                        level VARCHAR, 
                        song_id VARCHAR, 
                        artist_id VARCHAR, 
                        session_id int, 
                        location VARCHAR, 
                        user_agent VARCHAR,
                        FOREIGN KEY (song_id) REFERENCES songs(song_id),
                        FOREIGN KEY (user_id) REFERENCES users(user_id),
                        FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
                        FOREIGN KEY (start_time) REFERENCES time(start_time)
                    );"""

user_table_create = """CREATE TABLE IF NOT EXISTS users(
                        User_id INT NOT NULL PRIMARY KEY,
                        first_name VARCHAR,
                        last_name VARCHAR,
                        gender VARCHAR NOT NULL,
                        level VARCHAR
                        );"""

song_table_create = """CREATE TABLE IF NOT EXISTS songs(
                        song_id VARCHAR NOT NULL PRIMARY KEY,
                        title VARCHAR,
                        artist_id VARCHAR NOT NULL,
                        year INT NOT NULL,
                        duration FLOAT NOT NULL
                        );"""

artist_table_create = """CREATE TABLE IF NOT EXISTS artists(
                        artist_id VARCHAR NOT NULL PRIMARY KEY,
                        artist_name VARCHAR NOT NULL,
                        location VARCHAR,
                        latitude VARCHAR,
                        longitude VARCHAR
                        );"""


time_table_create = """CREATE TABLE IF NOT EXISTS time(
                        start_time TIMESTAMP NOT NULL PRIMARY KEY,
                        hour INT NOT NULL,
                        day INT NOT NULL,
                        week_of_year INT NOT NULL,
                        month INT NOT NULL,
                        year INT NOT NULL,
                        weekday INT NOT NULL
                        );"""


# STAGING TABLES

staging_events_copy = (
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


staging_songs_copy = (
"""
    copy staging_songs_table from {}
    iam_role '{}'
    json 'auto'
""".format( config.get("S3", "SONG_DATA"), ARN)
)


# FINAL TABLES

songplay_table_insert = """INSERT INTO songplays(start_time, user_id, level, 
                            song_id, artist_id, session_id, 
                            location, user_agent)
                    SELECT
                        TIMESTAMP 'epoch' + se.ts/1000 * INTERVAL '1 second' AS start_time, 
                        se.user_id, 
                        se.level, 
                        ss.song_id, 
                        ss.artist_id, 
                        se.session_id,
                        se.location,
                        se.user_agent 
                    FROM staging_events_table se
                    JOIN staging_songs_table ss ON (se.song = ss.title and se.artist = ss.artist_name)
                    WHERE se.page = 'NextSong'
                    """

user_table_insert = """INSERT INTO users(User_id, first_name, 
                        last_name, gender, level )
                    SELECT    
                        se.user_id,
                        se.first_name,
                        se.last_name,
                        se.gender,
                        se.level
                    FROM staging_events_table se
                    WHERE se.page = 'NextSong'
                    """


song_table_insert = """INSERT INTO songs
                    SELECT 
                        ss.song_id,
                        ss.title,
                        ss.artist_id,
                        ss.year,
                        ss.duration
                    FROM staging_songs_table ss
                    """

artist_table_insert =  """INSERT INTO artists
                    SELECT
                        ss.artist_id,
                        ss.artist_name,
                        ss.artist_location      AS location,
                        ss.artist_latitude      AS latitude,
                        ss.artist_longitude     AS longitude
                    FROM staging_songs_table ss
                    """


time_table_insert = """INSERT INTO time       
                    SELECT DISTINCT
                        t.time                        AS start_time,
                        EXTRACT(hour from t.time)     AS hour,
                        EXTRACT(day from t.time)      AS day,
                        EXTRACT(week from t.time)     AS week,
                        EXTRACT(month from t.time)    AS month,
                        EXTRACT(year from t.time)     AS year,
                        EXTRACT(dow from t.time)  AS weekday
                    FROM
                    -- sub query that convert milliseconds to timestamp
                    (SELECT 
                        TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second' AS time
                    FROM staging_events_table
                    ) AS t
                    """

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, 
                        user_table_create, song_table_create, artist_table_create,
                        time_table_create, songplay_table_create]

drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, 
                    songplay_table_drop, user_table_drop, song_table_drop, 
                    artist_table_drop, time_table_drop]

copy_table_queries = [staging_events_copy, staging_songs_copy]

insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert,
                         artist_table_insert, time_table_insert]
