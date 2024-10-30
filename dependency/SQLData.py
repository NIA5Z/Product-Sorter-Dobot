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
  print("Database.db exist, however if you want to overwrite it then create_table(overwrite=True)")
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

def insert(data):

   if Init == 0:
     print("Library haven't been initialized yet.")
     return
   
   sql_query = """
   INSERT INTO Product (PCODE, PBRAND, PNAME, PTYPE, PUP, PBP, PQTY)
   VALUES (?, ?, ?, ?, ?, ?, ?);
   """
   try:
      cursor.execute(sql_query, (data.CODE,data.BRAND, data.NAME, data.TYPE, data.PUnit, data.PBase, data.QTY))
      connection.commit()
      print("Product inserted successfully.")
   except sql.Error as e:
      print(f"An error occurred: {e}")

def remove(target,pcode):
    if Init == 0:
        print("Library hasn't been initialized yet.")
        return

    sql_query = f"DELETE FROM Product WHERE {target} = ?;"
    try:
        cursor.execute(sql_query, (pcode,))
        connection.commit()
        print("Product removed successfully.")
    except sql.Error as e:
        print(f"An error occurred: {e}")

def fetch(data):
   if Init == 0:
     print("Library haven't been initialized yet.")
     return
   
   sql_query = """SELECT * FROM Product WHERE PCODE = ? ;"""
   try:
      cursor.execute(sql_query, (data,))  
      products = cursor.fetchall()
      return products
   except sql.Error as e:
      print(f"An error occurred: {e}")
      return None
    
def update(data):
   if Init == 0:
     print("Library haven't been initialized yet.")
     return
   
   sql_query = """
        UPDATE Product
        SET PBRAND = ?, PNAME = ?, PTYPE = ?, PUP = ?, PBP = ?, PQTY = ?
        WHERE PCODE = ?;
   """
   try:
      cursor.execute(sql_query, (data.BRAND, data.NAME, data.TYPE, data.PUnit, data.PBase, data.QTY, data.CODE))
      connection.commit()
      print("Product updated successfully.")
   except sql.Error as e:
      print(f"An error occurred: {e}")

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