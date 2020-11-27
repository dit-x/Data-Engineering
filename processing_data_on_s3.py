#%%

import os
import glob
import boto3, s3fs
from io import StringIO
import pandas as pd
from datetime import datetime 

s3 = boto3.client('s3')


def save_to_s3(bucket, df, name):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, name  + '.csv').put(Body=csv_buffer.getvalue())



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


def process_log_file(input_path):
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
    # df = process_multiple_file(input_path + '/log_data')
    path = input_path + '/2018-11-02-events.json'
    df = pd.read_json(path, lines=True)

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
    save_to_s3('dit-store-s3', time_df, 'time_table')

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]
    save_to_s3('dit-store-s3', user_df, 'users_table')
     

def main():
    input_path = 's3://dit-store-s3'
    process_log_file(input_path)

if __name__ == "__main__":
    main()
# %%
