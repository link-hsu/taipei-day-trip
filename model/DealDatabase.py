import os
from flask import jsonify
from flask import *
import mysql.connector
import re

def get_con():
    con = mysql.connector.connect(
        user="root",
        password="123456789",
        host="localhost",
        database="attraction",
        auth_plugin="mysql_native_password"
        )
    return con


# ====== register_data_is_empty
def register_data_is_empty(name, email, password):
    if name == "" or email == "" or password == "":
        return True

# ====== register_email_exist
def register_email_exist(email):
    try:
        con = get_con()
        cursor = con.cursor(dictionary=True)
        sql_check = "SELECT * FROM accounts WHERE email = %s"
        adr_check = (email,)
        cursor.execute(sql_check, adr_check)
        myresult_checkEmail = cursor.fetchone()
        if myresult_checkEmail != None:
            return True
    except:
        print("error for Database register_email_exist()")
    finally:
        cursor.close()
        con.close()

# ====== register
def register(name, email, password):
    try:
        con = get_con()
        cursor = con.cursor(dictionary=True)
        sql_register = "INSERT INTO accounts (name, email, password) VALUES (%s, %s, %s)"
        val_register = (name, email, password)
        cursor.execute(sql_register, val_register)
        con.commit()
        return True
    except:
        print("error for register()")
    finally:
        cursor.close()
        con.close()

# ====== signin_data_is_empty
def signin_data_is_empty(email, password):
    if email == "" or password == "":
        return True


# ======= sign
def signin_account_exist(email, password):
    try:
        con = get_con()
        cursor = con.cursor(dictionary=True)
        sql_check = "SELECT * FROM accounts WHERE email = %s AND password = %s"
        adr_check = (email, password)
        cursor.execute(sql_check, adr_check)
        myresult_check = cursor.fetchone()
        if myresult_check != None:
            return myresult_check
    except:
        print("error for sginin_account_exist()")
    finally:
         cursor.close()
         con.close()


# ====== check_email_format
def check_email_format(email):
    if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        return True
    

# ====== check_user_id_in_token_exist
def check_user_id_in_token_exist(decode):
    try:
        user_id = decode["data"]["id"]
        con = get_con()
        cursor = con.cursor(dictionary = True)
        sql_check = "SELECT * FROM accounts WHERE id_people = %s"
        adr_check = (user_id,)
        cursor.execute(sql_check, adr_check)
        myresult = cursor.fetchone()
        if myresult != None:
            return True
    except:
        print("error for check_user_id_in_token_exist")
    finally:
        cursor.close()
        con.close()
