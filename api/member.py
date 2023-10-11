from flask import *
from flask import jsonify

member = Blueprint("member",__name__)

# ====== jwt
from model import jwt_decode
from model import jwt_encode


from model import get_account_information_by_person_id
from model import change_email_is_not_exist
from model import update_account_information
from model import register_data_is_empty
from model import check_email_format




@member.route("/member",methods=["GET","POST"])
def api_member():
    if request.method=="GET":
        try:
            auth_header = request.headers.get('Authorization')
            token = auth_header.split(' ')[1]
            payload = jwt_decode(token)
            person_id = payload["data"]["id"]
            if not person_id:
                return jsonify({"error":True, "message": "身份驗證錯誤"})
            response = get_account_information_by_person_id(person_id)
            return jsonify(response)
        except:
            return jsonify({"error":True,"message":"系統異常，請聯繫客服處理"})


    if request.method=="POST":
        try:
            auth_header = request.headers.get('Authorization')
            token = auth_header.split(' ')[1]
            payload = jwt_decode(token)
            person_id = payload["data"]["id"]

            newMemberData = request.get_json()
            name = newMemberData["name"]
            email = newMemberData["email"]
            password = newMemberData["password"]

            print("newMemberData: ", newMemberData)
            print("----")

            if register_data_is_empty(name,email,password):
                return jsonify({"error":True,"message":"更新資料未填寫完整"})
            if not check_email_format(email):
                return jsonify({"error":True,"message":"信箱格式不符"})
            if not(change_email_is_not_exist(email)):
                return jsonify({"error":True,"message":"信箱重複，請更換"})
            person_information = update_account_information(name, email, password, person_id)
            token = jwt_encode(person_information)
            return jsonify({"token": token})

        except:
            return jsonify({"error":True,"message":"系統異常，請聯繫客服處理"})
