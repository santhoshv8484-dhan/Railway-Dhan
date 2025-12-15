from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")
CLIENT_ID = os.getenv("DHAN_CLIENT_ID")

DHAN_ENDPOINT = "https://api-sandbox.dhan.co/orders"

@app.route("/place", methods=["POST"])
def place_order():
    if not ACCESS_TOKEN:
        return jsonify({"error": "DHAN_ACCESS_TOKEN missing"}), 500
    if not CLIENT_ID:
        return jsonify({"error": "DHAN_CLIENT_ID missing"}), 500

    try:
        payload = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid JSON payload"}), 400

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "client-id": CLIENT_ID
    }

    response = requests.post(DHAN_ENDPOINT, json=payload, headers=headers)

    try:
        return jsonify(response.json()), response.status_code
    except Exception:
        return response.text, response.status_code


@app.route("/", methods=["GET"])
def home():
    return "Dhan Proxy Running on Railway", 200
