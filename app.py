from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy


# MySQL Configerations
mysql_user = "root"
mysql_password = ""
mysql_db = "restaurant_db"

app = Flask(__name__)
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    f'mysql+pymysql://{mysql_user}:{mysql_password}@localhost:3306/{mysql_db}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
import database


@app.route('/hello')
def hello():
    return 'Hello, World!'


@app.route('/get_restaurants', methods=['GET'])
def get_restaurants():
    """
    Get Restaurants List
    """
    response = database.get_restaurants_list()
    return make_response(jsonify(response), 200)


@app.route('/create_restaurants', methods=['POST'])
def create_restaurants():
    restaurant_list = request.json
    response = database.create_restaurant(restaurant_list)
    return make_response(jsonify(response), 200)


@app.route('/create_tables', methods=['POST'])
def create_tables():
    table_list = request.json
    response = database.create_table(table_list)
    return make_response(jsonify(response), 200)


@app.route('/create_menu', methods=['POST'])
def create_menu():
    menu_list = request.json
    response = database.create_menu(menu_list)
    return make_response(jsonify(response), 200)


@app.route('/get_tables', methods=['POST'])
def get_tables():
    restaurant = request.json['restaurant']
    response = database.get_tables(restaurant)
    if response:
        return make_response(jsonify(response), 200)
    return make_response(
        jsonify({"status": "failure", "reason": "couldnot find tables"}), 400
    )


@app.route('/get_menu', methods=['POST'])
def get_menu():
    restaurant = request.json['restaurant']
    response = database.get_menu(restaurant)
    if response:
        return make_response(jsonify(response), 200)
    return make_response(
        jsonify({"status": "failure", "reason": "couldnot find menus"}), 400
    )


@app.route('/book_table', methods=['POST'])
def book_table():
    booking_details = request.json
    response = database.book_table(booking_details)
    if response['status'] == 'failure':
        return make_response(jsonify(response), 400)
    return make_response(jsonify(response), 200)


@app.route('/register', methods=['POST'])
def register():
    user_details = request.json
    user, status = database.create_user(user_details)
    if not(status):
        response = {
            "status": "failure",
            "reason": "User already exists!"
        }
    else:
        response = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number,
            'email': user.email,
            'is_registered': user.is_registered
        }
    return make_response(jsonify(response), 200)


@app.route('/get_bookings', methods=['POST'])
def get_bookings():
    user = request.json['user']
    response = database.get_bookings(user)
    if response['status'] == 'success':
        return make_response(jsonify(response), 200)
    return make_response(jsonify(response), 400)


@app.route('/pay_bill', methods=['POST'])
def pay_bill():
    billing = request.json
    response = database.pay_bill(billing)
    if response['status'] == "success":
        return make_response(jsonify(response), 200)
    return make_response(jsonify(response), 400)


if __name__ == '__main__':
    app.run(debug=True)
