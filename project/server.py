from flask import Flask, request, jsonify
import bcrypt

app = Flask(__name__)

users = {
    "lukas": {
        "password": bcrypt.hashpw(b"123", bcrypt.gensalt()),
        "premium": False,
        "banned": False
    }
}


@app.route("/login", methods=["POST"])
def login():
    data = request.json

    u = data["user"]
    p = data["pass"].encode()

    if u not in users:
        return {"status": "fail"}

    user = users[u]

    if bcrypt.checkpw(p, user["password"]):
        return {
            "status": "ok",
            "premium": user["premium"]
        }

    return {"status": "fail"}


@app.route("/premium", methods=["POST"])
def premium():
    u = request.json["user"]

    if u in users:
        users[u]["premium"] = True

    return {"status": "ok"}


@app.route("/users")
def all_users():
    return jsonify(users)


app.run(host="0.0.0.0", port=10000)