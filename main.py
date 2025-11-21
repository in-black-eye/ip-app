import os
import requests
from flask import Flask, jsonify


app = Flask(__name__)

def get_ip_from_ip_api():
    response = requests.get("http://ip-api.com/json/")
    response.raise_for_status()
    data = response.json()
    return data.get("query")

def get_ip_from_jsonip():
    response = requests.get("https://jsonip.com/", timeout=5)
    response.raise_for_status()
    data = response.json()
    return data.get("ip")

@app.route("/")
def get_ip():
    api_type = os.getenv("TYPE", "ip-api").lower()

    ip_address = None
    if api_type == "ip-api":
        ip_address = get_ip_from_ip_api()
    elif api_type == "jsonip":
        ip_address = get_ip_from_jsonip()
    else:
        return jsonify({"error": "Ошибка в имени API."}), 400
    
    if ip_address:
        return jsonify({"myIP":ip_address, "API_TYPE":api_type})
    else:
        return jsonify({"error": "Ошибка в получении IP адреса."}), 500

app.run(host="localhost", port="5000")