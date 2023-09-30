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
        if myresult_check != None:
            return myresult_check
        else:
            return False
    except:
        print("error for booking_people_exist()")
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
    except:
        print("error for Database register_email_exist()")
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
        sql = "SELECT attraction_name.id, attraction_name.name, attraction_name.address, attraction_name.images, reservationflash.date, reservationflash.time, reservationflash.price, reservationflash.id FROM attraction_name INNER JOIN reservationflash ON reservationflash.personId=%s and attraction_name.id = reservationflash.attractionId ORDER BY reservationflash.id DESC LIMIT 1"
        val = (person_id, )
        cursor.execute(sql, val)
        myresult = cursor.fetchone()
        
        print("get_data_for_booking_page: ", myresult)
        if myresult == None:
            return ({"error": True, "message": "No matching data"})
        img = filter_imagelink(myresult["images"])
        # img = myresult["images"].split(" ")
        data_for_booking_page = (
            {
                "data":{
                    "attraction":{
                        "id": myresult["id"],
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
        sql = "SELECT * FROM reservationflash WHERE personId = %s AND attractionId = %s"
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
        now = datetime.now()
        date_time = now.strftime("%Y%m%d%H%M%S")
        sql = "UPDATE historical_order SET transaction_time = %s, order_status = %s WHERE order_number = %s"
        val = (date_time, tappay_api_response["status"], the_last_order_number)
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
        sql = "SELECT transaction_time, order_status FROM historical_order WEHERE order_number = %s;"
        val = (the_last_order_number, )
        cursor.execute(sql, val)
        transaction_record = cursor.fetchone()
        
        if transaction_record["order_status"] == 0:
            return({
                "data": {
                    "number": str(transaction_record["transaction_time"]+str(the_last_order_number)),
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
                # 新增
                "number": str(transaction_record["transaction_time"] + str(the_last_order_number))
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
        transaction_time = str(transaction_number)[:14]
        order_number = str(transaction_number)[14:]

        sql = "SELECT * FROM historical_order WHERE order_number = %s AND transaction_time = %s AND order_account_id = %s"
        val = (order_number, transaction_time, person_id)
        cursor.execute(sql, val)
        total_record = cursor.fetchone()

        sql = "SELECT * FROM attraction_name WHERE id = %s"
        val = (total_record["order_attraction_id"],)
        cursor.execute(sql, val)
        attractions_information = cursor.fetchone()

        if total_record != None:
            return(
				{
					"data": {
						"number": str(total_record["transaction_time"])+str(total_record["order_number"]),
						"price": total_record["order_price"],
						"trip": {
							"attraction": {
								"id": total_record["order_attraction_id"],
								"name": attractions_information["name"],
								"address": attractions_information["address"],
								"image": attractions_information["images"].split(" ")[0]
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





         


