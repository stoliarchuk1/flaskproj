from flask import  jsonify, request
from flaskproj import app


CATEGORIES = [
    {
        "id": 1,
        "name": "Food"
    }
]


# GET /categories
# POST /categories

@app.route("/categories")
def get_categories():
    return jsonify({"categories": CATEGORIES})


@app.route("/category", methods=['POST'])
def create_category():
    request_data = request.get_json()
    CATEGORIES.append(request_data)
    return jsonify(request_data)

