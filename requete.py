# We will now rewrite the code to include all 15 problem statements and queries, and save them to a text file.

# Define all 15 problem statements and corresponding queries
problems_and_queries = [
    {"problem": "Obtenir tous les produits disponibles dans une catégorie spécifique", "query": "db.products.find({'category_id': '<category_id>'})"},
    {"problem": "Trouver les produits en dessous d'un certain prix", "query": "db.products.find({'price': {'$lt': <max_price>}})"},
    {"problem": "Identifier les produits les plus stockés", "query": "db.products.find({}).sort({'quantity_stock': -1})"},
    {"problem": "Trouver les produits ajoutés récemment au catalogue", "query": "db.products.find({}).sort({'date_added': -1})"},
    {"problem": "Sélectionner les produits les mieux notés", "query": "db.reviews.aggregate([{'$group': {'_id': '$product_id', 'average_rating': {'$avg': '$rating'}}}, {'$match': {'average_rating': {'$gt': <rating_threshold>}}}])"},
    {"problem": "Déterminer quels utilisateurs ont passé le plus de commandes", "query": "db.orders.aggregate([{'$group': {'_id': '$user_id', 'total_orders': {'$sum': 1}}}, {'$sort': {'total_orders': -1}}])"},
    {"problem": "Calculer le revenu total généré par catégorie de produit", "query": "db.orders.aggregate([{'$unwind': '$products'}, {'$lookup': {'from': 'products', 'localField': 'products.id_product', 'foreignField': 'id_product', 'as': 'product_info'}}, {'$group': {'_id': '$product_info.category_id', 'total_sales': {'$sum': {'$multiply': ['$products.quantity', '$product_info.price']}}}}])"},
    {"problem": "Identifier les produits qui n'ont jamais été commandés", "query": "db.products.find({'_id': {'$nin': db.orders.distinct('products.id_product')}})"},
    {"problem": "Calculer la critique moyenne des produits d'une catégorie spécifique", "query": "db.reviews.aggregate([{'$lookup': {'from': 'products', 'localField': 'product_id', 'foreignField': 'id_product', 'as': 'product_info'}}, {'$match': {'product_info.category_id': '<category_id>'}}, {'$group': {'_id': '$product_id', 'average_review': {'$avg': '$rating'}}}])"},
    {"problem": "Trouver le produit le moins cher dans chaque catégorie", "query": "db.products.aggregate([{'$group': {'_id': '$category_id', 'cheapest_product': {'$min': '$price'}}}])"},
    {"problem": "Identifier les clients n'ayant pas passé de commande depuis plus d'un an", "query": "db.users.find({'_id': {'$nin': db.orders.find({'order_date': {'$gte': new Date((new Date()).getTime() - (365 * 24 * 60 * 60 * 1000))}}).distinct('user_id')}})"},
    {"problem": "Trouver les produits avec une quantité de stock inférieure à un seuil spécifique", "query": "db.products.find({'quantity_stock': {'$lt': <threshold>}})"},
    {"problem": "Compter le nombre total de produits différents vendus", "query": "db.orders.aggregate([{'$unwind': '$products'}, {'$group': {'_id': '$products.id_product'}}, {'$count': 'distinct_products_sold'}])"},
    {"problem": "Identifier la commande la plus chère passée", "query": "db.orders.find({}).sort({'order_total': -1}).limit(1)"},
    {"problem": "Obtenir les avis des utilisateurs sur un produit spécifique", "query": "db.reviews.find({'product_id': '<product_id>'})"}
]

# Write the content to a text file
file_path = '/mnt/data/problems_and_queries.txt'
with open(file_path, 'w') as file:
    for item in problems_and_queries:
        file.write(f"Problématique: {item['problem']}\nRequête: {item['query']}\n\n")

file_path
