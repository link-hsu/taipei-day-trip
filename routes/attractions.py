from flask import Blueprint, jsonify, request
from models import attractions as attractions_model
import json
import re


attractions = Blueprint("attractions", __name__)



@attractions.route("", methods=["GET"])
def search_page_and_keyword():    
    page = request.args.get("page", "")
    keyword = request.args.get("keyword", "")    
    
    if page and keyword:
        return attractions_model.get_attration_page_keyword(page, keyword)
    if page:
        return attractions_model.get_attraction_page(page)
    if keyword:
        return attractions_model.get_attration_page_keyword(page, keyword)
    # except Exception as e:
    # return jsonify({"error": True, "message": str(e)}), 500


    

            

@attractions.route("/<attractionID>")
def search_by_id(attractionID):
    
    data = json.loads(attractions_model.get_attraction_search_id(int(attractionID)))
    if not data:
        return jsonify({"error": True, "message": "No matching attraction ID"}), 400
    elif data:
        return jsonify(data), 200      
    # except Exception as e:
    #     return jsonify({"error": True, "message": str(e)}), 500

