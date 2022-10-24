import mysql.connector

import database

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="+2d+CVd_&6jJ+@Y",

)


my_cursor = mydb.cursor()

my_cursor.execute("CREATE DATABASE AetherVoid")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)