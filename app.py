from flask import *
from api.attractions import attractions
from api.user import user
from api.user import user_auth
from api.booking import booking
from api.orders import orders
from api.orders import order_num
# from api.thankyou import thankyou

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True



# attractions route setting
app.register_blueprint(attractions, url_prefix="/api")
app.register_blueprint(user, url_prefix="/api")
app.register_blueprint(user_auth, url_prefix="/api")
app.register_blueprint(booking, url_prefix="/api")
app.register_blueprint(orders, url_prefix="/api")
app.register_blueprint(order_num, url_prefix="/api")
# app.register_blueprint(thankyou)


# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

app.run(host="0.0.0.0", port=3000)
# app.run(port=3000)


