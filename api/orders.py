from flask import *
from flask import jsonify

orders = Blueprint("orders", __name__)
order_num = Blueprint("order_num", __name__)

# ====== jwt
from model import jwt_decode

# ====== handle orders 
from model import order_data_is_empty
from model import check_email_format
from model import order_reservation_exist
from model import write_historical_order
from model import pay_by_prime_API
from model import write_transaction_record_in_historical_order
from model import get_transaction_record_in_historical_order
from model import delete_reservation_flash_by_person_id


# ====== handle order/<ordernumber>
from model import get_transaction_record_by_transaction_number

@orders.route("/orders", methods=["POST"])
def api_orders():
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1]
        payload = jwt_decode(token)
        person_id = payload["data"]["id"]
        order_data_from_frontEnd = request.get_json()
        if order_data_is_empty(order_data_from_frontEnd):
            return jsonify({"error": True, "message": "有order資料未填寫"})
        contact_email = order_data_from_frontEnd["order"]["contact"]["email"]
        if not check_email_format(contact_email):
            return jsonify({"error": True, "message": "信箱格式有誤"})
        if not order_reservation_exist(person_id, order_data_from_frontEnd):
            return jsonify({"error": True, "message": "此訂單不在您的預訂清單中"})
        the_last_order_number = write_historical_order(person_id, order_data_from_frontEnd)
        tappay_api_response = pay_by_prime_API(order_data_from_frontEnd)
        write_transaction_record_in_historical_order(the_last_order_number, tappay_api_response)
        delete_reservation_flash_by_person_id(person_id)
        transaction_record = get_transaction_record_in_historical_order(the_last_order_number)
        return jsonify(transaction_record)
    except Exception as e:
        print("orders伺服器內部錯誤: ", e)
        return jsonify({"error": True, "message": "orders伺服器內部錯誤"})

        
@order_num.route("/order/<orderNumber>", methods=["GET"])
def api_order_num(orderNumber):
    print(orderNumber)
    try:
        print(orderNumber)
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1]
        payload = jwt_decode(token)
        person_id = payload["data"]["id"]
        transaction_number = orderNumber
        transaction_record = get_transaction_record_by_transaction_number(transaction_number, person_id)
        print(transaction_record)
        if transaction_record:
            return jsonify(transaction_record)
        return jsonify({"error": True, "message": "此訂單不在您預訂清單中"})
    except Exception as e:
        print("order/<orderNumber>伺服器內部錯誤: ", e)
        return jsonify({"error": True, "message": "order/<orderNumber>伺服器內部錯誤"})

