from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017/")
db = client['projet_nosql_antoine']

queries_info = [
    {"collection": "products", "query": [{"$match": {"quantity_stock": {"$gt": 0}}}], "description": "Lister tous les produits disponibles en stock."},
    {"collection": "products", "query": [{"$match": {"category_id": "c100"}}], "description": "Trouver les produits d'une catégorie spécifique, par exemple, 'Electronics'."},
    {"collection": "reviews", "query": [{"$match": {"product_id": "p1003"}}, {"$group": {"_id": "$product_id", "averageRating": {"$avg": "$rating"}}}], "description": "Obtenir la moyenne des notes pour un produit spécifique."},
    {"collection": "orders", "query": [{"$match": {"user_id": "u1002"}}], "description": "Afficher les commandes passées par un utilisateur spécifique."},
    {"collection": "products", "query": [{"$match": {"quantity_stock": {"$lt": 10}}}], "description": "Rechercher les produits ayant un stock inférieur à un certain seuil, par exemple, 10."},
    {"collection": "users", "query": [{"$match": {"order_history": {"$size": 0}}}], "description": "Trouver les utilisateurs qui n'ont jamais passé de commande."},
    {"collection": "products", "query": [{"$lookup": {"from": "orders", "localField": "id_product", "foreignField": "products.id_product", "as": "orders"}}, {"$match": {"orders": {"$size": 0}}}], "description": "Lister les produits qui n'ont jamais été commandés."},
]

with open('results.txt', 'w', encoding='utf-8') as file:
    for query_info in queries_info:
        cursor = db[query_info['collection']].aggregate(query_info['query'])
        results = list(cursor)
        file.write(f"Problématique: {query_info['description']}\n")
        file.write(f"Résultats:\n{json.dumps(results, indent=4, default=str)}\n\n")

client.close()
