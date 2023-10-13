from database import db_manager as db
from flask import Blueprint, request, jsonify



vehicle_router = Blueprint('vehicle_router', __name__)

@vehicle_router.route('/', methods=['GET'])
def get_vehicles():
    query = "SELECT vehicle_id, make, model, seats, category, year, registration_number FROM VEHICLE"
    vehicles = db.fetch_all(query)
    if vehicles:
        print(vehicles)
        return jsonify({"vehicles": vehicles})
    else:
        return jsonify({"error": f"Failed to retrieve vehicles"}), 422

@vehicle_router.route('/<int:vehicle_id>', methods=['GET'])
def get_vehicle(vehicle_id):
    query = "SELECT * FROM VEHICLE WHERE vehicle_id = %s"
    values = (vehicle_id,)

    
    vehicle = db.fetch_one(query, values)
    print(vehicle)
    
    if vehicle:
        vehicle_data = {
            "vehicle_id": vehicle[0],
            "make": vehicle[1],
            "model": vehicle[2],
            "seats": vehicle[3],
            "category": vehicle[4],
            "year": vehicle[5],
            "registration_number": vehicle[6]
        }
        return jsonify(vehicle_data)
    else:
        return jsonify({"error": f"Failed to retrieve vehicle with id {vehicle_id}"}), 404
    
@vehicle_router.route('/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    data = request.json
    make, model, seats, category, year, registration_number = data.get('make'), data.get('model'), data.get('seats'), data.get('category'), data.get('year'), data.get('registration_number') 

    if not any([make, model, seats, category, year, registration_number]):
        return jsonify({"error": "No valid data provided for update"}), 400

    query = "UPDATE VEHICLE SET"
    values = []

    if make:
        query += " make = %s, "
        values.append(make)
    if model:
        query += " model = %s, "
        values.append(model)
    if seats:
        query += " seats = %s, "
        values.append(seats)
    if seats:
        query += " category = %s, "
        values.append(category)
    if year:
        query += " year = %s, "
        values.append(year)
    if registration_number:
        query += " registration_number = %s, "
        values.append(registration_number)
    query = query.rstrip(', ') + " WHERE vehicle_id = %s"
    values.append(vehicle_id)

    success, result = db.execute_query(query, tuple(values))

    if success:
        return jsonify({"message": f"Vehicle updated successfully with {tuple(values)}"}), 201
    else:
        return jsonify({"error": result}), 422

@vehicle_router.route('/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    query = "DELETE FROM VEHICLE WHERE vehicle_id = %s"
    values = (vehicle_id,)

    success, result = db.execute_query(query, values)

    if success:
        return jsonify({"message": f"Vehicle with id {vehicle_id} deleted successfully"}), 200
    else:
        return jsonify({"error": result}), 422


@vehicle_router.route('/', methods=['POST'])
def create_vehicle():
    
    data = request.json
    required_keys = ['make', 'model', 'seats', 'category', 'year', 'registration_number']
    
    if all(key not in data for key in required_keys):
        return jsonify({"error": "make, model, seats, category, year, and registration_number are required"}), 400
    
    make, model, seats, category, year, registration_number = data.get('make'), data.get('model'), data.get('seats'), data.get('category'), data.get('year'), data.get('registration_number') 
    
    query = "INSERT INTO VEHICLE (make, model, seats, category, year, registration_number) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (make, model, seats, category, year, registration_number)
    
    success, message = db.execute_query(query, values, return_last_row_id=True)

    if success:
        return jsonify({"message": f"Vehicle added successfully with values {values} with ID: {message}"}), 201
    else:
        if "Duplicate entry error" in message:
            return jsonify({"error": message}), 400
        else:
            return jsonify({"error": "Failed to add vehicle"}), 500