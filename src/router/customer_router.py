from database import db_manager as db
from flask import Blueprint, request, jsonify



customer_router = Blueprint('customer_router', __name__)

@customer_router.route('/', methods=['GET'])
def get_customers():
    query = "SELECT customer_id, email, name, phone_number FROM CUSTOMER"


    
    customers = db.fetch_all(query)
    if customers:
        customer_list = []
        for customer in customers:
            customer_list.append({
            "customer_id": customer[0],
            "email": customer[1],
            "name": customer[2],
            "phone_number": customer[3]
            })

        return jsonify({"customers": customer_list})
    else:
        return jsonify({"error": f"Failed to retrieve customers"}), 422



@customer_router.route('/', methods=['POST'])
def create_customer():
    
    data = request.json
    required_keys = ['name', 'phone_number', 'email']
    
    if all(key not in data for key in required_keys):
        return jsonify({"error": "Name, phone number, and email are required"}), 400
    
    name, phone_number, email = data['name'], data['phone_number'], data['email']
    
    query = "INSERT INTO CUSTOMER (name, phone_number, email) VALUES (%s, %s, %s)"
    values = (name, phone_number, email)
    
    success, message = db.execute_query(query, values, return_last_row_id=True)

    if success:
        return jsonify({"message": f"Customer added successfully with values {values} with ID: {message}"}), 201
    else:
        if "Duplicate entry error" in message:
            return jsonify({"error": message}), 400
        else:
            return jsonify({"error": "Failed to add customer"}), 500


@customer_router.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    query = "SELECT * FROM CUSTOMER WHERE customer_id = %s"
    values = (customer_id,)

    
    customer = db.fetch_one(query, values)
    
    if customer:
        customer_data = {
            "id": customer[0],
            "name": customer[1],
            "phone_number": customer[2],
            "email": customer[3]
        }
        return jsonify(customer_data)
    else:
        return jsonify({"error": f"Failed to retrieve customer with id {customer_id}"}), 404


@customer_router.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.json
    name, email, phone_number = data.get('name'), data.get('email'), data.get('phone_number')

    if not any([name, email, phone_number]):
        return jsonify({"error": "No valid data provided for update"}), 400

    query = "UPDATE CUSTOMER SET"
    values = []

    if name:
        query += " name = %s, "
        values.append(name)
    if phone_number:
        query += " phone_number = %s, "
        values.append(phone_number)
    if email:
        query += " email = %s, "
        values.append(email)

    query = query.rstrip(', ') + " WHERE customer_id = %s"
    values.append(customer_id)

    success, result = db.execute_query(query, tuple(values))

    if success:
        return jsonify({"message": f"Customer updated successfully with {tuple(values)}"}), 201
    else:
        return jsonify({"error": result}), 422
    
@customer_router.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    query = "DELETE FROM CUSTOMER WHERE customer_id = %s"
    values = (customer_id,)

    success, result = db.execute_query(query, values)

    if success:
        return jsonify({"message": f"Customer with id {customer_id} deleted successfully"}), 200
    else:
        return jsonify({"error": result}), 422
