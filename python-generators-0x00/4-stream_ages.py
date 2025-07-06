import mysql.connector
from seed import connect_to_prodev

def stream_user_ages():
    """
    Generator that yields user ages one by one from the user_data table.
    """
    connection = connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:
        yield age

    cursor.close()
    connection.close()


def calculate_average_age():
    """
    Uses the stream_user_ages generator to calculate and print the average age.
    """
    total = 0
    count = 0

    for age in stream_user_ages():  # ✅ First and only loop
        total += age
        count += 1

    if count > 0:
        average = total / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users found.")

# Optional: Run when this file is executed directly
if __name__ == "__main__":
    calculate_average_age()
