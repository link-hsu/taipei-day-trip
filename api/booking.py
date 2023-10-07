from flask import *
from flask import jsonify

booking = Blueprint("booking", __name__)

# ====== jwt
from model import jwt_decode

# ====== booking_data
from model import booking_data_is_empty
from model import update_booking_data
from model import insert_booking_data
from model import get_data_for_booking_page
from model import delete_data_for_bookin_page
from model import delete_reservation_flash_by_person_id
from model import booking_register_people_exist

@booking.route("/booking", methods=["POST", "GET", "DELETE"])
def api_booking():
    if request.method == "POST":
        try:
            auth_header = request.headers.get('Authorization')
            print("auth_header is: ", auth_header)
            token = auth_header.split(' ')[1]
            payload = jwt_decode(token)
            # print(payload)
            person_id = payload["data"]["id"]
            booking_information = request.get_json()
            booking_attraction_id = int(booking_information["attractionId"])
            booking_date = booking_information["date"]
            booking_price = int(booking_information["price"])
            booking_time = booking_information["time"]
            if booking_data_is_empty(booking_attraction_id, booking_date, booking_price, booking_time):
                return jsonify({"error": True, "message": "booking資料不得有空白"})
            if booking_register_people_exist(person_id):
                insert_booking_data(booking_attraction_id, booking_date, booking_price, booking_time, person_id)
                return jsonify({"ok": True})
        except Exception as e:
            print("line 49 api/booking GET: ", e)
            return jsonify({"error": True, "message": "booking伺服器內部錯誤"})
        
    if request.method == "GET":
        try:
            print("/api/booking start here")
            auth_header = request.headers.get('Authorization')
            token = auth_header.split(' ')[1]
            payload = jwt_decode(token)
            person_id = payload["data"]["id"]
            response = get_data_for_booking_page(person_id)
            print("line 68 response: ", response)
            print("/api/booking response: ", response)
            return jsonify(response)
        except Exception as e:
            print("eeee", e)
            return jsonify({"error": True, "message": "booking伺服器內部錯誤"})
        
    if request.method == "DELETE":
        try:
            auth_header = request.headers.get('Authorization')
            print("auth_header is below")
            print(auth_header )
            token = auth_header.split(' ')[1]
            payload = jwt_decode(token)
            person_id = payload["data"]["id"]
            # attraction_id = int(request.get_json()["attractionId"])
            
            delete_reservation_flash_by_person_id(person_id)
            # delete_data_for_bookin_page(attraction_id, person_id)
            print("delete OK")
            return jsonify({"ok": True})
        except:
            return jsonify({"error": True, "message": "booking伺服器內部錯誤"})
