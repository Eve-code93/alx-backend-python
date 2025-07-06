import csv
import mysql.connector
import uuid

def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",       # use your mysql username
            password="yourpassword"  # replace with your MySQL password
        )
    except mysql.connector.Error as err:
        print(f"Connection error: {err}")
        return None

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

def connect_to_prodev():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="yourpassword",  # replace with your MySQL password
            database="ALX_prodev"
        )
    except mysql.connector.Error as err:
        print(f"Connection error: {err}")
        return None

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3) NOT NULL,
            INDEX(user_id)
        )
    """)
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")

def insert_data(connection, filename):
    cursor = connection.cursor()
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute("""
                INSERT IGNORE INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (row['user_id'], row['name'], row['email'], row['age']))
    connection.commit()
    cursor.close()

def stream_user_data(connection):
    """
    Generator that streams rows one at a time from the user_data table.
    """
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data;")
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row
    cursor.close()
