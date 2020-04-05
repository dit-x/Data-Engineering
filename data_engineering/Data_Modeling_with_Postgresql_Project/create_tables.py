import psycopg2
from sql_queries import create_table_queries, drop_table_queries
import pandas as pd

df = pd.read_csv('detail.csv')

# getting login details
user = df["user"].iloc[0]
password = df["password"].iloc[0]


def create_database():
    """
    - Creates and connects to the sparkifydb
    - Returns the connection and cursor to sparkifydb
    """
    
    
    # connect to sparkify database
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=postgres", password=password)
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    return cur, conn


def drop_tables(cur, conn):
    try:
            
        """
        Drops each table using the queries in `drop_table_queries` list.
        """
        for query in drop_table_queries:
            cur.execute(query)
            conn.commit()
            
        print("All table dropped succefully")

    except Exception as e:
        print(e)


def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list. 
    """
    try:

        for query in create_table_queries:
            cur.execute(query)
            conn.commit()

        print("Table(s) created succussfully")
    except Exception as e:
        print(e)


def main():
    """
    - Drops (if exists) and Creates the sparkify database. 
    
    - Establishes connection with the sparkify database and gets
    cursor to it.  
    
    - Drops all the tables.  
    
    - Creates all tables needed. 
    
    - Finally, closes the connection. 
    """
    cur, conn = create_database()
    
    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()


