from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['projet_nosql_antoine']  # Remplacez par le nom de votre base de données

# Endpoint pour obtenir tous les produits
@app.route('/products', methods=['GET'])
def get_products():
    products = db.products.find({})
    result = [{item: product[item] for item in product if item != '_id'} for product in products]
    return jsonify(result)

# Endpoint pour ajouter un produit
@app.route('/products', methods=['POST'])
def add_product():
    product = request.json
    db.products.insert_one(product)
    return jsonify({'msg': 'Product added successfully'}), 201

# Endpoint pour mettre à jour un produit
@app.route('/products/<id>', methods=['PUT'])
def update_product(id):
    updates = request.json
    db.products.update_one({'_id': ObjectId(id)}, {'$set': updates})
    return jsonify({'msg': 'Product updated successfully'})

# Endpoint pour supprimer un produit
@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    db.products.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': 'Product deleted successfully'})

# Exécuter l'application
if __name__ == '__main__':
    app.run(debug=True)
    
#http://localhost:5000/products