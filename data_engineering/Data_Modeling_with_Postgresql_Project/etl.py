import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
from datetime import datetime 


def convert_ts(ts):
    """
    Parameter:
            The 'ts' parameter is a millisecond value from the log_data

    Function:
            Convert the timestamp in millisecond to the required format i.e
            hour, day, week of year, month, year and weekday.
    """

    t = datetime.fromtimestamp(ts/1000)
    try:
        hour = t.hour
        day =  t.day
        week_of_year = t.isocalendar()[1]
        month = t.month
        year = t.year
        weekday =  t.weekday()

        data = (ts, hour, day, week_of_year, month, year, weekday)

    except Exception as e:
        print(e)

    return data


def process_song_file(cur, filepath):
    """
    Parameters:
        cur: this is holds the data retrieved from database

        filepath: This holds the directory to the folder to be considered. In this code,
                  it is considered to the mother folder to all song file subfolders

    Function:
        To process all song files in the filepath and extract specific information to 
        song table and artist table
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record

    song_col =  df[[ 'song_id', 'title', 'artist_id', 'year', 'duration']]
    song_col =  song_col.values

    for data in song_col:
        song_data = []
        for value in data:
            song_data.append(value)

    cur.execute(song_table_insert, song_data)
    

    # insert artist record 

    artist_col =  df[[ 'artist_id', 'artist_name', 'artist_location',
                        'artist_latitude', 'artist_longitude']]
    artist_col =  artist_col.values

    for data in artist_col:
        artist_data = []
        for value in data:
            artist_data.append(value)

    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Parameters:
        cur: this is holds the data retrieved from database

        filepath: This holds the directory to the folder to be considered. In this code,
                  it is considered to the mother folder to all log file subfolders

    Function:
        To process all log files in the filepath and extract specific information to 
        time table, user table and songplay table
    """

    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    filt = (df['page'] == "NextSong")
    df = df[filt]

    # convert timestamp column to datetime   
    ts = df['ts'] 
    t_data = []

    for what in ts: 
        # Calling the function to convert the values in ts.
        
        data = convert_ts(what)
        t_data.append(data)

    # insert time data records
    time_data = t_data
    column_labels = ('time_stamp', 'hour', 'day', 'week_of_year', 'month', 'year', 'weekday') 
    time_df =  pd.DataFrame(time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]
     
    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)


    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid,
                         row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Parameters:
        cur: This holds the data retrieved from database

        conn: This holds the connection made to the database

        filepath: This holds the directory to the folder to be considered.

        func: This holdd functions

    Function:
        To process all song files in the filepath and extract specific information
        from all the file involved
    """

    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()