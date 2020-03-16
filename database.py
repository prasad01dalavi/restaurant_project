from app import db
from models import Restaurant, RestaurantTable, User, Booking, Menu
import email_notification


def get_restaurants_list():
    restaurant_list = []
    restaurants = Restaurant.query.all()
    for restaurant in restaurants:
        restaurant_list.append({
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            'opened_at': restaurant.opened_at,
            'closed_at': restaurant.closed_at
        })
    return restaurant_list


def create_restaurant(restaurant_list):
    for restaurant in restaurant_list:
        database_query = Restaurant(
            name=restaurant['name'],
            address=restaurant['address'],
            opened_at=restaurant['opened_at'],
            closed_at=restaurant['closed_at']
        )
        db.session.add(database_query)
        db.session.commit()
    return {'status': 'success', 'reason': 'restaurants created'}


def create_table(table_list):
    for table in table_list:
        database_query = RestaurantTable(
            name=table['name'],
            restaurant=table['restaurant'],
            size=table['size'],
        )
        db.session.add(database_query)
        db.session.commit()
    return {'status': 'success', 'reason': 'tables created'}


def create_menu(menu_list):
    for menu in menu_list:
        database_query = Menu(
            name=menu['name'],
            restaurant=menu['restaurant'],
            price=menu['price'],
        )
        db.session.add(database_query)
        db.session.commit()
    return {'status': 'success', 'reason': 'menu created'}


def create_user(user_details):
    """
    Create new user if it's not present
    """
    user = User.query.filter_by(phone_number=user_details['phone_number'],
                                is_registered=True).first()
    # if user is already present then return its details
    if user:
        print(f'[INFO] User already exists!')
        return user, False
    else:
        # create new user
        new_user = User(
            first_name=user_details['first_name'],
            last_name=user_details['last_name'],
            phone_number=user_details['phone_number'],
            email=user_details['email'],
            is_registered=user_details['registration']
        )
        db.session.add(new_user)
        db.session.commit()
        print(f'[INFO] New user created!')
        return new_user, True


def get_tables(restaurant):
    tables = RestaurantTable.query.filter(RestaurantTable.restaurant ==
                                          restaurant)
    table_list = []
    for table in tables:
        table_list.append({
            "id": table.id,
            "name": table.name,
            "is_booked": table.is_booked,
            "size": table.size
        })
    return table_list


def get_menu(restaurant):
    menus = Menu.query.filter(Menu.restaurant == restaurant)
    menus_list = []
    for menu in menus:
        menus_list.append({
            "id": menu.id,
            "name": menu.name,
            "price": menu.price
        })
    return menus_list


def verify_booking_slot(booking_details):
    # Check for the date and time on which the booking is not done already
    table_bookings = Booking.query.filter(
        Booking.table == booking_details['table'])

    same_date = False  # Assume the new booking is not on already booked day

    for booking in table_bookings:
        print(f'[INFO] Verifying Booking ID: {booking.id}')
        if booking.date == booking_details['date']:
            print(f'[INFO] Booking present on this date!')
            print(f'[INFO] Lets check for time...')
            same_date = True
            # New booking is on the already booked day for that table

        expected_booking_time = int(booking_details["time"].replace(":", ""))
        existing_booking_time = int(booking.time.replace(":", ""))
        if not(expected_booking_time <= existing_booking_time-100) and \
                not(expected_booking_time >= existing_booking_time+100) and \
                same_date:
            print(f'[INFO] Already booked for same date and time!')
            response = {'status': 'failure',
                        'reason': 'Already booked for same date and time!'}
            return response
    return {'status': 'success'}


def create_new_booking(booking_details):
    print(f'[INFO] Creating new booking for this request!')
    # Create User entry in User Table
    user, status = create_user(booking_details['guest_details'])
    # Create Booking entry in Booking Table
    print(f'[INFO] Booking for User: {user.id}')
    bill = 0
    selected_menu = ""
    # If menu is selected then only calculate bill
    if booking_details['selected_menu']:
        for menu in booking_details['selected_menu']:
            price = Menu.query.get(menu).price
            bill += price
        selected_menu = ",".join(
            str(x) for x in booking_details['selected_menu'])
    booking = Booking(
        user=user.id,
        table=booking_details['table'],
        date=booking_details['date'],
        time=booking_details['time'],
        bill=bill,
        selected_menu=selected_menu
    )
    db.session.add(booking)
    db.session.commit()
    response = {
        "id": booking.id,
        "user": booking.user,
        "table": booking.table,
        "is_paid": booking.is_paid,
        "bill": booking.bill,
        "status": "success",
        "reason": "new booking created!"
    }
    subject = "Booking Confirmed!"
    restaurant_table = RestaurantTable.query.get(booking.table)
    restaurant = Restaurant.query.get(restaurant_table.restaurant).name
    text = f"""
    Congratulations {user.first_name}!

    Your Booking has been confirmed for following:
    Restaurant Name: {restaurant}
    Table: {restaurant_table.name}
    Date: {booking_details['date']}
    Time: {booking_details['time']}
    """
    email_notification.send(user.email, subject, text)
    return response


def book_table(booking_details):
    """
    1. Check for expected table size
    2. Check whether already booked
    3. Check booking date time
    4. Create User entry in User Table
    5. Create Booking entry in Booking Table
    """
    table = RestaurantTable.query.get(booking_details['table'])
    # Check for expected and available table size
    if table.size < booking_details['guest_count']:
        print(f'[INFO] Table size is less than the guest count!')
        response = {'status': 'failure',
                    'reason': 'Table size is less than the guest count!'}
        return response

    # First check whether time is as per the restaurant
    booking_time = int(booking_details['time'].replace(":", ""))
    restaurant_opened_at = int(Restaurant.query.get(
        table.restaurant).opened_at.replace(":", ""))
    restaurant_closed_at = int(Restaurant.query.get(
        table.restaurant).closed_at.replace(":", ""))
    if booking_time < restaurant_opened_at or \
            booking_time > restaurant_closed_at:
        print(f'[INFO] Restaurant is not available for the selected time!')
        response = {'status': 'failure',
                    'reason': 'Booking Time is out of restaurant Timings!'}
        return response

    print(f'[INFO] Table Booking Status: {table.is_booked}')
    if table.is_booked:
        print(f'[INFO] Table is already booked, Lets verify the date-time')
        response = verify_booking_slot(booking_details)
        if response['status'] == 'success':
            table.is_booked = True
            db.session.commit()
            response = create_new_booking(booking_details)
    else:
        print(f'[INFO] Table was not booked!')
        table.is_booked = True
        db.session.commit()
        response = create_new_booking(booking_details)
    return response


def get_bookings(user):
    booking = Booking.query.filter_by(user=user).first()
    if booking:
        response = {
            "id": booking.id,
            "user": booking.user,
            "table": booking.table,
            "bill": booking.bill,
            "is_paid": booking.is_paid,
            "date": booking.date,
            "time": booking.time,
            "status": "success",
            "reason": "found bookings for the requested user"
        }
    else:
        response = {
            "status": "failure",
            "reason": "couldnot find bookings for requested user"
        }
    return response


def pay_bill(billing):
    booking = Booking.query.get(billing['booking'])
    if booking:
        booking.bill = booking.bill - billing['amount']
        if booking.bill <= 0:
            booking.is_paid = True
        db.session.commit()
        response = {
            "id": booking.id,
            "user": booking.user,
            "table": booking.table,
            "bill": booking.bill,
            "is_paid": booking.is_paid,
            "date": booking.date,
            "time": booking.time,
            "status": "success",
            "reason": "bill paid"
        }
    else:
        response = {
            "status": "failure",
            "reason": "could not find requested booking"
        }
    return response
