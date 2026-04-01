from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

DB_FILE = "users.json"


def load_users():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    users = load_users()

    if data["username"] in users:
        return jsonify({"status": "error", "message": "User exists"})

    users[data["username"]] = data["password"]
    save_users(users)

    return jsonify({"status": "ok"})


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    users = load_users()

    if users.get(data["username"]) == data["password"]:
        return jsonify({"status": "ok"})

    return jsonify({"status": "error"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)