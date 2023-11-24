import unittest
from datetime import date

from currency_check import app


class TestHomeFunction(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app.test_client()
        self.today = date.today().strftime('%Y-%m-%d')

    def test_home_page(self) -> None:
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)

    def test_home_function_selected_date_valid(self) -> None:
        response = self.app.post('/', data={'date': self.today})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)

    def test_home_function_selected_date_invalid(self) -> None:
        response = self.app.post('/', data={'date': '2025-01-01'})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)


if __name__ == '__main__':
    unittest.main()
