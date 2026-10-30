import unittest
from app import app


class CalculatorTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def calculate(self, first, second, operation):
        return self.client.post('/calculate', json={'first_number': first, 'second_number': second, 'operation': operation})

    def test_operations_and_decimal_inputs(self):
        cases = [(1.5, 2.25, '+', 3.75), (4, 2, '-', 2), (3, 2, '*', 6), (5, 2, '/', 2.5), (7, 3, '%', 1), (10, 21, '**', 1e21), (2, -2, '**', .25)]
        for first, second, op, expected in cases:
            with self.subTest(operation=op):
                response = self.calculate(first, second, op)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json['result'], expected)

    def test_invalid_requests_are_client_errors(self):
        for payload in [[], None, {}, {'first_number': True}, {'first_number': 'NaN'}, {'first_number': [1]}]:
            with self.subTest(payload=payload):
                self.assertEqual(self.client.post('/calculate', json=payload).status_code, 400)
        self.assertEqual(self.client.post('/calculate', data='{', content_type='application/json').status_code, 400)

    def test_bounds_and_undefined_arithmetic(self):
        cases = [(1, 0, '/'), (1, 0, '%'), (0, -1, '**'), (2, 1001, '**'), (1e12, 1000, '**'), (1e13, 1, '+'), (2, .5, '**'), (1, 2, 'unknown')]
        for first, second, op in cases:
            with self.subTest(first=first, second=second, op=op):
                self.assertEqual(self.calculate(first, second, op).status_code, 400)

    def test_request_size_limit(self):
        self.assertEqual(self.client.post('/calculate', data='x' * 5000, content_type='application/json').status_code, 413)


if __name__ == '__main__':
    unittest.main()
