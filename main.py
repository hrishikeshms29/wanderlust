from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:hrishi2003@localhost:3306/trip'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'




@login_manager.user_loader
def load_user(user_id):
    provider = ServiceProvider.query.get(int(user_id))
    print(type(provider))
    if provider:
        print(provider)
        return provider
    else:
        user = User.query.get(int(user_id))
        print(user)
        if user:
            return user
    return None


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
    Image = db.Column(db.String(255))


class Room(db.Model):
    __tablename__ = 'rooms'

    RoomID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ServiceProviderID = db.Column(db.Integer, db.ForeignKey('serviceproviders.ServiceProviderID'))
    HotelID = db.Column(db.Integer, db.ForeignKey('hotels.HotelID'), nullable=False)
    RoomNumber = db.Column(db.Integer, nullable=False)
    IsAvailable = db.Column(db.Boolean, nullable=False, default=True)
    Capacity = db.Column(db.Integer, nullable=False)
    PricePerNight = db.Column(db.DECIMAL(10,2), nullable=False)
    Image = db.Column(db.String(255))
    RoomType = db.Column(db.String(255), nullable=False)


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
    IsAvailable = db.Column(db.Boolean, nullable=False, default=True)


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


class BillingDetail(db.Model):
    __tablename__ = 'billingdetails'

    BillingID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
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
        #all_buses = Bus.query.all()
        available_buses = Bus.query.filter_by(IsAvailable=True).all()

        # Pass the buses to the template
        return render_template('all_buses.html', username=current_user.Username, buses=available_buses, service_type='bus')

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


#all_hotels route
@app.route('/all_hotels')
@login_required
def all_hotels():
    if isinstance(current_user, User):
        # Fetch all hotels from the database
        all_hotels = Hotel.query.all()

        # Pass the hotels to the template
        return render_template('all_hotels.html', username=current_user.Username, hotels=all_hotels)

    return 'You are not authorized to access this page.'


# Route for fetching all rooms of a particular hotel
@app.route('/all_rooms/<int:hotel_id>')
@login_required
def all_rooms(hotel_id):
    if isinstance(current_user, User):
        selected_hotel = Hotel.query.get(hotel_id)

        if not selected_hotel:
            abort(404)  # Hotel not found

        #rooms = Room.query.filter_by(HotelID=hotel_id).all()
        available_rooms = Room.query.filter_by(HotelID=hotel_id, IsAvailable=True).all()

        # Pass the selected hotel and its rooms to the template
        return render_template('all_rooms.html', username=current_user.Username, hotel=selected_hotel, rooms=available_rooms)

    return 'You are not authorized to access this page.'

# Route to show all bookings for the logged-in user
@app.route('/all_bookings')
@login_required  # Use the @login_required decorator to ensure the user is logged in
def all_bookings():
    bookings = Booking.query.filter_by(UserID=current_user.UserID).all()
    return render_template('all_bookings.html', bookings=bookings)

# Route to show all billings for the logged-in user
@app.route('/all_billings')
@login_required
def all_billings():
    billings = BillingDetail.query.filter_by(UserID=current_user.UserID).all()
    return render_template('all_billings.html', billings=billings)


# Assuming your app variable is named 'app'
@app.route('/generate_bill/<int:billing_id>', methods=['GET'])
def generate_bill(billing_id):
    # Retrieve billing details based on billing_id (Assuming you have a Billing model)
    billing = BillingDetail.query.get_or_404(billing_id)

    # Pass billing details to the 'bill.html' template
    return render_template('bill.html', billing=billing)
# ... (previous imports)

@app.route('/book/<string:service_type>/<int:service_id>', methods=['GET', 'POST'])
@login_required
def book(service_type, service_id):
    if not isinstance(current_user, User):
        return 'You are not authorized to access this page.'

    service_types = {'bus': Bus, 'room': Room, 'package': Package}

    if service_type not in service_types:
        abort(404)  # Invalid service type

    service = service_types[service_type].query.get(service_id)
    print(service_id)
    if not service:
        abort(404)  # Service not found

    booking_date = datetime.now()
    total_price = calculate_total_price(service, service_type)

    # Apply fixed discount of 10%
    discount_amount = 0.1 * float(total_price)
    discounted_price = float(total_price) - discount_amount
    tax_amount = 0.07 * float(discounted_price)
    grand_total = float(discounted_price) + tax_amount
    print(service.ServiceProviderID)
    if request.method == 'POST':
        try:
            # Process the booking form data
            new_booking = Booking(
                UserID=current_user.UserID,
                ServiceProviderID=service.ServiceProviderID,
                BookingDate=booking_date,
                TotalPrice=total_price,
                BookingType=service_type,
                RoomID=service_id if service_type == 'room' else None,
                BusID=service_id if service_type == 'bus' else None,
                PackageID=service_id if service_type == 'package' else None
            )
            print(service.ServiceProviderID)
            db.session.add(new_booking)
            db.session.commit()

            new_billing = BillingDetail(
                UserID=current_user.UserID,
                BillingDate=booking_date,
                TotalAmount=total_price,
                DiscountAmount=discount_amount,
                TaxAmount=tax_amount,
                GrandTotal=grand_total
            )

            db.session.add(new_billing)
            db.session.commit()

            new_booking.BillingID = new_billing.BillingID
            db.session.commit()

            flash('Booking and Billing successful!')
            return redirect(url_for('user_home'))

        except Exception as e:
            db.session.rollback()  # Rollback changes in case of an exception
            flash(f'Error: {str(e)}', 'error')
            print(f"Error adding booking and billing: {str(e)}")

    return render_template('book.html', username=current_user.Username, service=service, service_type=service_type, total_price=total_price, discount_amount=discount_amount, discounted_price=discounted_price, tax_percent=7, tax_amount=tax_amount, grand_total=grand_total)

# ... (previous code)

def calculate_total_price(service, service_type):
    if service_type == 'room':
        return float(service.PricePerNight)
    else:
        return float(service.Price)


@app.route('/add_hotel', methods=['GET', 'POST'])
@login_required
def add_hotel():
    if isinstance(current_user, ServiceProvider):
        if request.method == 'POST':
            # Process form data
            hotel_name = request.form['hotel_name']
            location = request.form['location']
            description = request.form['description']
            image_url = request.form['image_url']  # Match the name to the form key

            # Create a new hotel instance
            new_hotel = Hotel(
                ServiceProviderID=current_user.ServiceProviderID,
                HotelName=hotel_name,
                Location=location,
                Description=description,
                Image=image_url
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
            image_url = request.form['image_url']  # Match the name to the form key
            room_type = request.form['room_type']

            # Create a new room instance
            new_room = Room(
                ServiceProviderID=current_user.ServiceProviderID,
                HotelID=hotel_id,
                RoomNumber=room_number,
                Capacity=capacity,
                PricePerNight=price_per_night,
                Image=image_url,
                RoomType=room_type
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
            print(request.form)
            bus_name = request.form['bus_name']
            departure_city = request.form['departure_city']
            arrival_city = request.form['arrival_city']
            departure_time_str = request.form['departure_time']
            arrival_time_str = request.form['arrival_time']
            price = request.form['price']

            # Extract image file from the request
            image_url = request.form['image_url']  # Match the name to the form key
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
                Image=image_url  # Change this to use the image URL

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
            image_url = request.form['image_url']  # Match the name to the form key

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
                Duration=duration,
                Image=image_url
            )
            print(Package.ServiceProviderID)
            # Add the new package to the database
            db.session.add(new_package)
            db.session.commit()

            flash('Package added successfully!', 'success')
            return redirect(url_for('provider_home'))

        return render_template('add_packages.html', username=current_user.Username)

    return 'You are not authorized to access this page.'

# Route for managing hotels, buses, and packages
# Add a new route to manage services
@app.route('/manage_services')
@login_required
def manage_services():
    if isinstance(current_user, ServiceProvider):
        # Fetch all services associated with the provider (hotels, buses, packages, rooms)
        hotels = Hotel.query.filter_by(ServiceProviderID=current_user.ServiceProviderID).all()
        buses = Bus.query.filter_by(ServiceProviderID=current_user.ServiceProviderID).all()
        packages = Package.query.filter_by(ServiceProviderID=current_user.ServiceProviderID).all()
        rooms = Room.query.join(Hotel).filter(Hotel.ServiceProviderID == current_user.ServiceProviderID).all()

        return render_template(
            'manage_services.html',
            username=current_user.Username,
            hotels=hotels,
            buses=buses,
            packages=packages,
            rooms=rooms
        )

    return 'You are not authorized to access this page.'


#update
# Add a new route to update an existing hotel
@app.route('/update_hotel/<int:hotel_id>', methods=['GET', 'POST'])
@login_required
def update_hotel(hotel_id):
    if isinstance(current_user, ServiceProvider):
        hotel = Hotel.query.get(hotel_id)

        if request.method == 'POST':
            # Process form data
            hotel.HotelName = request.form['hotel_name']
            hotel.Location = request.form['location']
            hotel.Description = request.form['description']

            # Update the hotel in the database
            db.session.commit()

            flash('Hotel updated successfully!')
            return redirect(url_for('provider_home'))

        return render_template('update_hotel.html', username=current_user.Username, hotel=hotel)

    return 'You are not authorized to access this page.'

# Add a new route to update an existing bus
@app.route('/update_bus/<int:bus_id>', methods=['GET', 'POST'])
@login_required
def update_bus(bus_id):
    if isinstance(current_user, ServiceProvider):
        bus = Bus.query.get(bus_id)

        if request.method == 'POST':
            # Process form data
            bus.BusName = request.form['bus_name']
            bus.DepartureCity = request.form['departure_city']
            bus.ArrivalCity = request.form['arrival_city']
            bus.DepartureTime = datetime.strptime(request.form['departure_time'], '%Y-%m-%dT%H:%M')
            bus.ArrivalTime = datetime.strptime(request.form['arrival_time'], '%Y-%m-%dT%H:%M')
            bus.Price = float(request.form['price'])
            bus.IsAvailable = bool(request.form.get('is_available'))

            # Update the bus in the database
            db.session.commit()

            flash('Bus updated successfully!')
            return redirect(url_for('provider_home'))

        return render_template('update_bus.html', username=current_user.Username, bus=bus)

    return 'You are not authorized to access this page.'

# Add a new route to update an existing package
@app.route('/update_package/<int:package_id>', methods=['GET', 'POST'])
@login_required
def update_package(package_id):
    if isinstance(current_user, ServiceProvider):
        package = Package.query.get(package_id)

        if request.method == 'POST':
            # Process form data
            package.PackageName = request.form['package_name']
            package.Description = request.form['description']
            package.Price = float(request.form['price'])
            package.Duration = int(request.form['duration'])

            # Update the package in the database
            db.session.commit()

            flash('Package updated successfully!')
            return redirect(url_for('provider_home'))

        return render_template('update_package.html', username=current_user.Username, package=package)

    return 'You are not authorized to access this page.'

@app.route('/delete_bus/<int:bus_id>')
@login_required
def delete_bus(bus_id):
    if isinstance(current_user, ServiceProvider):
        # Find the bus in the database
        bus = Bus.query.get(bus_id)

        if bus:
            # Perform the deletion logic (e.g., db.session.delete(bus))
            # Commit the changes to the database
            db.session.delete(bus)
            db.session.commit()

            # Redirect to the manage services page or home page
            flash('Bus deleted successfully!', 'success')
            return redirect(url_for('manage_services'))

        flash('Bus not found!', 'error')
        return redirect(url_for('manage_services'))

    return 'You are not authorized to access this page.'

@app.route('/delete_package/<int:package_id>')
@login_required
def delete_package(package_id):
    if isinstance(current_user, ServiceProvider):
        # Find the package in the database
        package = Package.query.get(package_id)

        if package:
            # Perform the deletion logic (e.g., db.session.delete(package))
            # Commit the changes to the database
            # Redirect to the manage services page or home page
            db.session.delete(package)
            db.session.commit()

            flash('Package deleted successfully!', 'success')
            return redirect(url_for('manage_services'))

        flash('Package not found!', 'error')
        return redirect(url_for('manage_services'))

    return 'You are not authorized to access this page.'
# Route for deleting a hotel
@app.route('/delete_hotel/<int:hotel_id>')
@login_required
def delete_hotel(hotel_id):
    if isinstance(current_user, ServiceProvider):
        # Find the hotel in the database
        hotel = Hotel.query.get(hotel_id)

        if hotel:
            # Perform the deletion logic (e.g., db.session.delete(hotel))
            # Commit the changes to the database
            db.session.delete(hotel)
            db.session.commit()

            # Redirect to the manage services page or home page
            flash('Hotel deleted successfully!', 'success')
            return redirect(url_for('manage_services'))

        flash('Hotel not found!', 'error')
        return redirect(url_for('manage_services'))

    return 'You are not authorized to access this page.'

# Route for deleting a room
@app.route('/delete_room/<int:room_id>')
@login_required
def delete_room(room_id):
    if isinstance(current_user, ServiceProvider):
        # Find the room in the database
        room = Room.query.get(room_id)

        if room:
            # Perform the deletion logic (e.g., db.session.delete(room))
            # Commit the changes to the database
            # Redirect to the manage services page or home page
            db.session.delete(room)
            db.session.commit()

            flash('Room deleted successfully!', 'success')
            return redirect(url_for('manage_services'))

        flash('Room not found!', 'error')
        return redirect(url_for('manage_services'))

    return 'You are not authorized to access this page.'
# Add a new route to update an existing room
@app.route('/update_room/<int:room_id>', methods=['GET', 'POST'])
@login_required
def update_room(room_id):
    if isinstance(current_user, ServiceProvider):
        room = Room.query.get(room_id)

        if request.method == 'POST':
            # Process form data
            room.RoomNumber = int(request.form['room_number'])
            room.Capacity = int(request.form['capacity'])
            room.PricePerNight = float(request.form['price_per_night'])
            room.Image = request.form['image']
            room.RoomType = request.form['room_type']
            room.IsAvailable = bool(request.form.get('is_available'))

            # Update the room in the database
            db.session.commit()

            flash('Room updated successfully!')
            return redirect(url_for('provider_home'))

        return render_template('update_room.html', username=current_user.Username, room=room)

    return 'You are not authorized to access this page.'


@app.route('/provider_dashboard')
@login_required
def provider_dashboard():
    if isinstance(current_user, ServiceProvider):
        # Retrieve all bookings and billings for the logged-in service provider
        bookings = Booking.query.filter_by(ServiceProviderID=current_user.ServiceProviderID).all()

        return render_template('provider_dashboard.html', username=current_user.Username, bookings=bookings)

    return 'You are not authorized to access this page.'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=3300)