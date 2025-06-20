import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="+2d+CVd_&6jJ+@Y",
    database="AetherVoid"
)


my_cursor = mydb.cursor()

#my_cursor.execute(''' INSERT INTO v_date (id, year, day, indexDate) VALUES (1,1907,108,0) ''')
my_cursor.execute(''' INSERT INTO AccessCode (id, code) VALUES (1,12345678) ''')
mydb.commit()