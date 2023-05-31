import csv
import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Read the CSV file and insert data into the table
with open('Communes.csv', 'r') as file:
    csv_reader = csv.reader(file, delimiter=',')
    next(csv_reader)  # Skip the header row if present
     
    for row in csv_reader:
        row = [cell if cell != '' else None for cell in row]
        # Determine the number of columns in the row
        num_columns = len(row)

        # Create the placeholders for the SQL query
        placeholders = ','.join(['?'] * num_columns)

        cursor.execute('INSERT INTO api_evotech_commune VALUES (?, ?, ?)', row)

# Commit the changes and close the connection
conn.commit()
conn.close()
