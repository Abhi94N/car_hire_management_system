
from dotenv import load_dotenv
load_dotenv()
import os
from flask import Flask
from router import customer_router


app = Flask(__name__)

app.register_blueprint(customer_router)







if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=int(os.environ.get('APP_PORT')))