"""
To run the test:
python -m unittest tests
"""

from app import app
import unittest
import json
import logging


logging.basicConfig(level=logging.DEBUG,
                    filename='tests_logs.log',
                    filemode='a',
                    format='%(levelname)s: Line:%(lineno)d %(asctime)s ==> %(message)s')

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        print(f"[INFO] Initial Setup!")
        logging.info(f"[INFO] Setting Up!")
        app.testing = True

    def tearDown(self):
        print(f"[INFO] End of Testing!")

    def test_get_restaurant(self):
        """
        Get list of restaurants for restaurant searching
        """
        url = "/get_restaurants"
        response = app.test_client().get(url)
        response_json = response.json
        with open('expected_responses/restaurants.json', 'r') as f:
            datastore = json.load(f)

        assert datastore == response_json, logging.error(
            "GET Restaurants Failed!")
        logging.info("GET Restaurants API Tested")

    def test_get_tables(self):
        """
        Get tables info(with availability) of particular restaurant
        """
        url = "/get_tables"
        data = {
            "restaurant": 1
        }
        response = app.test_client().post(url,
                                          json=data,
                                          content_type='application/json')
        assert response.status_code == 200, logging.error(
            "Getting Tables Failed!")
        logging.info("GET Tables Tested!")

    def test_get_menu(self):
        """
        Get Menus info of particular restaurant
        """
        url = "/get_menu"
        data = {
            "restaurant": 1
        }
        response = app.test_client().post(url,
                                          json=data,
                                          content_type='application/json')
        assert response.status_code == 200, logging.error(
            "Getting Menus Failed!")
        logging.info("GET Menu Tested!")

    def test_get_booking(self):
        """
        Get Booking info of particular user
        """
        url = "/get_bookings"
        data = {
            "user": 2
        }
        response = app.test_client().post(url,
                                          json=data,
                                          content_type='application/json')
        assert response.status_code == 200, logging.error(
            "GET Bookings Failed!")
        logging.info("GET Bookings Tested!")

    def test_book_table(self):
        """
        Book/Reserve a table in a restaurant
        """
        url = "/book_table"
        data = {
            "guest_details": {
                "first_name": "Prasad",
                "last_name": "Dalavi",
                "email": "prasad01dalavi@gmail.com",
                "phone_number": "8983050327",
                "registration": False
            },
            "time": "23:00",
            "date": "2020-03-16",
            "guest_count": 2,
            "table": 2,
            "selected_menu": [4]
        }

        response = app.test_client().post(url,
                                          json=data,
                                          content_type='application/json')
        assert response.status_code == 200, logging.error(
            "Booking Table Failed!")
        logging.info("Booking Table Tested!")

    def test_pay_bill(self):
        """
        Pay bill for the booking
        """
        url = "/pay_bill"
        data = {
            "booking": 4,
            "amount": 10
        }
        response = app.test_client().post(url,
                                          json=data,
                                          content_type='application/json')
        assert response.status_code == 200, logging.error(
            "Paying Bill Failed!")
        logging.info("Pay Bill Tested!")

    def test_simple_registration(self):
        """
        Register New User
        """
        url = "/register"
        data = {
            "first_name": "Prasad",
            "last_name": "Dalavi",
            "email": "personal-2",
            "phone_number": "8983050329",
            "registration": True
        }
        response = app.test_client().post(url,
                                          json=data,
                                          content_type='application/json')
        assert response.status_code == 200, logging.error(
            "User Registration Failed!")
        logging.info("User Registration Tested!")


if __name__ == '__main__':
    unittest.main()
