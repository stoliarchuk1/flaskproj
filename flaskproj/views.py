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

USERS = [
    {
        "id": 1,
        "name": "Kolyan"
    }
]

RECORDS = [
    {
        "id": 1,
        "user_id": 1,
        "category_id": 1,
        "data_and_time": "123",
        "currency": 123
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


@app.route("/users")
def get_users():
    return jsonify({"users": USERS})


@app.route("/user", methods=['POST'])
def create_user():
    request_data = request.get_json()
    user_id = str(uuid.uuid4())
    USERS.append({"id": user_id, "name": request_data["name"]})
    return jsonify(request_data)


@app.route("/user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    for i in USERS:
        if i['id'] == int(user_id):
            deleted_user = i
            break
    USERS.remove(deleted_user)
    return jsonify(deleted_user)


@app.route("/user/<user_id>")
def get_user_by_id(user_id):
    for i in USERS:
        if i['id'] == int(user_id):
            user = i
            break
    return jsonify(user)


@app.route("/records")
def get_records():
    return jsonify({"records": RECORDS})


@app.route("/record", methods=['POST'])
def create_record():
    request_data = request.get_json()
    record_id = str(uuid.uuid4())
    RECORDS.append({"id": record_id,
                    "user_id": request_data["user_id"],
                    "category_id": request_data["category_id"],
                    "date_and_time": datetime.now(),
                    "currency": request_data["currency"]})
    return jsonify(request_data)


@app.route("/record/<record_id>", methods=["DELETE"])
def delete_record(record_id):
    for i in RECORDS:
        if i['id'] == int(record_id):
            deleted_record = i
            break
    USERS.remove(deleted_record)
    return jsonify(deleted_record)


@app.route("/record")
def get_record():
    request_data = request.get_json()
    records = []
    try:
        category_id = request_data['category_id']
        user_id = request_data['user_id']
    except:
        try:
            category_id = request_data['category_id']
        except:
            try:
                user_id = request_data['user_id']
            except:
                records = {"Error": "no one args"}
            else:
                records = []
                for i in RECORDS:
                    if i["user_id"] == user_id:
                        records.append(i)
        else:
            for i in RECORDS:
                if i["category_id"] == category_id:
                    records.append(i)
    else:
        for i in RECORDS:
            if i["user_id"] == user_id & i["category_id"] == category_id:
                records.append(i)
    finally:
        return jsonify(records)
