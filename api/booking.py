from flask import *
from flask import jsonify

booking = Blueprint("booking", __name__)

# ====== jwt
from model import jwt_decode

# ====== booking_data
from model import booking_data_is_empty
from model import booking_people_exist
from model import update_booking_data
from model import get_data_for_booking_page
from model import delete_data_for_bookin_page

@booking.route("/booking", methods=["POST", "GET", "DELETE"])
def api_booking():

    auth_header = request.headers.get('Authorization')
    token = auth_header.split(' ')[1]
    payload = jwt_decode(token)
    print(payload)
    person_id = payload["data"]["id"]
    username = payload["data"]["name"]
    print(person_id)
    print(username)

    if request.method == "POST":
        try:
            
            # check booking process
            booking_information = request.get_json()
            booking_attraction_id = booking_information["attractionId"]
            booking_date = booking_information["date"]
            booking_price = booking_information["price"]
            booking_time = booking_information["time"]
            if booking_data_is_empty(booking_attraction_id, booking_date, booking_price, booking_time):
                return jsonify({"error": True, "message": "booking資料不得有空白"})
            if booking_people_exist(person_id):
                update_booking_data(booking_attraction_id, booking_date, booking_price, booking_time, person_id)
                return jsonify({"ok": True})
        except:
            return jsonify({"error": True, "message": "booking伺服器內部錯誤"})
        
    if request.method == "GET":
        try:
            response = get_data_for_booking_page(username, person_id)
            print(response)
            return jsonify(response)
        except:
            return jsonify({"error": True, "message": "booking伺服器內部錯誤"})
        
    if request.method == "DELETE":
        try:
            attraction_id = request.get_json()["attractionId"]
            delete_data_for_bookin_page(attraction_id, person_id)
            return jsonify({"ok": True})
        except:
            return jsonify({"error": True, "message": "booking伺服器內部錯誤"})
