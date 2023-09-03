import mysql.connector
import json
from flask import jsonify

def filter_imagelink(file):    
    def is_imagelink(link):
        return link.lower().endswith((".png", ".jpg"))
    images = file.split("https://")
    images = ["https://" + image for image in images if is_imagelink(image)]    
    return images

def data_for_page(name_data, data_per_page):
    page_results = []
    for i in range(0, len(name_data), data_per_page):
        grouping = name_data[i:i + data_per_page]
        page_result = {"nextPage": (i // data_per_page) + 1, "data": grouping}
        page_results.append(page_result)
    return page_results




# data for routing api/attractions?page=c

def get_attraction_page(page):
    con = mysql.connector.connect(
        user="root",
        password="123456789",
        host="localhost",
        database="attraction",
        auth_plugin="mysql_native_password"
        )
    
    cursor = con.cursor()        
    query = """
        SELECT nextPage, id, name, category, description, address, transport, mrt, lat, longitude, images
        FROM attraction_name
        WHERE nextPage = %s      
    """ 
    nextPage = int(page) + 1
    cursor.execute(query, (int(nextPage),))
    results = cursor.fetchall()
    result = {"data": []}
    for item in results:
        if int(page) + 1 == item[0]:
            result["nextPage"] = item[0]
            data_item = {
                "id": item[1],
                "name": item[2],
                "category": item[3],
                "description": item[4],
                "address": item[5],
                "transport": item[6],
                "mrt": item[7],
                "lat": float(item[8]),
                "longitude": float(item[9]),
                "images": filter_imagelink(item[10]) }
            result["data"].append(data_item)
    if not result["data"]:
            return jsonify({"error": True, "message": "no more attractions"}), 500
    return jsonify(result)




# data for routing api/attractions?page=c&keyword=c
# data for routing api/attractions?keyword=c
def get_attration_page_keyword(page, keyword):
    con = mysql.connector.connect(
        user="root",
        password="123456789",
        host="localhost",
        database="attraction",
        auth_plugin="mysql_native_password"
        )
    
    cursor = con.cursor()
    query = """
        SELECT id, name, category, description, address, transport, mrt, lat, longitude, images
        FROM attraction_name
        WHERE mrt = %s OR name LIKE %s
    """   
    cursor.execute(query, (keyword, f'%{keyword}%'))
    results = cursor.fetchall()
    
    output_total = []
    for i in range(0, len(results), 12):
        grouping = results[i:i + 12]
        output = {
            "nextPage": (i  // 12) + 1, "data":grouping}
        output_total.append(output)
    cursor.close()
    con.close()
    if not page:
        return output_total
    elif int(page) > len(output_total) - 1:
        return jsonify({"error": True, "message": "no more page"}), 500
    for item in output_total:
        if item["nextPage"] == int(page) + 1:
            return item
    return jsonify({"error": True, "message": "Searching page doesn't exist"}), 500

def get_attraction_search_id(id):
    con = mysql.connector.connect(
        user="root",
        password="123456789",
        host="localhost",
        database="attraction",
        auth_plugin="mysql_native_password"
        )
    
    cursor = con.cursor()
    query = """
    SELECT id, name, category, description, address, transport, mrt, lat, longitude, images
    FROM attraction_name
    WHERE id = %s
    """ 

    cursor.execute(query, (int(id),))    
    results = cursor.fetchall()
    print(results)
    if not results:
        return jsonify({"error": True, "message": "attraction doesn't exist"}), 500
    result = {
            "id": results[0][0],
            "name": results[0][1],
            "category": results[0][2],
            "description": results[0][3],
            "address": results[0][4],
            "transport": results[0][5],
            "mrt": results[0][6],
            "lat": float(results[0][7]),
            "longitude": float(results[0][8]),
            "images": filter_imagelink(results[0][9]) }
    return json.dumps(result)

def get_attraction_mrts_descending():
    """api for api/mrts"""
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

