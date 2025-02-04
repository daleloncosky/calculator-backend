from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Replace "*" with your frontend URL for better security
CORS(app, resources={r"/*": {"origins": ["https://calculator-frontend-three.vercel.app/calculate"]}})

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    first_number = float(data.get("first_number", 0))
    second_number = float(data.get("second_number", 0))
    operation = data.get("operation")

    if operation == "+":
        result = first_number + second_number
    elif operation == "-":
        result = first_number - second_number
    elif operation == "*":
        result = first_number * second_number
    elif operation == "/":
        if second_number == 0:
            return jsonify({"error": "Cannot divide by zero"}), 400
        result = first_number / second_number
    elif operation == "%":
        if second_number == 0:
            return jsonify({"error": "Cannot modulo by zero"}), 400
        result = first_number % second_number
    elif operation == "**":
        result = first_number ** second_number
    else:
        return jsonify({"error": "Invalid operation"}), 400

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
