from app import db


class Restaurant(db.Model):
    """
    Restaurants information
    """
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(),
                           server_onupdate=db.func.now())
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    address = db.Column(db.String(20))
    opened_at = db.Column(db.String(20), default="10 AM")
    closed_at = db.Column(db.String(20), default="11 PM")

    def __repr__(self):
        return '<Restaurant %r>' % self.name


class RestaurantTable(db.Model):
    """
    Tables Details in a Restaurant
    """
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(),
                           server_onupdate=db.func.now())
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    restaurant = db.Column(db.Integer, db.ForeignKey('restaurant.id'),
                           nullable=False)
    size = db.Column(db.Integer)
    is_booked = db.Column(db.Boolean, default=False, nullable=False)


class User(db.Model):
    """
    User Information, Registration.
    """
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(),
                           server_onupdate=db.func.now())
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    phone_number = db.Column(db.String(10))
    email = db.Column(db.String(50))
    is_registered = db.Column(db.Boolean, default=False, nullable=False)


class Menu(db.Model):
    """
    Menus available in Restaurant
    """
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(),
                           server_onupdate=db.func.now())
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    restaurant = db.Column(db.Integer, db.ForeignKey('restaurant.id'),
                           nullable=False)
    price = db.Column(db.Integer, default=50)


class Booking(db.Model):
    """
    Booking Details
    """
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(),
                           server_onupdate=db.func.now())
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'),
                     nullable=False)
    table = db.Column(db.Integer, db.ForeignKey('restaurant_table.id'),
                      nullable=False)
    is_paid = db.Column(db.Boolean, default=False, nullable=False)
    bill = db.Column(db.Integer, default=0)
    date = db.Column(db.String(20))
    time = db.Column(db.String(20))
    selected_menu = db.Column(db.String(20), default="")  # comma seperated pks
