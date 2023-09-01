from flask import *
from routes.attractions import attractions
from routes.mrts import mrts
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

# attractions route setting
app.register_blueprint(attractions, url_prefix="/api/attractions")
app.register_blueprint(mrts, url_prefix="/api/mrts")


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