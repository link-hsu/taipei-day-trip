import mysql.connector
from flask import Blueprint, jsonify, request


attractions = Blueprint("attractions", __name__)


def filter_imagelink(file):    
    def is_imagelink(link):
        return link.lower().endswith((".png", ".jpg"))
    images = file.split("https://")
    images = ["https://" + image for image in images if is_imagelink(image)]    
    return images

def get_con():
    con = mysql.connector.connect(
        user="root",
        password="123456789",
        host="localhost",
        database="attraction",
        auth_plugin="mysql_native_password"
        )
    return con


# api: api/attractions?page=c&keyword=c
@attractions.route("/attractions", methods=["GET"])
def search_page_and_keyword():    
    page = int(request.args.get("page", ""))
    keyword = request.args.get("keyword", "")

    try:
        # no keyword search page
        if not keyword:
            query = """
                SELECT id, name, category, description, address, transport, mrt, lat, longitude, images
                FROM attraction_name
                LIMIT 13 OFFSET %s
            """
            con = get_con()
            cursor = con.cursor(dictionary=True) 
            cursor.execute(query, (page * 12,))
            results = cursor.fetchall()
            
            # close connection
            con.close()
            cursor.close()

            # no page data
            if not results:
                result_data = {"error": True, "message": "searching page doesn't exist"}
                return jsonify(result_data), 500

            
        # search keyword and page
        else:
            query = """
                SELECT id, name, category, description, address, transport, mrt, lat, longitude, images
                FROM attraction_name
                WHERE (mrt IS NOT NULL AND mrt = %s) OR (name LIKE CONCAT('%', %s, '%') AND name IS NOT NULL)
                LIMIT 13 OFFSET %s
            """   
            con = get_con()
            cursor = con.cursor(dictionary=True) 
            cursor.execute(query, (keyword, keyword, page * 12))        
            results = cursor.fetchall()

            # close connection
            con.close()
            cursor.close()


        if not results:
            result_data = {"error": True, "message": "doesn't exist attractions within searching field"}
            return jsonify(result_data), 500
        
        result_data = {}
        if len(results) == 13:
            result_data["nextPage"] = page + 1
            results.pop()

        elif len(results) < 13:
            result_data["nextPage"] = None

        for result in results:
            result["images"] = filter_imagelink(result["images"])

        result_data["data"] = results

        return jsonify(result_data), 200
    
    except:
        result_data = {"error": True, "message": "server error"}
        return jsonify(result_data), 500
    

# api: api/attraction/<id>
@attractions.route("/attraction/<attractionID>")
def search_by_id(attractionID):

    try:
        query = """
        SELECT id, name, category, description, address, transport, mrt, lat, longitude, images
        FROM attraction_name
        WHERE id = %s
        """ 
        con = get_con()
        cursor = con.cursor(dictionary=True) 
        cursor.execute(query, (attractionID,))
        results = cursor.fetchone()

        # close connection
        con.close()
        cursor.close()
        print(results)

        if results["id"] == None:
            return jsonify({"error": True, "message": "wrong attraction_id"}), 400
        if not results:
            return jsonify({"error": True, "message": "attraction_id doesn't exist"}), 500

        result_data = {}
        results["images"] = filter_imagelink(results["images"])
        result_data["data"] = results
        return jsonify(result_data), 200
    
    except:
        result_data = {"error": True, "message": "server error"}
        return jsonify(result_data), 500


# api: /api/mrts
@attractions.route("/mrts")
def get_attraction_mrts_descending():
    """api for api/mrts"""
    try:
        con = get_con()
        cursor = con.cursor(dictionary=True)
        cursor.execute("SELECT mrt, count FROM attraction_mrt ORDER BY count DESC")
        results = cursor.fetchall()

        # close connection
        con.close()
        cursor.close()

        mrt_data = [item["mrt"] for item in results if item["mrt"] is not None]
        result_data = {"data": mrt_data}
        return jsonify(result_data), 200
    
    except:
        result_data = {"error": True, "message": "server error"}
        return jsonify(result_data), 500
