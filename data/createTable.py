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



# # Table accounts
# sql = """CREATE TABLE IF NOT EXISTS
#         accounts(id_people INT PRIMARY KEY AUTO_INCREMENT,
#         name VARCHAR(255), email VARCHAR(255), password VARCHAR(255))"""
# con = get_con()
# cursor = con.cursor()
# cursor.execute(sql)
# cursor.close()
# con.close()


# Table reservationflash
sql = """CREATE TABLE IF NOT EXISTS
        reservationflash(
        id INT PRIMARY KEY AUTO_INCREMENT,
        attractionId INT,
        date VARCHAR(20),
        time VARCHAR(20),
        price INT,
        personId INT)"""
con = get_con()
cursor = con.cursor()
cursor.execute(sql)
cursor.close()
con.close()

# Table historical_order
sql = """CREATE TABLE IF NOT EXISTS
        historical_order(
        order_number INT PRIMARY KEY AUTO_INCREMENT,
        order_account_id INT,
        order_contact_name VARCHAR(200),
        order_contact_email VARCHAR(200),
        order_contact_phone VARCHAR(200),
        order_date VARCHAR(200),
        order_time VARCHAR(200),
        order_attraction_id INT,
        order_price INT,
        transaction_time VARCHAR(20),
        order_status INT NOT NULL DEFAULT 1)"""
con = get_con()
cursor = con.cursor()
cursor.execute(sql)
cursor.close()
con.close()