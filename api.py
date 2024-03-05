from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client['projet_nosql_antoine']

@app.route('/products', methods=['GET'])
def get_products():
    products = db.products.find({})
    result = [{item: product[item] for item in product if item != '_id'} for product in products]
    return jsonify(result)

@app.route('/products', methods=['POST'])
def add_product():
    product = request.json
    db.products.insert_one(product)
    return jsonify({'msg': 'Product added successfully'}), 201

@app.route('/products/<id>', methods=['PUT'])
def update_product(id):
    updates = request.json
    db.products.update_one({'_id': ObjectId(id)}, {'$set': updates})
    return jsonify({'msg': 'Product updated successfully'})

@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    db.products.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': 'Product deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
    
#http://localhost:5000/products