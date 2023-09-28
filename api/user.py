from flask import *
from flask import jsonify

from model import register_data_is_empty
from model import register_email_exist
from model import register

from model import signin_data_is_empty
from model import signin_account_exist

from model import check_email_format
from model import check_user_id_in_token_exist

from model.jwt import jwt_encode
from model.jwt import jwt_decode

user = Blueprint("user", __name__)
user_auth = Blueprint("user_auth", __name__)

@user.route("/user", methods=["POST"])
def api_user():
    try: 
        registerDataFromFrontEnd = request.get_json()
        name = registerDataFromFrontEnd.get("name")
        email = registerDataFromFrontEnd.get("email")
        password = registerDataFromFrontEnd.get("password")
        if register_data_is_empty(name, email, password):
            return jsonify({"error": True, "message": "有註冊資料未填寫"})
        if not check_email_format(email):
            return jsonify({"error": True, "message": "信箱格式有誤，請重新註冊"})
        if register_email_exist(email):
            return jsonify({"error": True,"message": "信箱已經註冊，請重新註冊"})
        if register(name, email, password):
            return jsonify({"ok": True})
    except Exception as e:
        print("error for api_user: ", e)
        return jsonify({"error": True, "message": "伺服器內部錯誤 500"})

@user_auth.route("/user/auth", methods=["GET", "PUT"])
def api_user_auth():
    if request.method == "PUT":
        try:
            signinDataFromFrontEnd = request.get_json()
            email = signinDataFromFrontEnd["email"]
            password = signinDataFromFrontEnd["password"]
            if signin_data_is_empty(email, password):
                return jsonify({"error": True, "message": "請輸入電子信箱及密碼"})
            if not signin_account_exist(email, password):
                return jsonify({"error": True, "message": "登入失敗 400"})
            person_information = signin_account_exist(email, password)
            token = jwt_encode(person_information)
            return jsonify({"token": token})

        except Exception as e:
            print("api_user_auth inetrnal server error: ",e)
            return jsonify({"error": True, "message": "伺服器內部錯誤 500"})
        
    if request.method == "GET":
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(' ')[1]
                payload = jwt_decode(token)
                return jsonify(payload)
            except:
                return jsonify({'data': None})