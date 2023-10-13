
from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask
from router import customer_router, vehicle_router, booking_router


app = Flask(__name__)

app.register_blueprint(customer_router, url_prefix='/api/customers')
app.register_blueprint(vehicle_router, url_prefix='/api/vehicles')
app.register_blueprint(booking_router, url_prefix='/api/booking')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=int(os.environ.get('APP_PORT')))