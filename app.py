from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows frontend to communicate with the backend

# Function to perform calculation
def calculate(first_number, second_number, operation):
    try:
        first_number = float(first_number)
        second_number = float(second_number)

        if operation == "+":
            result = first_number + second_number
        elif operation == "-":
            result = first_number - second_number
        elif operation == "*" or operation == "x":
            result = first_number * second_number
        elif operation == "/":
            if second_number == 0:
                return {"error": "Division by zero is not allowed."}
            result = first_number / second_number
        elif operation == "%":
            if second_number == 0:
                return {"error": "Modulo by zero is not allowed."}
            result = first_number % second_number
        elif operation == "**" or operation == "^":
            result = first_number ** second_number
        else:
            return {"error": "Invalid operation."}

        return {"result": result}

    except ValueError:
        return {"error": "Invalid input. Please enter valid numbers."}

# API Endpoint to perform calculations
@app.route("/calculate", methods=["POST"])
def calculate_route():
    data = request.get_json()
    first_number = data.get("first_number")
    second_number = data.get("second_number")
    operation = data.get("operation")
    
    response = calculate(first_number, second_number, operation)
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)