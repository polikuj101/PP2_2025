import psycopg2
import csv

# Connect to your postgres DB
conn = psycopg2.connect(
    host="localhost",
    database="my_phonebook",
    user="postgres",
    password="Sherlok123"
)
cur = conn.cursor()

def create_table():
    cur.execute('''
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            phone_number VARCHAR(15) NOT NULL
        );
    ''')
    conn.commit()

# 1. Insert via console
def insert_from_console():
    first_name = input("Enter first name: ")
    phone_number = input("Enter phone number: ")
    cur.execute("INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s)", (first_name, phone_number))
    conn.commit()
    print("Inserted successfully.")

# 2. Insert from CSV
def insert_from_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip header
        for row in reader:
            cur.execute("INSERT INTO phonebook (first_name, phone_number) VALUES (%s, %s)", (row[0], row[1]))
    conn.commit()
    print("CSV data inserted.")

# Update data
def update_user(old_name=None, new_name=None, new_phone=None):
    if new_name:
        cur.execute("UPDATE phonebook SET first_name = %s WHERE first_name = %s", (new_name, old_name))
    if new_phone:
        cur.execute("UPDATE phonebook SET phone_number = %s WHERE first_name = %s", (new_phone, old_name))
    conn.commit()
    print("User updated.")

# Query with filters
def query_users(filter_field=None, value=None):
    if filter_field and value:
        cur.execute(f"SELECT * FROM phonebook WHERE {filter_field} = %s", (value,))
    else:
        cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()
    for row in rows:
        print(row)

# Delete by username or phone
def delete_user(value):
    cur.execute("DELETE FROM phonebook WHERE first_name = %s OR phone_number = %s", (value, value))
    conn.commit()
    print("User deleted.")

# Usage example
if __name__ == '__main__':
    create_table()
    
    insert_from_console()
    insert_from_csv("phonebook_data.csv")
    update_user(old_name="Alice", new_phone="1234567890")
    query_users()
    delete_user("Alice")
    
    cur.close()
    conn.close()
