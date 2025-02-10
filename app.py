from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://calculator.hypsster.com"}})  # Accepts requests from front end only

@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        data = request.get_json()
        num1 = int(data.get("first_number"))
        num2 = int(data.get("second_number"))
        operation = data.get("operation")

        if operation == "**":
            result = pow(num1, num2, 10**20)
        elif operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        elif operation == "*":
            result = num1 * num2
        elif operation == "/":
            if num2 == 0:
                return jsonify({"error": "Division by zero is not allowed"}), 400
            result = num1 / nu
        elif operation == "%":
            if num2 == 0:
                return jsonify({"error": "Modulo by zero is not allowed"}), 400
            result = num1 % num2
        else:
            return jsonify({"error": "Invalid operation"}), 400

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
