from flask import Blueprint, request, jsonify
from models import db, Product

product_bp = Blueprint('product', __name__)


@product_bp.route('/', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    return jsonify([
        {
            'id': p.id,
            'name': p.name,
            'price': p.price
        } for p in products
    ])


@product_bp.route('/search', methods=['GET'])
def search_products():
    name = request.args.get('name')

    if not name:
        return jsonify([])

    products = Product.query.filter(Product.name.contains(name)).all()

    return jsonify([
        {
            'id': p.id,
            'name': p.name,
            'price': p.price
        } for p in products
    ])


@product_bp.route('/', methods=['POST'])
def create_product():
    data = request.json

    if not data or not data.get('name') or not data.get('price'):
        return jsonify({'error': 'Name and price are required'}), 400

    p = Product(
        name=data['name'],
        price=data['price']
    )

    db.session.add(p)
    db.session.commit()

    return jsonify({'message': 'Product created'}), 201


@product_bp.route('/<int:id>', methods=['PUT'])
def update_product(id):
    p = Product.query.get_or_404(id)
    data = request.json

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    p.name = data.get('name', p.name)
    p.price = data.get('price', p.price)

    db.session.commit()

    return jsonify({'message': 'Updated'})

@product_bp.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    p = Product.query.get_or_404(id)

    db.session.delete(p)
    db.session.commit()

    return jsonify({'message': 'Deleted'})