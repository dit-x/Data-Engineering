import pandas as pd
import configparser
import os
import findspark
from datetime import datetime 

# Get spark location on PC
SPARK_HOME = os.getenv("SPARK_HOME")
findspark.init(SPARK_HOME)

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format
from pyspark.sql.types import MapType, StructType, StructField , DoubleType, IntegerType ,  StringType, TimestampType



config = configparser.ConfigParser()
config.read(r"C:\DiT\CS\Data Engineer\Module 3 - Data lake\dl.cfg")

os.environ['AWS_ACCESS_KEY_ID']=config['AWS']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS']['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    """Create a apache spark session."""
    spark = SparkSession.builder \
                .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.2") \
                    .appName("Using Spark on S3") \
                .getOrCreate()
    print("SparkSession Created!")
    return spark


@udf(MapType(StringType(), StringType()))
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

    except Exception as e:
        print(e)

    return {"start_time"   : ts, 
                'hour'              : hour, 
                'day'                : day, 
                'week'              : week_of_year, 
                'month'            : month, 
                'year'               : year, 
                'weekday'         : weekday}


def process_song_data(spark, input_data, output_data):
    """
    This helps process the song data into the different dimension table

    Parameters
    ----------
    spark: session
        This is the spark session that has been created
    input_data: path
        This is the path to the song_data s3 bucket.
    output_data: path
        This is the path that holds all saved files
    """

    print("\nRunning process_song_data")
    # making a struct for the columns
    songSchema =  StructType([
                        StructField("artist_id", StringType()),
                        StructField("artist_latitude", DoubleType()),
                        StructField("artist_location", StringType()),
                        StructField("artist_longitude", DoubleType()),
                        StructField("artist_name", StringType()),
                        StructField("duration", DoubleType()),
                        StructField("num_songs", IntegerType()),
                        StructField("song_id", StringType()),
                        StructField("title", StringType()),
                        StructField("year", IntegerType()),
            ])

    # get filepath to song data file
    song_data = input_data + 'song_data/*/*/*/*.json'
    
    # read song data file
    song_df = spark.read.json(song_data, schema=songSchema)

    # extract columns to create songs table
    songs_table = song_df.select(["song_id", "title", "artist_id", "year", "duration"]).dropDuplicates()
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.partitionBy('year', 'artist_id') \
                     .parquet(os.path.join(output_data, 'songs/songs.parquet'), 'overwrite')
    print("songs_table created and save out as parquet")
    
    # extract columns to create artists table
    artists_table = song_df.select(["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]).dropDuplicates()
    
    # write artists table to parquet files
    artists_table.write.parquet(os.path.join(output_data, 'artists/artists.parquet'), 'overwrite')
    print("artists_table created and save out as parquet")

    return song_df, songs_table, artists_table
    
   


def process_log_data(spark, input_data, output_data):
    """
    This helps process the log data into the different dimension table

    Parameters
    ----------
    spark: session
        This is the spark session that has been created
    input_data: path
        This is the path to the log_data s3 bucket.
    output_data: path
        This is the path that holds all saved files
    """

    print("n\Running process_log_data")
    # get filepath to log data file
    log_data = input_data + 'log_data/*.json'

    log_df = spark.read.json(log_data)
    log_df = log_df.filter(log_df.page == "NextSong")
    
    users_table = log_df.select(["userId", "firstName", "lastName", "gender", "level"]).dropDuplicates()
    
    # write users table to parquet files
    users_table.write.parquet(os.path.join(output_data, 'users/users.parquet'), 'overwrite')
    print("users_table created and save out as parquet")

    # create timestamp column from original timestamp column
    ts_col = log_df.select("ts")
    ts_col = ts_col.withColumn("parsed_ts", convert_ts("ts"))

    #  Process the field name
    fields = ['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    exprs = [f"parsed_ts['{field}'] as {field}" for field in fields ]

    # extract columns to create time table
    time_table = ts_col.selectExpr(*exprs).dropDuplicates() 
    
    # write time table to parquet files partitioned by year and month
    time_table.write.partitionBy('year', 'month').parquet(os.path.join(output_data, 'time/time.parquet'), 'overwrite')
    print("time_table created and save out as parquet")

    # create month column from datetime
    get_month = udf(lambda x: datetime.fromtimestamp(x / 1000).month)
    log_df = log_df.withColumn("month", get_month(log_df.ts))
    
    # create year column from datetime
    get_year = udf(lambda x: datetime.fromtimestamp(x / 1000).year)
    log_df = log_df.withColumn("year", get_year(log_df.ts))

    # Load the song data from it location
    song_df = spark.read.json(input_data + 'song_data/*/*/*/*.json')
    
    song_df.createOrReplaceTempView("song_df")
    log_df.createOrReplaceTempView("log_df")

   # extract columns from joined song and log datasets to create songplays table 
    songplays_table = spark.sql("""
                    SELECT DISTINCT 
                                l.ts as start_time, 
                                l.userId as user_id, 
                                l.level, 
                                s.song_id, 
                                s.artist_id, 
                                l.sessionId as session_id,
                                l.location,
                                l.userAgent as user_agent,
                                l.year,
                                l.month                               
                    FROM 
                                log_df l
                    LEFT JOIN
                                song_df s ON l.artist = s.artist_name
                    """)

    songplays_table.write.partitionBy('year', 'month').parquet(os.path.join(output_data, 'songplays/songplays.parquet'), 'overwrite')
    print("songplays_table created and save out as parquet")

    return log_df, users_table, time_table, songplays_table



def main():
    """
    Perform the following roles:
    1.) Get or create a spark session.
    1.) Read the song and log data from s3.
    2.) take the data and transform them to tables
    which will then be written to parquet files.
    3.) Load the parquet files on s3.
    """

    spark = create_spark_session()
    # input_data = r"\data\\"
    input_data = r"s3://udacity-dend/"
    output_data = ""
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()