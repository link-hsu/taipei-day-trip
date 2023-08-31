from flask import Blueprint, jsonify, request
from models import attractions as attractions_model
import json

mrts = Blueprint("mrts", __name__)

@mrts.route("/mrts", methods=["GET"])
def query_mrts():
    try:
        data = json.loads(attractions_model.get_attraction_mrts_descending())
        data = {"data": [item["mrt"] for item in data if item["mrt"]]}
        return jsonify(data), 200

        # mrts = request.args.get("mrts", "")
        # for item in data:
        #     if not item["mrt"]:
        #         return jsonify({"error": True, "message": "something wrong for this data"})                 
        #     if item["mrt"] and mrts and mrts == item["mrt"]:
        #         return jsonify({"data": [item["mrt"]]}), 200
        # return jsonify({"error": True, "message": "No matching mrt station"}), 500

    except Exception as e:
        return jsonify({"error": True, "message": str(e)}), 500