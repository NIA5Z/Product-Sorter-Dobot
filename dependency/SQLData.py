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

def insert(pcode, pbrand, pname, ptype, pup, pbp, pqty):

   if Init == 0:
     print("Library haven't been initialized yet.")
     return
   
   sql_query = """
   INSERT INTO Product (PCODE, PBRAND, PNAME, PTYPE, PUP, PBP, PQTY)
   VALUES (?, ?, ?, ?, ?, ?, ?);
   """
   try:
      cursor.execute(sql_query, (pcode, pbrand, pname, ptype, pup, pbp, pqty))
      connection.commit()
      print("Product inserted successfully.")
   except sql.Error as e:
      print(f"An error occurred: {e}")

def remove(pcode):
    if Init == 0:
        print("Library hasn't been initialized yet.")
        return

    sql_query = "DELETE FROM Product WHERE PCODE = ?;"
    try:
        cursor.execute(sql_query, (pcode,))
        connection.commit()
        print("Product removed successfully.")
    except sql.Error as e:
        print(f"An error occurred: {e}")

def fetch(target):
   if Init == 0:
     print("Library haven't been initialized yet.")
     return
   
   sql_query = f"SELECT {target} FROM Product;"
   try:
      cursor.execute(sql_query)
      results = cursor.fetchall()
      return results
   except sql.Error as e:
      print(f"An error occurred: {e}")
      return None
    
def search(target, value):
    if Init == 0:
     print("Library haven't been initialized yet.")
     return
    
    sql_query = f"SELECT {target} FROM Product WHERE {target} = ?;"
    try:
        cursor.execute(sql_query, (value,))  
        results = cursor.fetchall()
        return results
    except sql.Error as e:
        print(f"An error occurred: {e}")
        return None

def fetchall():
   data = []
   cursor.execute("SELECT * FROM Product;")
   products = cursor.fetchall()
   for product in products:
      data.append(product)
   return data

# Example usage:
#create_table()  # Ensure you have called this to initialize your database
#insert('001', 'BrandX', 'ProductA', 'Type1', 10.0, 15.0, 100)
#remove('001')  # Call this to remove the product with PCODE '001'