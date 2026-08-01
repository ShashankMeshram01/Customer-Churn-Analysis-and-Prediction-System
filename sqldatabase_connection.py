# db_connect.py — MySQL connection and data loader
import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

def get_connection():
    conn = mysql.connector.connect(
        host= os.environ.get("DB_HOST"),
        user= os.environ.get("DB.USER"),          
        password= os.environ.get("DB_PASSWORD"),  
        database= os.environ.get("DB_NAME")       
    )
    return conn

def load_data():
    conn = get_connection()
    query = "SELECT * FROM Customers"   
    df = pd.read_sql(query, conn)
    conn.close()
    print(f"✅ Data loaded: {df.shape[0]} rows × {df.shape[1]} columns")
    return df
          