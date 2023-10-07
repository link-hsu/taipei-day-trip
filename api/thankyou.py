# from flask import *
# from flask import jsonify

# from model import jwt_decode
# from model import get_transaction_record_by_transaction_number

# thankyou = Blueprint("thankyou", __name__)

# @thankyou.route("/thankyou", methods=["GET"])
# def api_thankyou():
#     auth_header = request.headers.get('Authorization')
#     token = auth_header.split(' ')[1]
#     payload = jwt_decode(token)
#     person_id = payload["data"]["id"]
#     transaction_number = int(request.args.get("number", ""))
#     print(transaction_number)
#     if not get_transaction_record_by_transaction_number(transaction_number, person_id):
#         print("無此訂單編號權限")
#         return ({"error": True, "message": "無此訂單觀看權限"})
#     return render_template("thankyou.html")
    