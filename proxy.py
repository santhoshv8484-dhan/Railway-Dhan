from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")
CLIENT_ID = os.getenv("DHAN_CLIENT_ID")

DHAN_ENDPOINT = "https://api-dhan-sandbox.paymatrix.in/orders"

@app.route("/place", methods=["POST"])
def place_order():
    if not ACCESS_TOKEN:
        return jsonify({"error": "Missing DHAN_ACCESS_TOKEN"}), 500

    if not CLIENT_ID:
        return jsonify({"error": "Missing DHAN_CLIENT_ID"}), 500

    try:
        payload = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid JSON"}), 400

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "client-id": CLIENT_ID
    }

    try:
        response = requests.post(DHAN_ENDPOINT, json=payload, headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return "Dhan Sandbox Proxy Running", 200
