from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
from models import db, ParkingSpot, Allocation, User
import config
from datetime import datetime, date
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SESSION_TYPE'] = 'filesystem'

# Initialize extensions
Session(app)
db.init_app(app)

# Seed database
with app.app_context():
    db.create_all()
    if not ParkingSpot.query.first():
        for i in range(1, 11):
            db.session.add(ParkingSpot(spot_number=f"A{i:02}"))
    if not User.query.filter_by(username="admin").first():
        db.session.add(User(username="admin", password="1234"))
        db.session.add(User(username="staff", password="adminpass"))
    db.session.commit()

@app.route('/')
def home():
    spots = ParkingSpot.query.all()
    allocations = Allocation.query.all()
    return render_template('home.html', spots=spots, allocations=allocations)

@app.route('/allocate', methods=['GET', 'POST'])
def allocate():
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        vehicle_number = request.form['vehicle_number']
        owner_name = request.form['owner_name']
        phone_number = request.form['phone_number']
        spot = ParkingSpot.query.filter_by(is_available=True).first()
        if spot:
            spot.is_available = False
            allocation = Allocation(vehicle_number=vehicle_number, owner_name=owner_name,
                                    phone_number=phone_number, spot=spot)
            db.session.add(allocation)
            db.session.commit()
            return redirect('/')
        else:
            flash("No parking spots available", "danger")
            return redirect('/')
    return render_template('allocate.html')

@app.route('/release/<int:allocation_id>')
def release(allocation_id):
    if 'user' not in session:
        return redirect('/login')

    allocation = Allocation.query.get(allocation_id)
    if allocation:
        allocation.spot.is_available = True
        checkin_time = allocation.allocated_at
        checkout_time = datetime.utcnow()

        total_minutes = int((checkout_time - checkin_time).total_seconds() // 60)
        chargeable_minutes = max(0, total_minutes - 30)
        extra_blocks = (chargeable_minutes + 9) // 10
        bill = extra_blocks * 2

        db.session.delete(allocation)
        db.session.commit()

        return render_template("bill.html", vehicle_number=allocation.vehicle_number,
                               spot=allocation.spot.spot_number,
                               owner_name=allocation.owner_name,
                               phone_number=allocation.phone_number,
                               checkin=checkin_time.strftime('%Y-%m-%d %H:%M:%S'),
                               checkout=checkout_time.strftime('%Y-%m-%d %H:%M:%S'),
                               total_minutes=total_minutes,
                               bill=bill)
    return redirect('/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user:
            session['user'] = user.username
            return redirect('/')
        else:
            flash("Invalid credentials", "danger")
            return redirect('/login')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session or session['user'] != 'admin':
        return redirect('/')

    today = date.today()
    earnings_data = db.session.query(
        func.sum(((func.strftime('%s','now') - func.strftime('%s', Allocation.allocated_at)) / 60 - 30) / 10 * 2)
    ).filter(Allocation.allocated_at >= today).scalar()

    earnings = int(earnings_data) if earnings_data else 0

    return render_template("dashboard.html", earnings=earnings, date=today.strftime('%Y-%m-%d'))

if __name__ == '__main__':
    app.run(debug=True)
