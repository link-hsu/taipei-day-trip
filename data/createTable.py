import mysql.connector

con = mysql.connector.connect(
    user = "root",
    password = "123456789",
    host = "localhost",
    database = "attraction",
    auth_plugin="mysql_native_password")
print("connnect to mysql successfully")
cursor = con.cursor()

sql = """CREATE TABLE IF NOT EXISTS
        accounts(id_people INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255), email VARCHAR(255), password VARCHAR(255))"""
cursor.execute(sql)
cursor.close()
con.close()

