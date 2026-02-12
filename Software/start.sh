#!/bin/bash

cd flask_server

python3 -m venv venv
source venv/bin/activate

# Install packages if needed
pip install Flask-SQLAlchemy
#pip3 install flask

# Run app
flask --app app_server run --host=0.0.0.0 --port=5000

# Stop working
#deactivate
#flask --app app_server run --host=0.0.0.0 --port=5000