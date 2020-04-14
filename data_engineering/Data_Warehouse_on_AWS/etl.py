import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Parameters:
        cur: This holds the data retrieved from database

        conn: This holds the connection made to the database

    Function:
        To copy files in the AWS S3 bucket and load it in staging tables
    """
    try:
        i = 0
        for query in copy_table_queries:
            cur.execute(query)
            conn.commit()
            i += 1
            print(f"{i}. Table Loaded")   
    except Exception as e:
        print(e)


def insert_tables(cur, conn):
    """
    Parameters:
        cur: This holds the data retrieved from database

        conn: This holds the connection made to the database

    Function:
        To extract info from the staging table, transform and load it in the
        dimensions and fact table that makes up the DWH
    """
    try:
        i = 0
        for query in insert_table_queries:
            print(f"\nStarting insert {i+1}")
            cur.execute(query)
            conn.commit()
            i += 1
            print(f"\tinsert {i} done! ")

    except Exception as e:
        print(e)

def main():
    """
        This makes connection to redshift cluster using already defined parameters,
        - calls the function to load data from AWS S3 bucket into the staging table and
        - calls the function that extract data from staging table and load it into Fact
          and dimensions table 
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}"
                .format(*config['CLUSTER'].values()))
    print('CONNECTED!')

    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()