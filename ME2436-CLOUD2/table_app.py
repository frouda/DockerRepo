import mysql.connector
from mysql.connector import Error
import time

def connect_and_query():
    connection = None 

    for attempt in range(5): 
        try:
            print(f"Attempt {attempt + 1}: Connecting to MySQL...")
            connection = mysql.connector.connect(
                host='ready_app',  
                port=3306,
                user='example_user',
                password='example_password',
                database='example_database'
            )
            if connection.is_connected():
                print("Connected to MySQL database!")
                break  
        except Error as e:
            print(f"Connection failed: {e}")
            print("Retrying in 3 seconds...")
            time.sleep(3)  

    if connection and connection.is_connected():
        cursor = connection.cursor()

        #Δημιουργία πίνακα
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            age INT NOT NULL
        )
        """)

        # **Ελέγχουμε αν υπάρχουν ήδη δεδομένα**
        cursor.execute("SELECT COUNT(*) FROM students")
        result = cursor.fetchone()
        if result[0] == 0:  #Εισαγωγή δεδομένων
            cursor.executemany("INSERT INTO students (name, age) VALUES (%s, %s)", 
                              [("Maria", 25), ("George", 28), ("Nick", 23)])
            connection.commit()
            print(f"✅ 3 rows inserted.")

        #Ανάγνωση δεδομένων
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        print("Data in 'students' table:")
        for row in rows:
            print(row)

        cursor.close()
        connection.close()
        print("MySQL connection is closed.")
    else:
        print("Could not establish connection after multiple attempts.")

if __name__ == "__main__":
    connect_and_query()
