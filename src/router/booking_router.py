from database import db_manager as db
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta


booking_router = Blueprint('booking_router', __name__)


@booking_router.route('/<int:booking_id>', methods=['GET'])
def get_booking_info(booking_id):

    query = "SELECT * FROM BOOKING WHERE booking_id = %s"
    values = (booking_id,)
    booking = db.fetch_one(query, values)
    
    if booking:
        return jsonify({
            "booking_id": booking[0],
            "customer_id": booking[1],
            "vehicle_id": booking[2],
            "date_of_hire": booking[3],
            "date_of_return": booking[4]
        })
    else:
        return jsonify({"error": f"Booking with id {booking_id} not found"}), 404

@booking_router.route('/daily_report', methods=['GET'])
def daily_report():
    current_date = datetime.now().date()
    bookings = db.fetch_all("SELECT customer_id, vehicle_id, date_of_hire, date_of_return FROM BOOKING WHERE date_of_hire <= %s AND date_of_return >= %s", (current_date, current_date))

    if not bookings:
        return jsonify({"message": "No bookings for today."}), 200

    report = []
    for booking in bookings:
        report.append({
            "customer_id": booking[0],
            "vehicle_id": booking[1],
            "date_of_hire": booking[2].strftime("%Y-%m-%d"),
            "date_of_return": booking[3].strftime("%Y-%m-%d")
        })

    return jsonify({"report": report}), 200

@booking_router.route('/', methods=['POST'])
def create_booking():
    data = request.json

    # check of correct values exist
    required_keys = ['customer_id', 'vehicle_id', 'date_of_hire', 'date_of_return']
    if any(key not in data for key in required_keys):
        return jsonify({"error": "Invalid request. Please provide customer_id, vehicle_id, date_of_hire, and date_of_return."}), 400
    
    customer_id = data['customer_id']
    vehicle_id = data['vehicle_id']
    date_of_hire = datetime.strptime(data['date_of_hire'], "%Y-%m-%d")
    date_of_return = datetime.strptime(data['date_of_return'], "%Y-%m-%d")

    # calculate booking duration
    duration = (date_of_return - date_of_hire).days
    if duration > 7:
        return jsonify({"error": "Booking duration exceeds the maximum allowed limit of 7 days"}), 400

    customer = db.fetch_one("SELECT name, email FROM CUSTOMER WHERE customer_id = %s", (customer_id,))
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    # Check if the booking is made within the allowed advance booking window (7 days)
    current_date = datetime.now()
    advance_booking_limit = current_date + timedelta(days=7)

    if date_of_hire > advance_booking_limit:
        return jsonify({"error": "Booking made too far in advance. You can book up to 7 days in advance."}), 400
    # check if vehicle is available for given date
    existing_booking =  db.fetch_one("SELECT booking_id FROM BOOKING WHERE vehicle_id = %s AND date_of_return < %s", (vehicle_id, date_of_hire))

    # create a booking if the existing booking doesn't exist
    if not existing_booking:


        _, booking_id  = db.execute_query("INSERT INTO BOOKING (customer_id, vehicle_id, date_of_hire, date_of_return) VALUES (%s, %s, %s, %s)", (customer_id, vehicle_id, date_of_hire, date_of_return), True)


        total_amount = 50 * duration

        db.execute_query("INSERT INTO INVOICE (booking_id, customer_id, invoice_date, total_amount, payment_status) VALUES (%s, %s, %s, %s, 'Paid')", (booking_id, customer_id, date_of_hire, total_amount))



        # Send confirmation letter (simplified as a print statement)
        print(f"Confirmation letter sent to {customer[1]}")

        return jsonify({"message": "Booking created successfully", "booking_id": booking_id}), 201
    else:
        return jsonify({"error": "Vehicle not available for booking within the 7-day advance booking window"}), 400
