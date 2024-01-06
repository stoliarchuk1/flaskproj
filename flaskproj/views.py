from flask import jsonify, request
from flaskproj import app
import uuid
from datetime import datetime


CATEGORIES = [
    {
        "id": 1,
        "name": "food"
    }
]

USERS = []


# GET /categories
# POST /categories

@app.route("/categories")
def get_categories():
    return jsonify({"categories": CATEGORIES})


@app.route("/category", methods=['POST'])
def create_category():
    request_data = request.get_json()
    category_id = str(uuid.uuid4())
    CATEGORIES.append({"id": category_id, "name": request_data["name"]})
    return jsonify(request_data)


@app.route("/category", methods=["DELETE"])
def delete_category():
    request_data = request.get_json()
    for i in CATEGORIES:
        if i['id'] == request_data["id"]:
            deleted_category = i
            break
    CATEGORIES.remove(deleted_category)
    return jsonify(deleted_category)


@app.route("/categories")
def get_categories():
    return jsonify({"categories": CATEGORIES})

