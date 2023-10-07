import mysql.connector


def get_con():
    con = mysql.connector.connect(
        user="root",
        password="123456789",
        host="localhost",
        database="attraction",
        auth_plugin="mysql_native_password"
        )
    print("connnect to mysql successfully")
    return con



# # Table reservationflash
# sql = """CREATE TABLE IF NOT EXISTS
#         reservationflash(
#         id INT PRIMARY KEY AUTO_INCREMENT,
#         attractionId INT,
#         date VARCHAR(20),
#         time VARCHAR(20),
#         price INT,
#         personId INT)"""
# con = get_con()
# cursor = con.cursor()
# cursor.execute(sql)
# cursor.close()
# con.close()

# # Table historical_order
# sql = """CREATE TABLE IF NOT EXISTS
#         historical_order(
#         order_number INT PRIMARY KEY AUTO_INCREMENT,
#         order_account_id INT,
#         order_contact_name VARCHAR(200),
#         order_contact_email VARCHAR(200),
#         order_contact_phone VARCHAR(200),
#         order_date VARCHAR(200),
#         order_time VARCHAR(200),
#         order_attraction_id INT,
#         order_price INT,
#         transaction_time VARCHAR(20),
#         order_status INT NOT NULL DEFAULT 1)"""

person_id = 3
attraction_id = '14'
sql = "SELECT * FROM reservationflash WHERE personId = %s AND attractionId = %s ORDER BY id DESC LIMIT 1"

con = get_con()
cursor = con.cursor(dictionary=True)
cursor.execute(sql)
myresult = cursor.fetchone()
if myresult is None:
    print("No data")
else:
    print(myresult)
cursor.close()
con.close()