# Calculator API

A Flask JSON API that performs arithmetic for the companion [React calculator](https://github.com/daleloncosky/calculator-frontend). It validates requests, handles mathematical errors as client errors, and returns finite results without truncating decimal operands or applying an unintended modulus to exponentiation.

## Run locally

Use Python 3.11 or newer.

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python app.py
```

The development server binds to `127.0.0.1:5001`. Export `PORT` to change the port. Export `ALLOWED_ORIGINS` with a comma-separated list of exact browser origins when using a different frontend. `.env.example` documents these variables; `python app.py` reads process environment variables directly.

## API

```sh
curl http://localhost:5001/health
curl -X POST http://localhost:5001/calculate \
  -H 'Content-Type: application/json' \
  -d '{"first_number":1.5,"second_number":2.25,"operation":"+"}'
```

The second request returns `{"result":3.75}`.

| Operation | Behavior |
| --- | --- |
| `+`, `-`, `*` | Addition, subtraction, multiplication |
| `/` | Division; rejects a zero divisor |
| `%` | Python modulo semantics; rejects a zero divisor |
| `**` | Exponentiation with an integer exponent from -1000 to 1000 |

Operands must be finite numbers with magnitude at most 1e12. Results use Python floating-point arithmetic and may be approximate. Non-finite or overflowing results are rejected. Invalid JSON, booleans, arrays, missing values, unsupported operators, and arithmetic errors return HTTP 400 with an `error` string. Bodies over 4 KiB return 413.

## Test and deploy

```sh
python -m unittest discover -s tests -v
gunicorn --bind 0.0.0.0:5001 app:app
```

Tests cover every operation, decimal inputs, large powers, negative exponents, malformed requests, bounds, and request-size limits. For a public deployment, supply HTTPS through the hosting platform and add request limits. CORS is not authentication. This demo includes no accounts, database, or calculation history.
