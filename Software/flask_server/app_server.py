from flask import Flask, request, jsonify, render_template # import the Flask class
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__) # this is an instance of the class.
# _name__ is a convenient shortcut for this that is appropriate for most cases.
# This is needed so that Flask knows where to look for resources such as templates and static files.


# we need to save sensor data in a database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    light_ambient = db.Column(db.Float)
    light_lux = db.Column(db.Float)
    timestamp = db.Column(db.DateTime,  default=lambda: datetime.now(timezone.utc))


# Create table
with app.app_context():
    db.create_all()


@app.route('/uploads', methods=['POST'])
def receive_upload():
    print("Uploads endpoint hit")
    #print("Headers:", dict(request.headers))
    #print("Raw body:", request.get_data())

    data = request.get_json(silent=True)
    #print("Parsed JSON:", data)

    if data:
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        light_ambient = data.get('light_ambient')
        light_lux = data.get('light_lux')


        reading = SensorData(temperature=temperature, humidity=humidity, 
                             light_ambient=light_ambient, light_lux = light_lux)
        db.session.add(reading)
        db.session.commit()


        print(f"Received temperature: {temperature}, humidity: {humidity}, light_ambient: {light_ambient}, light_lux: {light_lux}")
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "reason": "no or invalid JSON"}), 400


@app.route('/') # homepage declares raw data
def raw_data():
    """Display all sensor readings in a table"""
    readings = SensorData.query.order_by(SensorData.timestamp.desc()).limit(1000).all()
    return render_template('raw_data.html', readings=readings)

if __name__ == '__main__':
    app.run(host='192.168.1.66', port=5000, debug=True)