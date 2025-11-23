"""
GDP Data ETL Pipeline
====================
This script extracts GDP data from Wikipedia, transforms it, and loads it into CSV and SQLite database.

Author: Your Name
Date: 2025
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import numpy as np
from datetime import datetime
import os
from config import URL, TABLE_ATTRIBS, DB_NAME, TABLE_NAME, CSV_PATH, LOG_FILE


def extract(url, table_attribs):
    """
    Extract GDP data from Wikipedia page.
    
    Args:
        url (str): URL of the Wikipedia page
        table_attribs (list): Column names for the DataFrame
        
    Returns:
        pd.DataFrame: Extracted data
    """
    try:
        page = requests.get(url).text
        data = BeautifulSoup(page, 'html.parser')
        df = pd.DataFrame(columns=table_attribs)
        tables = data.find_all('tbody')
        rows = tables[2].find_all('tr')
        
        for row in rows:
            col = row.find_all('td')
            if len(col) != 0:
                if col[0].find('a') is not None and '—' not in col[2]:
                    data_dict = {
                        "Country": col[0].a.contents[0],
                        "GDP_USD_millions": col[2].contents[0]
                    }
                    df1 = pd.DataFrame(data_dict, index=[0])
                    df = pd.concat([df, df1], ignore_index=True)
        
        log_progress(f'Successfully extracted {len(df)} records')
        return df
    
    except Exception as e:
        log_progress(f'Error during extraction: {str(e)}')
        raise


def transform(df):
    """
    Transform GDP data from millions to billions.
    
    Args:
        df (pd.DataFrame): Input DataFrame
        
    Returns:
        pd.DataFrame: Transformed DataFrame
    """
    try:
        GDP_list = df["GDP_USD_millions"].tolist()
        GDP_list = [float("".join(x.split(','))) for x in GDP_list]
        GDP_list = [np.round(x/1000, 2) for x in GDP_list]
        df["GDP_USD_millions"] = GDP_list
        df = df.rename(columns={"GDP_USD_millions": "GDP_USD_billions"})
        
        log_progress(f'Transformed {len(df)} records from millions to billions')
        return df
    
    except Exception as e:
        log_progress(f'Error during transformation: {str(e)}')
        raise


def load_to_csv(df, csv_path):
    """
    Save DataFrame to CSV file.
    
    Args:
        df (pd.DataFrame): DataFrame to save
        csv_path (str): Path to output CSV file
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        df.to_csv(csv_path, index=False)
        log_progress(f'Data saved to CSV: {csv_path}')
    
    except Exception as e:
        log_progress(f'Error saving to CSV: {str(e)}')
        raise


def load_to_db(df, sql_connection, table_name):
    """
    Load DataFrame to SQLite database.
    
    Args:
        df (pd.DataFrame): DataFrame to load
        sql_connection: SQLite connection object
        table_name (str): Name of the table
    """
    try:
        df.to_sql(table_name, sql_connection, if_exists='replace', index=False)
        log_progress(f'Data loaded to database table: {table_name}')
    
    except Exception as e:
        log_progress(f'Error loading to database: {str(e)}')
        raise


def run_query(query_statement, sql_connection):
    """
    Execute SQL query and display results.
    
    Args:
        query_statement (str): SQL query to execute
        sql_connection: SQLite connection object
    """
    try:
        print(f"\n{'='*60}")
        print(f"Executing Query: {query_statement}")
        print(f"{'='*60}")
        query_output = pd.read_sql(query_statement, sql_connection)
        print(query_output)
        print(f"{'='*60}\n")
        log_progress(f'Query executed successfully: {query_statement}')
    
    except Exception as e:
        log_progress(f'Error executing query: {str(e)}')
        raise


def log_progress(message):
    """
    Log progress messages with timestamp.
    
    Args:
        message (str): Message to log
    """
    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    with open(LOG_FILE, "a") as f:
        f.write(timestamp + ' : ' + message + '\n')
    
    # Also print to console
    print(f"[{timestamp}] {message}")


def main():
    """
    Main function to run the ETL pipeline.
    """
    print("\n" + "="*60)
    print("GDP DATA ETL PIPELINE")
    print("="*60 + "\n")
    
    # Step 1: Extract
    log_progress('Preliminaries complete. Initiating ETL process')
    df = extract(URL, TABLE_ATTRIBS)
    log_progress('Data extraction complete. Initiating Transformation process')
    
    # Step 2: Transform
    df = transform(df)
    log_progress('Data transformation complete. Initiating loading process')
    
    # Step 3: Load to CSV
    load_to_csv(df, CSV_PATH)
    log_progress('Data saved to CSV file')
    
    # Step 4: Load to Database
    sql_connection = sqlite3.connect(DB_NAME)
    log_progress('SQL Connection initiated.')
    load_to_db(df, sql_connection, TABLE_NAME)
    log_progress('Data loaded to Database as table. Running the query')
    
    # Step 5: Run sample queries
    query_statement = f"SELECT * FROM {TABLE_NAME} WHERE GDP_USD_billions >= 100"
    run_query(query_statement, sql_connection)
    
    # Additional query examples
    query_statement = f"SELECT COUNT(*) as total_countries FROM {TABLE_NAME}"
    run_query(query_statement, sql_connection)
    
    query_statement = f"SELECT * FROM {TABLE_NAME} ORDER BY GDP_USD_billions DESC LIMIT 10"
    run_query(query_statement, sql_connection)
    
    # Close connection
    log_progress('Process Complete.')
    sql_connection.close()
    
    print("\n" + "="*60)
    print("ETL PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"CSV Output: {CSV_PATH}")
    print(f"Database: {DB_NAME}")
    print(f"Log File: {LOG_FILE}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()