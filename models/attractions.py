import mysql.connector
import json

def get_attraction_table(table_name):
    """table_name = name | image | mrt"""
    con = mysql.connector.connect(
        user="root",
        password="123456789",
        host="localhost",
        database="attraction",
        auth_plugin="mysql_native_password")
    
    cursor = con.cursor()
    query = f"SELECT * FROM attraction_{table_name}"
    cursor.execute(query)    
    data = cursor.fetchall()
    cursor.close()
    con.close()
    data_table_name = [{"id": item[0], "name": item[1], "category": item[2], "description": item[3], "address": item[4], "transport": item[5], "mrt": item[6], "lat": float(item[7]), "lng": float(item[8]), "images": item[9]} for item in data]
    data_table_image = [{"id": item[0], "name": item[1], "image": item[2]} for item in data]
    data_table_mrt = [{"id": item[0], "mrt": item[1], "count": item[2]} for item in data]
    if table_name == "name":
        return json.dumps(data_table_name)
    elif table_name == "image":
        return json.dumps(data_table_image)
    elif table_name == "mrt":
        return json.dumps(data_table_mrt)
    else:
        raise ValueError(f"Invalid table name: {table_name}")
    

def get_attraction_name_join_image():
    con = mysql.connector.connect(
    user = "root",
    password = "123456789",
    host = "localhost",
    database = "attraction",
    auth_plugin="mysql_native_password")

    cursor = con.cursor()
    cursor.execute("SELECT * FROM attraction_name n INNER JOIN attraction_image i ON n.name = i.name")
    data = cursor.fetchall()
    cursor.close()
    con.close()
    data = [{"id": item[0], "name": item[1], "category": item[2], "description": item[3], "address": item[4], "transport": item[5], "mrt": item[6], "lat": float(item[7]), "lng": float(item[8]), "images": item[12]} for item in data]
    return json.dumps(data)

def get_attraction_mrts_descending():
    con = mysql.connector.connect(
    user = "root",
    password = "123456789",
    host = "localhost",
    database = "attraction",
    auth_plugin="mysql_native_password")

    cursor = con.cursor()
    cursor.execute("SELECT mrt, count FROM attraction_mrt ORDER BY count DESC")
    data = cursor.fetchall()
    cursor.close()
    con.close()
    data = [{"mrt": item[0], "count": item[1]} for item in data]
    return json.dumps(data)
