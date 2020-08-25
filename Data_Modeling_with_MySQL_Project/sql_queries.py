

# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = """CREATE TABLE IF NOT EXISTS songplays(
                        songplay_id SERIAL PRIMARY KEY,
                        start_time BIGINT NOT NULL, 
                        user_id INT NOT NULL, 
                        level VARCHAR(15), 
                        song_id CHAR(18), 
                        artist_id CHAR(19), 
                        session_id int, 
                        location VARCHAR(100), 
                        user_agent VARCHAR(255),
                        FOREIGN KEY (song_id) REFERENCES songs(song_id),
                        FOREIGN KEY (user_id) REFERENCES users(user_id),
                        FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
                        FOREIGN KEY (start_time) REFERENCES time(start_time)
                    );"""

user_table_create = """CREATE TABLE IF NOT EXISTS users(
                        User_id INT NOT NULL PRIMARY KEY,
                        first_name VARCHAR(25),
                        last_name VARCHAR(25),
                        gender CHAR(1) NOT NULL,
                        level VARCHAR(15)
                        );"""

song_table_create = """CREATE TABLE IF NOT EXISTS songs(
                        song_id CHAR(18) NOT NULL PRIMARY KEY,
                        title VARCHAR(100),
                        artist_id CHAR(19) NOT NULL,
                        year INT NOT NULL,
                        duration FLOAT NOT NULL
                        );"""


artist_table_create = """CREATE TABLE IF NOT EXISTS artists(
                        artist_id CHAR(19) NOT NULL PRIMARY KEY,
                        artist_name VARCHAR(100) NOT NULL,
                        location VARCHAR(100),
                        latitude VARCHAR(50),
                        longitude VARCHAR(50)
                        );"""

time_table_create = """CREATE TABLE IF NOT EXISTS time(
                        start_time BIGINT NOT NULL PRIMARY KEY,
                        hour INT,
                        day INT,
                        week_of_year INT,
                        month INT,
                        year INT,
                        weekday INT
                        );"""

# INSERT RECORDS

songplay_table_insert = """INSERT INTO songplays(start_time, user_id, level, 
                            song_id, artist_id, session_id, 
                            location, user_agent)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """

user_table_insert = """INSERT INTO users
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (user_id) DO UPDATE SET level=EXCLUDED.level;
                    """

song_table_insert = """INSERT INTO songs
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT
                    DO NOTHING;
                    """

artist_table_insert =  """INSERT INTO artists
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT
                    DO NOTHING;
                    """


time_table_insert = """INSERT INTO time
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING
                    """

# FIND SONGS

song_select = ("""
                SELECT 
                    s.song_id, 
                    a.artist_id 
                FROM 
                    songs s
                INNER JOIN 
                    artists a ON a.artist_id = s.artist_id
                WHERE s.title = (%s) AND a.artist_name = (%s) AND s.duration = (%s)
""")

# QUERY LISTS

create_table_queries = [user_table_create,
                         song_table_create, artist_table_create, 
                         time_table_create, songplay_table_create]

drop_table_queries = [songplay_table_drop, user_table_drop, 
                        song_table_drop, artist_table_drop, 
                        time_table_drop]
