from flask import Flask, request, jsonify, make_response, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github
from flask_sqlalchemy import SQLAlchemy


# MySQL Configurations
mysql_user = "root"
mysql_password = "your_root_password"
mysql_db = "restaurant_db"

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisissupposedtobeasecret'
# app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    f'mysql+pymysql://{mysql_user}:{mysql_password}@localhost:3306/{mysql_db}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

github_blueprint = make_github_blueprint(
    client_id='7fb389094ec4a2bddb52',
    client_secret='f959b9c41b9f0bd10c41dce1a5ce2c0bcd4209d0'
)

app.register_blueprint(github_blueprint, url_prefix='/github_login')

db = SQLAlchemy(app)
import database


@app.route('/get_restaurants', methods=['GET'])
def get_restaurants():
    """
    Get Restaurants List
    """
    response = database.get_restaurants_list()
    return make_response(jsonify(response), 200)


@app.route('/create_restaurants', methods=['POST'])
def create_restaurants():
    """
    Create Restaurants fake data
    """
    restaurant_list = request.json
    response = database.create_restaurant(restaurant_list)
    return make_response(jsonify(response), 200)


@app.route('/create_tables', methods=['POST'])
def create_tables():
    """
    Create Tables in Restaurants
    """
    table_list = request.json
    response = database.create_table(table_list)
    return make_response(jsonify(response), 200)


@app.route('/create_menu', methods=['POST'])
def create_menu():
    """
    Create Menu of Restaurant with price
    """
    menu_list = request.json
    response = database.create_menu(menu_list)
    return make_response(jsonify(response), 200)


@app.route('/get_tables', methods=['POST'])
def get_tables():
    """
    Get all tables in particular restaurant with its availability
    """
    restaurant = request.json['restaurant']
    response = database.get_tables(restaurant)
    if response:
        return make_response(jsonify(response), 200)
    return make_response(
        jsonify({"status": "failure", "reason": "couldnot find tables"}), 400
    )


@app.route('/get_menu', methods=['POST'])
def get_menu():
    """
    Get Menu available in restaurant to order/reserve
    """
    restaurant = request.json['restaurant']
    response = database.get_menu(restaurant)
    if response:
        return make_response(jsonify(response), 200)
    return make_response(
        jsonify({"status": "failure", "reason": "couldnot find menus"}), 400
    )


@app.route('/book_table', methods=['POST'])
def book_table():
    """
    Book Table (associated with restaurant) along with menu choice
    Get Email Notification of Booking Confirmation along with its details
    """
    booking_details = request.json
    response = database.book_table(booking_details)
    if response['status'] == 'failure':
        return make_response(jsonify(response), 400)
    return make_response(jsonify(response), 200)


@app.route('/register', methods=['POST'])
def register():
    """
    Register New User to the system
    """
    user_details = request.json
    user, status = database.create_user(user_details)
    if not(status):
        response = {
            "status": "failure",
            "reason": "User already exists!"
        }
        status_code = 400
    else:
        response = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number,
            'email': user.email,
            'is_registered': user.is_registered
        }
        status_code = 200
    return make_response(jsonify(response), status_code)


@app.route('/get_bookings', methods=['POST'])
def get_bookings():
    """
    Get Bookings of User which is for billing
    """
    user = request.json['user']
    response = database.get_bookings(user)
    if response['status'] == 'success':
        return make_response(jsonify(response), 200)
    return make_response(jsonify(response), 400)


@app.route('/pay_bill', methods=['POST'])
def pay_bill():
    """
    Pay Bill for the booking
    """
    billing = request.json
    response = database.pay_bill(billing)
    if response['status'] == "success":
        return make_response(jsonify(response), 200)
    return make_response(jsonify(response), 400)


@app.route('/github')
def github_login():
    """
    OAuth2.0 User Registration/Log In using github account
    """
    if not github.authorized:
        return redirect(url_for('github.login'))

    account_info = github.get('/user')

    if account_info.ok:
        account_info_json = account_info.json()
        response = database.verify_user(account_info_json)
        if response['status'] == 'success':
            return make_response(jsonify(response), 200)

    return make_response(jsonify(response), 400)


if __name__ == '__main__':
    app.run(debug=True)
