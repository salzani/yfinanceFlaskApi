from flask import Flask, request, jsonify
import json
import os
from datetime import datetime
from financeConsult import get_currency_value_att

app = Flask(__name__)

@app.route('/api/value/<currency>', methods=['GET'])
def get_currency_value_route(currency):
    try:
        currentValue = get_currency_value_att(currency)
        data = {
            "currency": currency,
            "value": currentValue
        }
        return jsonify(data)
    except ValueError as ex:
        return jsonify({"Error": str(ex)}), 400


############################## J S O N ##############################

data_file = 'data.json'

def read_data():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return []

def write_data(data):
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)


@app.route('/api/value', methods=['POST'])
def post_currency_value():
    try:
        if request.is_json:
            req_data = request.json
            print(f"Received JSON data: {req_data}")
            currency = req_data.get('currency')
            if not currency:
                return jsonify({"Error": "Currency is required"}), 400

            try:
                current_value = get_currency_value_att(currency)
            except ValueError as ex:
                return jsonify({"Error": str(ex)}), 400

            new_data = {
                "currency": currency,
                "value": current_value,
                "timestamp": datetime.now().isoformat()
            }

            data = read_data()
            print(f"Current data before update: {data}")

            data.append(new_data)

            write_data(data)
            print(f"Data after update: {data}")

            return jsonify(new_data)
        else:
            return jsonify({"Error": "Invalid Content-Type, expected application/json"}), 415
    except ValueError as ex:
        return jsonify({"Error": str(ex)}), 400

if __name__ == '__main__':
    app.run(debug=True)
