import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your actual DB username
        password="yourpassword",  # Replace with your actual password
        database="ALX_prodev"
    )

def stream_users_in_batches(batch_size):
    """
    Generator that yields users in batches from the user_data table.
    """
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        yield rows  # Yield the entire batch
    cursor.close()
    conn.close()

def batch_processing(batch_size):
    """
    Process and filter users over age 25 from batches.
    """
    for batch in stream_users_in_batches(batch_size):  # Loop 1
        for user in batch:  # Loop 2
            if user["age"] > 25:
                yield user  # Generator filter
