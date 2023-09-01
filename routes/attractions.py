from flask import Blueprint, jsonify, request
from models import attractions as attractions_model
import json
import re

attractions = Blueprint("attractions", __name__)

def filter_imagelink(file):    
    def is_imagelink(link):
        return link.lower().endswith((".png", ".jpg"))
    images = file.split("https://")
    images = ["https://" + image for image in images if is_imagelink(image)]    
    return images

@attractions.route("/attractions", methods=["GET"])
def search_page_and_keyword():
    page = request.args.get("page", "")
    keyword = request.args.get("keyword", "")

    def data_for_page(name_data, data_per_page):
        page_results = []
        for i in range(0, len(name_data), data_per_page):
            grouping = name_data[i:i + data_per_page]
            page_result = {"nextPage": (i // data_per_page) + 1, "data": grouping}
            page_results.append(page_result)
        return page_results

    try:
        data = json.loads(attractions_model.get_attraction_table("name"))
        for item in data:
            item["images"] = filter_imagelink(item["images"])

        results_total = []
        if keyword:
            for item in data:
                if not item["mrt"]:
                    continue
                if keyword in item["mrt"] or re.search(keyword, item["name"]):
                    results_total.append(item)
            if not results_total:
                return jsonify({"error": True, "message": "No matching mrt and attraction"}), 500
            if page:
                results = data_for_page(results_total, 12)
                for result in results:
                    if result["nextPage"] == int(page):
                        return jsonify(result), 200
                    else:
                        return jsonify({"error": True, "message": "Searching page doesn't exist"}), 500
            else:
                return jsonify(data_for_page(results_total, 12)), 200
        elif page:
            results = data_for_page(data, 12)
            for result in results:
                if result["nextPage"] == int(page):
                    return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500
            

@attractions.route("/attractions/<attractionID>")
def search_by_id(attractionID):
    try:
        data = json.loads(attractions_model.get_attraction_table("name"))
        results = []
        for item in data:
            if int(attractionID) == item["id"]:
                item["images"] = filter_imagelink(item["images"])
                return jsonify({"data": item}), 200      
        return jsonify({"error": True, "message": "No matching attraction ID"}), 400
    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500

