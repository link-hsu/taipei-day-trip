import os
from dotenv import load_dotenv
load_dotenv()
import requests



tappay_partner_key = os.getenv("TAPPAY_PARTNER_KEY")
tappay_merchant_id = os.getenv("TAPPAY_MERCHANT_ID")



def pay_by_prime_API(order_data_from_frontEnd):
    try:
        pay_data_for_api={
                "prime":order_data_from_frontEnd["prime"],
                "partner_key":tappay_partner_key,
                "merchant_id":tappay_merchant_id,
                "details":"TapPay Test",
                "amount":order_data_from_frontEnd["order"]["price"],
                "cardholder":{
                    "phone_number":order_data_from_frontEnd["order"]["contact"]["phone"],
                    "name":order_data_from_frontEnd["order"]["contact"]["name"],
                    "email":order_data_from_frontEnd["order"]["contact"]["email"]
                },
                "remember": True
            }
            
        url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": tappay_partner_key
        }
        response = requests.post(url, json=pay_data_for_api, headers=headers)
        print(response)
        print(response.status_code)
        print(response.json())
        return response.json()

    except Exception as e:
        print("tappay pay_by_prime_API()發生問題: ",e)