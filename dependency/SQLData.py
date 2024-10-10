import sqlite3 as sql
import os

Init = 0

if os.path.exists('./dependency/SQL_Database/database.db') == True:
 print("Existing Database Armed.")
 Init=1

connection = sql.connect('./dependency/SQL_Database/database.db')
cursor = connection.cursor()

def create_table(loc="./dependency/SQL_Database/Setup.sql",overwrite=False): 
 global Init

 if Init == 1 and not overwrite:
  print("Database.db already exists! Are you sure you want to overwrite the current db? If so, use overwrite=True.")
  return

 with open(loc, 'r') as file:
    sql_script = file.read()

 try:
    cursor.executescript(sql_script)
    print("Tables created successfully.")
    Init = 1
    connection.commit()
    return
 except sql.Error as e:
    print(f"An error occurred: {e}")
    return

