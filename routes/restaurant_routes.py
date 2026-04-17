

from flask import Blueprint, request, jsonify
from models import db, Restaurant

restaurant_bp = Blueprint('restaurant', __name__)

@restaurant_bp.route('/', methods=['GET'])
def get_all():
    restaurants = Restaurant.query.all()
    return jsonify([{'id': r.id, 'name': r.name, 'address': r.address} for r in restaurants])

@restaurant_bp.route('/search', methods=['GET'])
def search():
    name = request.args.get('name')
    restaurants = Restaurant.query.filter(Restaurant.name.contains(name)).all()
    return jsonify([{'id': r.id, 'name': r.name} for r in restaurants])

@restaurant_bp.route('/', methods=['POST'])
def create():
    data = request.json
    r = Restaurant(name=data['name'], address=data['address'])
    db.session.add(r)
    db.session.commit()
    return jsonify({'message': 'Created'}), 201

@restaurant_bp.route('/<int:id>', methods=['PUT'])
def update(id):
    r = Restaurant.query.get_or_404(id)
    data = request.json
    r.name = data['name']
    r.address = data['address']
    db.session.commit()
    return jsonify({'message': 'Updated'})

@restaurant_bp.route('/<int:id>', methods=['DELETE'])
def delete(id):
    r = Restaurant.query.get_or_404(id)
    db.session.delete(r)
    db.session.commit()
    return jsonify({'message': 'Deleted'})
