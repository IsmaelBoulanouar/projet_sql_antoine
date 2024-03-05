from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client['projet_nosql']

@app.route('/products', methods=['GET'])
def get_products():
    products = db.products.find({})
    result = [{item: product[item] for item in product if item != '_id'} for product in products]
    return jsonify(result)

@app.route('/products/<id>', methods=['GET'])
def get_product_by_id(id):
    product = db.products.find_one({'_id': ObjectId(id)})
    if product:
        result = {item: product[item] for item in product if item != '_id'}
        return jsonify(result)
    else:
        return jsonify({'error': 'Product not found'}), 404
    
@app.route('/users/never_ordered', methods=['GET'])
def users_never_ordered():
    pipeline = [
        {
            "$lookup": {
                "from": "orders",
                "localField": "_id",
                "foreignField": "user_id",
                "as": "orders"
            }
        },
        {
            "$match": {
                "orders": { "$size": 0 }
            }
        },
        {
            "$project": {
                "orders": 0  # Exclure le champ orders du résultat
            }
        }
    ]
    users = db.users.aggregate(pipeline)
    result = list(users)
    return jsonify(result)

    
@app.route('/products/count_by_category', methods=['GET'])
def count_products_by_category():
    pipeline = [
        {"$group": {"_id": "$category_id", "count": {"$sum": 1}}}
    ]
    results = db.products.aggregate(pipeline)
    count_by_category = [{item['_id']: item['count']} for item in results]
    return jsonify(count_by_category)

@app.route('/products/in_stock', methods=['GET'])
def get_products_in_stock():
    products_in_stock = db.products.find({"quantity_stock": {"$gt": 0}})
    result = [{item: product[item] for item in product if item != '_id'} for product in products_in_stock]
    return jsonify(result)


@app.route('/search', methods=['GET'])
def search_products():
    query = request.args.get('query', '')
    products = db.products.find({
        "$or": [
            {"name": {"$regex": query, "$options": "i"}},
            {"description": {"$regex": query, "$options": "i"}}
        ]
    })
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
    
#http://localhost:5000/products Affiche tous les produits
#http://localhost:5000/search?query=stream    Affiche les produits par descriptions
#http://localhost:5000/products/65e4b177757444150e6fbfb5      Affiche les produits par id
#http://localhost:5000/products/in_stock      Affiche le stocke des produits

