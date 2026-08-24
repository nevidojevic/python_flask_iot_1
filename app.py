from flask import Flask, jsonify, request
from database import db, User, IoTDevice

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smarthome.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


# GET: Dobavljanje svih IoT uredjaja
@app.route('/api/devices', methods=['GET'])
def get_devices():
    devices = IoTDevice.query.all()
    return jsonify([d.to_dict() for d in devices]), 200


#  GET sa parametrima: Pretraga uredjaja po tipu
@app.route('/api/devices/search', methods=['GET'])
def search_devices_by_type():
    dev_type = request.args.get('type')
    if not dev_type:
        return jsonify({"error": "Parametar 'type' je obavezan"}), 400

    devices = IoTDevice.query.filter_by(device_type=dev_type).all()
    return jsonify([d.to_dict() for d in devices]), 200


#3. POST: Registracija novog IoT uredjaja
@app.route('/api/devices', methods=['POST'])
def add_device():
    data = request.get_json()
    if not data or 'name' not in data or 'device_type' not in data:
        return jsonify({"error": "Nedostaju obavezni podaci (name, device_type)"}), 400

    new_device = IoTDevice(
        name=data['name'],
        device_type=data['device_type'],
        status=data.get('status', 'off'),
        value=data.get('value', 0.0)
    )
    db.session.add(new_device)
    db.session.commit()
    return jsonify(new_device.to_dict()), 201


#4. PUT: Ažuriranje stanja uredjaja
@app.route('/api/devices/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    device = IoTDevice.query.get_or_404(device_id)
    data = request.get_json()

    device.name = data.get('name', device.name)
    device.status = data.get('status', device.status)
    device.value = data.get('value', device.value)

    db.session.commit()
    return jsonify(device.to_dict()), 200


#5. DELETE:BrisanjeIoT uredjaja
@app.route('/api/devices/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    device = IoTDevice.query.get_or_404(device_id)
    db.session.delete(device)
    db.session.commit()
    return jsonify({"message": f"Uređaj sa ID-jem {device_id} je uspešno obrisan."}), 200


# 6. POST Kreiranje korisničkog profila
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({"error": "Nedostaju podaci za korisnika (username, email)"}), 400

    if User.query.filter_by(username=data['username']).first():
        jsonify({"error": "Korisničko ime već postoji"}), 400

    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201


if __name__ == '__main__':
    app.run(debug=True)