import json
import mysql.connector

with open("./taipei-attractions.json", "r") as json_attractions:
    attractions = json.load(json_attractions)

attractions = attractions["result"]["results"]

con = mysql.connector.connect(
    user = "root",
    password = "123456789",
    host = "localhost",
    database = "attraction")
print("connnect to mysql successfully")
cursor = con.cursor()

def filter_imagelink(file):    
    def is_imagelink(link):
        return link.lower().endswith((".png", ".jpg"))
    images = file.split("https://")
    images = ["https://" + image for image in images if is_imagelink(image)]    
    return images

attraction_mrt = {}

count = 0
for attraction in attractions:
    id = attraction["_id"]
    name = attraction["name"]
    category = attraction["CAT"]
    description = attraction["description"]
    address = attraction["address"].replace(" ", "")
    transport = attraction["direction"]        
    mrt = attraction["MRT"]
    lat = float(attraction["latitude"])
    lng = float(attraction["longitude"])
    images = attraction["file"]

    images_sep = filter_imagelink(attraction["file"])

    cursor.execute("INSERT INTO attraction_name (id, name, category, description, address, transport, mrt, lat, longitude, images) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (id, name, category, description, address, transport, mrt, lat, lng, images))
    con.commit()
    
    for image in images_sep:
        cursor.execute("INSERT INTO attraction_image (name, image) VALUES (%s, %s)",
                   (name, image))
        con.commit()

    if mrt in attraction_mrt:
        attraction_mrt[mrt] += 1
    else:
        attraction_mrt[mrt] = 1

for key, value in attraction_mrt.items():
    cursor.execute("INSERT INTO attraction_mrt (mrt, count) VALUES (%s, %s)", (key, value)) 
    con.commit()

cursor.close()
con.close()
