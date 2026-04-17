
from flask import Blueprint, request, jsonify
from models import db, Order

order_bp = Blueprint('order', __name__)

@order_bp.route('/', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([{'id': o.id, 'product_id': o.product_id, 'quantity': o.quantity} for o in orders])

@order_bp.route('/', methods=['POST'])
def create_order():
    data = request.json
    o = Order(product_id=data['product_id'], quantity=data['quantity'])
    db.session.add(o)
    db.session.commit()
    return jsonify({'message': 'Order created'}), 201

@order_bp.route('/<int:id>', methods=['PUT'])
def update_order(id):
    o = Order.query.get_or_404(id)
    data = request.json
    o.quantity = data['quantity']
    db.session.commit()
    return jsonify({'message': 'Updated'})

@order_bp.route('/<int:id>', methods=['DELETE'])
def delete_order(id):
    o = Order.query.get_or_404(id)
    db.session.delete(o)
    db.session.commit()
    return jsonify({'message': 'Deleted'})
