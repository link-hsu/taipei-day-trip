import os
from flask import jsonify
from flask import *
import mysql.connector
import re

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


# ====== booking
# ====== bookging_data_is_empty
def booking_data_is_empty(booking_attraction_id,booking_date,booking_price,booking_time):
    if booking_attraction_id == "" or booking_date == "" or booking_price == "" or booking_time == "":
        return True
    else:
        return False

# ====== booking_people_exist
def booking_people_exist(person_id):
    try:
        con = get_con()
        cursor = con.cursor(dictionary = True)
        sql_check = "SELECT * FROM  reservationflash  WHERE  personId = %s"
        adr_check = (person_id,)
        cursor.execute(sql_check, adr_check)
        myresult_check = cursor.fetchone()
        print("myresult_check", myresult_check)
        if myresult_check != None:
            print("myresult_check", myresult_check)
            return myresult_check
        else:
            return False
    except Exception as e:
        print("error for booking_people_exist()", e)
    finally:
        cursor.close()
        con.close()

# ====== booking_register_people_exist
def booking_register_people_exist(person_id):
    try:
        con = get_con()
        cursor = con.cursor(dictionary=True)
        sql_check = "SELECT * FROM accounts WHERE id_people = %s"
        adr_check = (person_id,)
        cursor.execute(sql_check, adr_check)
        myresult_checkEmail = cursor.fetchone()
        if myresult_checkEmail != None:
            return True
        else:
            return False
    except Exception as e:
        print("error for Database register_email_exist(): ", e)
    finally:
        cursor.close()
        con.close()






# ====== update_booking_data
def update_booking_data(booking_attraction_id, booking_date, booking_price, booking_time, person_id):
    try:
        con = get_con()
        cursor = con.cursor(dictionary = True)
        print("update_booking_data() line 147")
        print("booking_attraction_id:", type(booking_attraction_id))
        print("booking_date:",type(booking_date))
        print("booking_price:",type(booking_price))
        print("booking_time:",type(booking_time))
        print("person_id:", type(person_id))

        sql_update="UPDATE reservationflash SET attractionId=%s,date=%s,price=%s,time=%s WHERE personId=%s"
        val_update=(booking_attraction_id,booking_date,booking_price,booking_time,person_id)
        print()
        cursor.execute(sql_update, val_update)
        con.commit()
        
    except Exception as e:
        print("line 152 error for update_booking_data()", e) 
    finally:
        cursor.close()
        con.close()


# ====== insert_booking_data
def insert_booking_data(booking_attraction_id,booking_date,booking_price,booking_time,person_id):
    try:
        con = get_con()
        cursor = con.cursor(dictionary = True)
        sql_deposit="INSERT INTO reservationflash(attractionId,date,price,time,personId) VALUES(%s,%s,%s,%s,%s)"
        val_deposit=(booking_attraction_id,booking_date,booking_price,booking_time,person_id)
        cursor.execute(sql_deposit,val_deposit)
        con.commit()
    except Exception as e:
        print("DealDatabase insert_booking_data()發生問題", e)
    finally:
        cursor.close()
        con.close()


# ====== get_data_for_booking_page
def get_data_for_booking_page(person_id):
    try:
        con = get_con()
        cursor = con.cursor(dictionary=True)
        sql = "SELECT attraction_name.id AS attraction_id, attraction_name.name, attraction_name.address, attraction_name.images, reservationflash.date, reservationflash.time, reservationflash.price, reservationflash.id AS reservationflash_id FROM attraction_name INNER JOIN reservationflash ON reservationflash.personId=%s and attraction_name.id = reservationflash.attractionId ORDER BY reservationflash.id DESC LIMIT 1"
        val = (person_id, )
        cursor.execute(sql, val)
        myresult = cursor.fetchone()
        print("get_data_for_booking_page original ", myresult)
        
        if myresult == None:
            return ({"error": True, "message": "No matching data"})
        img = filter_imagelink(myresult["images"])
        # img = myresult["images"].split(" ")
        data_for_booking_page = (
            {
                "data":{
                    "attraction":{
                        "id": myresult["attraction_id"],
                        "name": myresult["name"],
                        "address": myresult["address"],
                        "image": img[0],
                    },
                    "date": myresult["date"],
                    "time": myresult["time"],
                    "price": myresult["price"],
                },
            })
        print("data_for_booking_page: ", data_for_booking_page)
        return (data_for_booking_page)
    except Exception as e:
        print("error for get_data_for_booking_page()", e)
        return ({"error": True, "message": "伺服器內部問題"})
    finally:
        cursor.close()
        con.close()

# ====== delete_data_for_booking_page
def delete_data_for_bookin_page(attractio_id,person_id):
    try:
        con = get_con()
        cursor = con.cursor(dictionary=True)
        sql = "DELETE FROM reservationflash WHERE attractionId = %s and personId = %s"
        val = (attractio_id,person_id)
        print("attraction_id: ", attractio_id)
        print("attraction_id: ", type(attractio_id))
        print("person_id: ", type(person_id))
        print("ready to delete")
        cursor.execute(sql, val)
        con.commit()
    except Exception as e:
        print("error for delete_data_for_bookin_page", e)
    finally:
        cursor.close()
        con.close()


# ====== deal_orders
# ====== order_data_is_empty
def order_data_is_empty(order_data_from_frontEnd):
    prime=order_data_from_frontEnd["prime"]
    order_price=order_data_from_frontEnd["order"]["price"]
    attraction_id=order_data_from_frontEnd["order"]["trip"]["attraction"]["id"]
    attraction_name=order_data_from_frontEnd["order"]["trip"]["attraction"]["name"]
    attraction_address=order_data_from_frontEnd["order"]["trip"]["attraction"]["address"]
    attraction_image=order_data_from_frontEnd["order"]["trip"]["attraction"]["image"]
    order_date=order_data_from_frontEnd["order"]["trip"]["date"]
    order_time=order_data_from_frontEnd["order"]["trip"]["time"]
    contact_name=order_data_from_frontEnd["order"]["contact"]["name"]
    contact_email=order_data_from_frontEnd["order"]["contact"]["email"]
    contact_phone=order_data_from_frontEnd["order"]["contact"]["phone"]
    if prime == "" or order_price == "" or attraction_id == "" or attraction_name == "" or attraction_address == "" or attraction_image == "" or order_date == "" or order_time == "" or contact_name == "" or contact_email == "" or contact_phone == "":
        return True








# ====== order_reservation_exist
def order_reservation_exist(person_id, order_data_from_frontEnd):
    try:
        con = get_con()
        cursor = con.cursor(dictionary=True)
        attraction_id = order_data_from_frontEnd["order"]["trip"]["attraction"]["id"]
        sql = "SELECT * FROM reservationflash WHERE personId = %s AND attractionId = %s ORDER BY id DESC LIMIT 1"
        adr = (person_id, attraction_id)
        cursor.execute(sql, adr)
        myresult = cursor.fetchone()
        if myresult != None:
            return True
    except Exception as e:
        print("error for order_reservation_exist: ",e)
    finally:
        cursor.close()
        con.close()

# ====== write_historical_order
def write_historical_order(person_id, order_data_from_frontEnd):
    try:
        con = get_con()
        cursor = con.cursor(dictionary=True)
        order_contact_name = order_data_from_frontEnd["order"]["contact"]["name"]
        order_contact_email = order_data_from_frontEnd["order"]["contact"]["email"]
        order_contact_phone = order_data_from_frontEnd["order"]["contact"]["phone"]
        order_date = order_data_from_frontEnd["order"]["trip"]["date"]
        order_time = order_data_from_frontEnd["order"]["trip"]["time"]
        order_attraction_id = order_data_from_frontEnd["order"]["trip"]["attraction"]["id"]
        order_price = order_data_from_frontEnd["order"]["price"]

        sql = "INSERT INTO historical_order(order_account_id, order_contact_name, order_contact_email, order_contact_phone, order_date, order_time, order_attraction_id, order_price) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (person_id, order_contact_name, order_contact_email, order_contact_phone, order_date, order_time, order_attraction_id, order_price)
        cursor.execute(sql, val)
        con.commit()
        sql = "SELECT order_number FROM historical_order ORDER BY order_number DESC LIMIT 1;"
        cursor.execute(sql)
        last_order_number = cursor.fetchone()
        return last_order_number["order_number"]
    except Exception as e:
        print("error for write_historical_order: ", e)
    finally:
        cursor.close()
        con.close()
    
# ====== write_transaction_record_in_historical_order
from datetime import datetime
def write_transaction_record_in_historical_order(the_last_order_number, tappay_api_response):
    try:
        con = get_con()
        cursor = con.cursor(dictionary=True)
        sql = "UPDATE historical_order SET order_status = %s WHERE order_number = %s"
        val = (tappay_api_response["status"], the_last_order_number)
        cursor.execute(sql, val)
        con.commit()
        return True
    except Exception as e:
        print("error for write_transaction_record_in_historical_order: ", e)
    finally:
        cursor.close()
        con.close()
 

#  ====== delete_reservation_flash_by_person_id
def delete_reservation_flash_by_person_id(person_id):
    try:
        con = get_con()
        cursor = con.cursor(dictionary=True)
        sql = "DELETE FROM reservationflash WHERE personId = %s"
        val = (person_id, )
        cursor.execute(sql, val)
        con.commit()
    except Exception as e:
        print("delete_reservation_flash_by_person_id", e)
    finally:
        cursor.close()
        con.close()

# ====== get_transaction_record_in_historical_order
def get_transaction_record_in_historical_order(the_last_order_number):
    try:
        con = get_con()
        cursor = con.cursor(dictionary=True)
        sql = "SELECT order_date, order_status FROM historical_order WHERE order_number = %s;"
        val = (the_last_order_number, )
        cursor.execute(sql, val)
        transaction_record = cursor.fetchone()
        
        if transaction_record["order_status"] == 0:
            return({
                "data": {
                    "number": str(transaction_record["order_date"])+"-"+str(the_last_order_number),
                    "payment": {
                    "status": transaction_record["order_status"],
                    "message": "付款成功"
                    }
                }
            })
        else:
            return({
                "error": True,
                "message": transaction_record["order_status"],
                # "number": str(transaction_record["transaction_time"] + str(the_last_order_number))
            })
    except Exception as e:
        print("error for get_transaction_record_in_historical_order(): ", e)
    finally:
        cursor.close()
        con.close()

# ====== get_transaction_record_by_order_number
def get_transaction_record_by_order_number(order_number):
    try:
        con = get_con()
        cursor = con.cursor(dictionary=True)
        sql = "SELECT order_attraction_id FROM historical_order WHERE order_number = %s"
        val = (order_number,)
        cursor.execute(sql, val)
        order_attraction_id = cursor.fetchone()["order_attraction_id"]
        print("order_number: ", order_number)
        print("order_attraction_id: ", order_attraction_id)
        
        sql = "SELECT * FROM historical_order INNER JOIN attraction_name WHERE historical_order.order_number = %s AND attraction_name.id = %s"
        val = (order_number, order_attraction_id)
        cursor.execute(sql, val)
        print("-------------")
        total_record = cursor.fetchone()
        print(total_record)
        
        if total_record == None:
            return ({"error": True, "message": "歷史訂單中不存在此筆資料"})
        
        return(
			{
  				"data": {
    				"number": str(total_record["transaction_time"])+str(total_record["order_number"]),
    				"price": total_record["order_price"],
    				"trip": {
      					"attraction": {
        					"id": total_record["order_attraction_id"],
        					"name": total_record["name"],
        					"address": total_record["address"],
        					"image": total_record["images"].split(" ")[0]
      					},
      					"date": total_record["order_date"],
      					"time": total_record["order_time"]
    				},
					"contact": {
						"name": total_record["order_contact_name"],
						"email": total_record["order_contact_email"],
						"phone": total_record["order_contact_phone"]
					},
					"status": total_record["order_status"]
  				}
			}
        )
    except Exception as e:
        print("error for get_transaction_record_by_order_number(): ", e)
    finally:
        cursor.close()
        con.close()

# ====== get_transaction_record_by_transaction_number
def get_transaction_record_by_transaction_number(transaction_number, person_id):
    try:
        con = get_con()
        cursor = con.cursor(dictionary=True)
        transaction_number = str(transaction_number).replace(" ", "")
        print("transaction_number: ", transaction_number)
        order_date = transaction_number[:10]
        order_number = transaction_number[11:]
        print("order_date: ", order_date)
        print("order_number: ", order_number)
        sql = "SELECT * FROM historical_order WHERE order_number = %s AND order_date = %s AND order_account_id = %s ORDER BY order_number DESC"
        val = (order_number, order_date, person_id)
        cursor.execute(sql, val)
        total_record = cursor.fetchone()
        print("total_record: ", total_record)

        sql = "SELECT * FROM attraction_name WHERE id = %s"
        val = (total_record["order_attraction_id"],)
        cursor.execute(sql, val)
        attractions_information = cursor.fetchone()
        print("attractions_information: ", attractions_information)
        img = filter_imagelink(attractions_information["images"])

        if total_record != None:
            return(
				{
					"data": {
						"number": str(total_record["transaction_time"])+"-"+str(total_record["order_number"]),
						"price": total_record["order_price"],
						"trip": {
							"attraction": {
								"id": total_record["order_attraction_id"],
								"name": attractions_information["name"],
								"address": attractions_information["address"],
								"image": img[0]
							},
							"date": total_record["order_date"],
							"time": total_record["order_time"]
						},
						"contact": {
							"name": total_record["order_contact_name"],
							"email": total_record["order_contact_email"],
							"phone": total_record["order_contact_phone"]
						},
						"status": total_record["order_status"]
					}
				}

			)
    except Exception as e:
        print("error for get_transaction_record_by_transaction_number(): ", e)
    finally:
        cursor.close()
        con.close()         





# ====== member_page
# ====== get_account_information_by_person_id

def get_account_information_by_person_id(person_id):
    try:
        print("person_id: ", person_id)
        con = get_con()
        cursor = con.cursor(dictionary=True)
        sql_check = "SELECT * FROM accounts WHERE id_people=%s"
        adr_check = (person_id,)
        cursor.execute(sql_check,adr_check)
        myresult = cursor.fetchone()
        print("myresult get_account_information_by_person_id: ", myresult)
        return myresult   
    except Exception as e:
        print("member_model get_account_information_by_person_id()發生問題: ",e)
    finally:
        cursor.close()
        con.close()

# ====== change_email_is_not_exist
def change_email_is_not_exist(email):
    try:
        con = get_con()
        cursor = con.cursor(dictionary=True)
        sql_check = "SELECT * FROM accounts WHERE email=%s"
        adr_check = (email,)
        cursor.execute(sql_check,adr_check)
        myresult=cursor.fetchone()
        if myresult == None:
            return True
    except Exception as e:
        print("member_model change_email_is_not_exist()發生問題: ",e)
    finally:
        cursor.close()
        con.close()

# ====== update_account_information
def update_account_information(name,email,password,id_people):
    try:
        con = get_con()
        cursor = con.cursor(dictionary=True)
        sql = "UPDATE accounts SET name=%s, email=%s, password=%s WHERE id_people=%s"
        val = (name,email,password,id_people)	
        cursor.execute(sql,val)
        con.commit()
        
        person_information={
            "id_people": id_people,
            "name": name,
            "email": email
        }
        print("成功更新帳戶資料： ", person_information)
        return person_information 

    except Exception as e:
        print("member_model update_account_information()發生問題: ",e)
    finally:
        cursor.close()
        con.close()






# ========================	register	========================

# def register_email_exist(email):
# 	try:
# 		connection_object = connection_pool.get_connection()
# 		mycursor = connection_object.cursor(dictionary=True) # 設定fetchone跟fetchall有搜尋結果時的回傳都為字典形式
# 		sql_check="SELECT *FROM accounts WHERE email=%s"
# 		adr_check=(email,)
# 		mycursor.execute(sql_check,adr_check)
# 		myresult_checkEmail=mycursor.fetchone()
# 		if myresult_checkEmail != None:
# 			return True
# 	except:
# 		print("DealDatabase register_email_exist()發生問題")
# 	finally:
# 		mycursor.close()
# 		connection_object.close()
         


