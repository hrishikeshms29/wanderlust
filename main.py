from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:hrishi2003@localhost:3306/wanderlust'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Add a secret key for Flask-Login
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'




@login_manager.user_loader
def load_user(user_id):
    # If not, check if the ID belongs to a ServiceProvider
    provider = ServiceProvider.query.get(int(user_id))
    print(type(provider))
    if provider:
        print(provider)
        return provider
    else:
        # Check if the ID belongs to a User
        user = User.query.get(int(user_id))
        print(user)
        if user:
            return user
    # If neither User nor ServiceProvider is found, return None
    return None
#
# # Service Provider loader
# @login_manager.user_loader
# def load_provider(provider_id):
#     return ServiceProvider.query.get(int(provider_id))

#models

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(255), nullable=False, unique=True)
    Password = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False, unique=True)
    def get_id(self):
        return str(self.UserID)

    @property
    def is_active(self):
        return True  # You can customize this based on your logic

    @property
    def is_authenticated(self):
        return True  # You can customize this based on your logic

    @property
    def is_anonymous(self):
        return False

    def __repr__(self):
        return f"<ServiceProvider {self.Username}>"


class ServiceProvider(db.Model):
    __tablename__ = 'serviceproviders'

    ServiceProviderID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(255), unique=True, nullable=False)
    PhoneNumber = db.Column(db.String(20))
    Email = db.Column(db.String(255))
    LogoOrPhoto = db.Column(db.String(255))
    BankDetails = db.Column(db.String(255))
    UPIScanImage = db.Column(db.String(255))
    Password = db.Column(db.String(255), nullable=False)
    def get_id(self):
        return str(self.ServiceProviderID)
    @property
    def is_active(self):
        return True  # You can customize this based on your logic
    @property
    def is_authenticated(self):
        return True  # You can customize this based on your logic
    @property
    def is_anonymous(self):
        return False
    def __repr__(self):
        return f"<ServiceProvider {self.Username}>"

class Package(db.Model):
    __tablename__ = 'packages'

    PackageID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ServiceProviderID = db.Column(db.Integer, db.ForeignKey('serviceproviders.ServiceProviderID'), nullable=False)
    PackageName = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text, nullable=False)
    Price = db.Column(db.DECIMAL(10,2), nullable=False)
    Duration = db.Column(db.Integer, nullable=False)
    Image = db.Column(db.String(255))

class Hotel(db.Model):
    __tablename__ = 'hotels'

    HotelID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ServiceProviderID = db.Column(db.Integer, db.ForeignKey('serviceproviders.ServiceProviderID'), nullable=False)
    HotelName = db.Column(db.String(255), nullable=False)
    Location = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text, nullable=False)

class Room(db.Model):
    __tablename__ = 'rooms'

    RoomID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    HotelID = db.Column(db.Integer, db.ForeignKey('hotels.HotelID'), nullable=False)
    RoomNumber = db.Column(db.Integer, nullable=False)
    IsAvailable = db.Column(db.Boolean, nullable=False, default=True)
    Capacity = db.Column(db.Integer, nullable=False)
    PricePerNight = db.Column(db.DECIMAL(10,2), nullable=False)
    Image = db.Column(db.String(255))

class Bus(db.Model):
    __tablename__ = 'buses'

    BusID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ServiceProviderID = db.Column(db.Integer, db.ForeignKey('serviceproviders.ServiceProviderID'), nullable=False)
    BusName = db.Column(db.String(255), nullable=False)
    DepartureCity = db.Column(db.String(255), nullable=False)
    ArrivalCity = db.Column(db.String(255), nullable=False)
    DepartureTime = db.Column(db.DateTime, nullable=False)
    ArrivalTime = db.Column(db.DateTime, nullable=False)
    Price = db.Column(db.DECIMAL(10,2), nullable=False)
    Image = db.Column(db.String(255))

class Booking(db.Model):
    __tablename__ = 'bookings'

    BookingID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    ServiceProviderID = db.Column(db.Integer, db.ForeignKey('serviceproviders.ServiceProviderID'))
    BookingDate = db.Column(db.DateTime, nullable=False)
    TotalPrice = db.Column(db.DECIMAL(10,2), nullable=False)
    BookingType = db.Column(db.String(50), nullable=False)
    RoomID = db.Column(db.Integer, db.ForeignKey('rooms.RoomID'))
    BusID = db.Column(db.Integer, db.ForeignKey('buses.BusID'))
    PackageID = db.Column(db.Integer, db.ForeignKey('packages.PackageID'))

class Review(db.Model):
    __tablename__ = 'reviews'

    ReviewID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    ServiceProviderID = db.Column(db.Integer, db.ForeignKey('serviceproviders.ServiceProviderID'))
    PackageID = db.Column(db.Integer, db.ForeignKey('packages.PackageID'))
    RoomID = db.Column(db.Integer, db.ForeignKey('rooms.RoomID'))
    BusID = db.Column(db.Integer, db.ForeignKey('buses.BusID'))
    Rating = db.Column(db.Integer, nullable=False)
    Comment = db.Column(db.Text)
    Date = db.Column(db.DateTime, nullable=False)

class Transaction(db.Model):
    __tablename__ = 'transactions'

    TransactionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    BookingID = db.Column(db.Integer, db.ForeignKey('bookings.BookingID'))
    TransactionDate = db.Column(db.DateTime, nullable=False)
    TransactionAmount = db.Column(db.DECIMAL(10,2), nullable=False)
    ServiceProviderID = db.Column(db.Integer, db.ForeignKey('serviceproviders.ServiceProviderID'))
    TransactionStatus = db.Column(db.String(255), nullable=False)

class BillingDetail(db.Model):
    __tablename__ = 'billingdetails'

    BillingID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    TransactionID = db.Column(db.Integer, db.ForeignKey('transactions.TransactionID'))
    BillingDate = db.Column(db.DateTime, nullable=False)
    TotalAmount = db.Column(db.DECIMAL(10,2), nullable=False)
    TaxAmount = db.Column(db.DECIMAL(10,2), nullable=False)
    DiscountAmount = db.Column(db.DECIMAL(10,2), nullable=False)
    GrandTotal = db.Column(db.DECIMAL(10,2), nullable=False)






#models end


#user functionalites only

#USer Signup Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        existing_user = User.query.filter_by(Username=username).first()
        if existing_user:
            return 'Username already exists! Choose a different username.'
        existing_user2 = User.query.filter_by(Email=email).first()
        if existing_user2:
            return 'Email Already in use Please try another email'
        existing_provider3 = ServiceProvider.query.filter_by(Username=username).first()
        if existing_provider3:
            return 'Username already exists! Choose a different username.'

        existing_provider4 = ServiceProvider.query.filter_by(Email=email).first()
        if existing_provider4:
            return 'Email already in use. Please try another email.'
        # Create a new user
        new_user = User(Username=username, Password=password, Email=email)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('user_home'))

    return render_template('signup.html')

#User Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(Username=username, Password=password).first()

        if user:
            login_user(user)
            return redirect(url_for('user_home'))

        return 'Invalid username or password. Please try again.'

    return render_template('login.html')

# Logout
# common logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))



#SERVICE PROVIDER FUCN
@app.route('/provider_login', methods=['GET', 'POST'])
def provider_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        provider = ServiceProvider.query.filter_by(Username=username, Password=password).first()

        if provider:
            login_user(provider)
            return redirect(url_for('provider_home'))

        return 'Invalid username or password. Please try again.'

    return render_template('provider_login.html')

@app.route('/provider_signup', methods=['GET', 'POST'])
def provider_signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone_number = request.form['phone_number']
        logo_or_photo = request.form['logo_or_photo']
        bank_details = request.form['bank_details']
        upi_scan_image = request.form['upi_scan_image']

        existing_provider = ServiceProvider.query.filter_by(Username=username).first()
        if existing_provider:
            return 'Username already exists! Choose a different username.'

        existing_provider2 = ServiceProvider.query.filter_by(Email=email).first()
        if existing_provider2:
            return 'Email already in use. Please try another email.'

        existing_user3 = User.query.filter_by(Username=username).first()
        if existing_user3:
            return 'Username already exists! Choose a different username.'
        existing_user4 = User.query.filter_by(Email=email).first()
        if existing_user4:
            return 'Email Already in use Please try another email'

        new_provider = ServiceProvider(
            Username=username,
            Password=password,
            Email=email,
            PhoneNumber=phone_number,
            LogoOrPhoto=logo_or_photo,
            BankDetails=bank_details,
            UPIScanImage=upi_scan_image
        )
        db.session.add(new_provider)
        db.session.commit()

        login_user(new_provider)
        return redirect(url_for('provider_home'))

    return render_template('provider_signup.html')


# route for service provider home
@app.route('/provider_home')
@login_required
def provider_home():
    if isinstance(current_user, ServiceProvider):
        return render_template('provider_home.html', username=current_user.Username)
    return 'You are not authorized to access this page.'

#END OF ser FUNC
# route for user home
@app.route('/user_home')
@login_required
def user_home():
    if isinstance(current_user, User):
        return render_template('user_home.html', username=current_user.Username)
    return 'You are not authorized to access this page.'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/all_buses')
@login_required
def all_buses():
    if isinstance(current_user, User):
        # Fetch all buses from the database
        all_buses = Bus.query.all()

        # Pass the buses to the template
        return render_template('all_buses.html', username=current_user.Username, buses=all_buses)

    return 'You are not authorized to access this page.'

#all_packages route
@app.route('/all_packages')
@login_required
def all_packages():
    if isinstance(current_user, User):
        # Pass the packages to the template
        all_packages = Package.query.all()
        return render_template('all_packages.html', username=current_user.Username, packages=all_packages)

    return 'You are not authorized to access this page.'







#provider funct
# Route for adding a new hotel
# Add a new hotel route
@app.route('/add_hotel', methods=['GET', 'POST'])
@login_required
def add_hotel():
    if isinstance(current_user, ServiceProvider):
        if request.method == 'POST':
            # Process form data
            hotel_name = request.form['hotel_name']
            location = request.form['location']
            description = request.form['description']

            # Create a new hotel instance
            new_hotel = Hotel(
                ServiceProviderID=current_user.ServiceProviderID,
                HotelName=hotel_name,
                Location=location,
                Description=description
            )

            # Add the new hotel to the database
            db.session.add(new_hotel)
            db.session.commit()

            flash('Hotel added successfully!')
            return redirect(url_for('provider_home'))

        return render_template('add_hotel.html', username=current_user.Username)

    return 'You are not authorized to access this page.'

# Add a new room route
# Add a new room route
@app.route('/add_room', methods=['GET', 'POST'])
@login_required
def add_room():
    if isinstance(current_user, ServiceProvider):
        # Check if there are hotels to associate rooms with
        hotels = Hotel.query.filter_by(ServiceProviderID=current_user.ServiceProviderID).all()
        if not hotels:
            flash('You need to add a hotel before adding rooms.')
            return redirect(url_for('add_hotel'))

        if request.method == 'POST':
            # Process form data
            hotel_id = request.form['hotel_id']
            room_number = request.form['room_number']
            capacity = request.form['capacity']
            price_per_night = request.form['price_per_night']
            image = request.form['image']

            # Create a new room instance
            new_room = Room(
                HotelID=hotel_id,
                RoomNumber=room_number,
                Capacity=capacity,
                PricePerNight=price_per_night,
                Image=image
            )

            # Add the new room to the database
            db.session.add(new_room)
            db.session.commit()

            flash('Room added successfully!')
            return redirect(url_for('provider_home'))

        # Provide hotels to the template
        return render_template('add_room.html', username=current_user.Username, hotels=hotels)

    return 'You are not authorized to access this page.'

# Route for adding a new bus
@app.route('/add_bus', methods=['GET', 'POST'])
@login_required
def add_bus():
    if isinstance(current_user, ServiceProvider):
        if request.method == 'POST':
            bus_name = request.form['bus_name']
            departure_city = request.form['departure_city']
            arrival_city = request.form['arrival_city']
            departure_time_str = request.form['departure_time']
            arrival_time_str = request.form['arrival_time']
            price = request.form['price']

            # Extract image file from the request
            image = request.files['image']

            # Convert string representations to appropriate types
            try:
                departure_time = datetime.strptime(departure_time_str, '%Y-%m-%dT%H:%M')
                arrival_time = datetime.strptime(arrival_time_str, '%Y-%m-%dT%H:%M')
                price = float(price)
            except ValueError:
                flash('Invalid date or price format.')
                return redirect(url_for('add_bus'))

            # Create a new bus instance
            new_bus = Bus(
                ServiceProviderID=current_user.ServiceProviderID,
                BusName=bus_name,
                DepartureCity=departure_city,
                ArrivalCity=arrival_city,
                DepartureTime=departure_time,
                ArrivalTime=arrival_time,
                Price=price,
                Image=image
            )

            # Add the new bus to the database
            db.session.add(new_bus)
            db.session.commit()

            flash('Bus added successfully!')
            return redirect(url_for('provider_home'))

        return render_template('add_bus.html', username=current_user.Username)

    return 'You are not authorized to access this page.'


# Route for adding a new package
@app.route('/add_package', methods=['GET', 'POST'])
@login_required
def add_package():
    if isinstance(current_user, ServiceProvider):
        if request.method == 'POST':
            # Process form data
            package_name = request.form['package_name']
            description = request.form['description']
            price = request.form['price']
            duration = request.form['duration']

            # Convert string representations to appropriate types
            try:
                price = float(price)
                duration = int(duration)
            except ValueError:
                flash('Invalid price or duration format.', 'error')
                return redirect(url_for('add_package'))

            # Create a new package instance
            new_package = Package(
                ServiceProviderID=current_user.ServiceProviderID,
                PackageName=package_name,
                Description=description,
                Price=price,
                Duration=duration
            )

            # Add the new package to the database
            db.session.add(new_package)
            db.session.commit()

            flash('Package added successfully!', 'success')
            return redirect(url_for('provider_home'))

        return render_template('add_packages.html', username=current_user.Username)

    return 'You are not authorized to access this page.'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)