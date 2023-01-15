from flask import Flask, request, render_template, jsonify, url_for, make_response
from dotenv import load_dotenv
from endpoints import endpoints_blueprint
import os, requests 

application = Flask(__name__)


load_dotenv()
application.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY")
application.register_blueprint(endpoints_blueprint)


if __name__ == "__main__":
   #application.run(host='0.0.0.0', debug=True, port=6543)
   application.run(host='0.0.0.0', debug=True)
   #application.run(host='0.0.0.0')







