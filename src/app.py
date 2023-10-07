from flask import Flask, request, jsonify
import mysql.connector
from dotenv import load_dotenv
import os 

load_dotenv()
app = Flask(__name__)

   


def create_db_connection():
    mysql_config = {
    'host': os.environ.get('MYSQL_HOST'),
    'user': os.environ.get('MYSQL_USER'),
    'port': os.environ.get('MYSQL_PORT'),
    'password':  os.environ.get('MYSQL_PASSWORD'),
    'database':  os.environ.get('MYSQL_DB'),
    }

    try:
        conn = mysql.connector.connect(**mysql_config)

        print("MySQL connection successful!")
        return conn 

    except mysql.connector.Error as err:

        print(f"MySQL connection error: {err}")

@app.route('/customers', methods=['POST'])
def create_customer():
    
    data = request.json
    if all(key not in data for key in ['name', 'phone_number', 'email']):
        return jsonify({"error": "Name, phone number, and email are required"}), 400

    name = data.get('name')
    phone_number = data.get('phone_number')
    email = data.get('email')
    
    conn = create_db_connection()
    
    if conn is not None:
        
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO CUSTOMER (name, phone_number, email) VALUES (%s, %s, %s)", (name, phone_number, email))
            lastrowid = cursor.lastrowid
            conn.commit()

            cursor.close()
            conn.close()     
        except mysql.connector.Error as e:
            conn.rollback()
            return jsonify({"error": e.msg})
            
        return jsonify({"message": f"Customer added successfully with values {name, phone_number, email} with ID: {lastrowid}"}), 201
    return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):

    conn = create_db_connection()
    
    if conn is not None:
        try:
            cursor = conn.cursor() 
            cursor.execute("SELECT * FROM CUSTOMER WHERE customer_id = %s", (customer_id,))
            customer = cursor.fetchone()
            cursor.close()
            conn.close()     
            if customer:
                customer_data = {
                    "id": customer[0],
                    "name": customer[1],
                    "phone_number": customer[2],
                    "email": customer[3]
                }
                return jsonify(customer_data)
        except Exception as e:
            print(e.msg)
            return jsonify({"error": f"Failed to retrieve customer with id {customer_id}"}), 404

    return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    
    if name is None and email is None and phone_number is None: 
        return jsonify({"error": "No valid data provided for update"}), 400


    query = "UPDATE CUSTOMER SET"
    values = []
    
    if name is not None:
        query += " name = %s, "
        values.append(name)
    if phone_number is not None:
        query += " phone_number = %s, "
        values.append(phone_number)
    if email is not None:
        query += " email = %s, "
        values.append(email)
    
    # remove trailing whitespace and comma
    query = query.rstrip().rstrip(',') 
    
    query += " WHERE customer_id = %s"
    values.append(customer_id)


    conn = create_db_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute(query, tuple(values))
            conn.commit()
            cursor.close()
            conn.close()  
            return jsonify({"message": f"Customer updated successfully with {tuple(values)}"}), 201
        except Exception as e:
            print(e.msg)
            return jsonify({"error": f"Failed to update customer with {tuple(values)}"}), 422
    return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    
    conn = create_db_connection()
    
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM CUSTOMER WHERE customer_id = %s", (customer_id,))
            conn.commit()
            cursor.close()
            conn.close()  
            return jsonify({"message": f"Customer with id {customer_id} deleted successfully"})
        except Exception as e:
            return jsonify({"error": f"Failed to delete customer with id {customer_id}"}), 422
    return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=int(os.environ.get('APP_PORT')))