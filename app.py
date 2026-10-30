"""A bounded JSON arithmetic API for the companion React calculator."""

import math
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 4096
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,https://calculator.hypsster.com").split(",")
CORS(app, resources={r"/calculate": {"origins": [x.strip() for x in origins if x.strip()]}})


def parse_number(value):
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        raise ValueError("Both operands must be finite numbers.")
    if isinstance(value, str) and (not value.strip() or len(value) > 64):
        raise ValueError("Both operands must be finite numbers.")
    number = float(value)
    if not math.isfinite(number) or abs(number) > 1e12:
        raise ValueError("Operands must be finite numbers with magnitude at most 1e12.")
    return number


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.errorhandler(413)
def payload_too_large(_error):
    return jsonify(error="Request body is too large."), 413


@app.post("/calculate")
def calculate():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Send a JSON object with first_number, second_number, and operation."), 400
    try:
        first = parse_number(data.get("first_number"))
        second = parse_number(data.get("second_number"))
        operation = data.get("operation")
        if operation in ("/", "%") and second == 0:
            raise ValueError("Division or modulo by zero is not allowed.")
        if operation == "+":
            result = first + second
        elif operation == "-":
            result = first - second
        elif operation == "*":
            result = first * second
        elif operation == "/":
            result = first / second
        elif operation == "%":
            result = first % second
        elif operation == "**":
            if not second.is_integer() or abs(second) > 1000:
                raise ValueError("The exponent must be an integer between -1000 and 1000.")
            result = math.pow(first, second)
        else:
            raise ValueError("Invalid operation.")
        if not math.isfinite(result):
            raise ValueError("The result is outside the supported numeric range.")
        if result.is_integer() and abs(result) <= 2**53 - 1:
            result = int(result)
        return jsonify(result=result)
    except (ValueError, TypeError, OverflowError) as error:
        message = str(error) if isinstance(error, ValueError) else "The result is outside the supported numeric range."
        return jsonify(error=message), 400


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5001")))
