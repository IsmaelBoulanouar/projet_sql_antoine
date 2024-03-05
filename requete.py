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
    {"collection": "orders", "query": [{"$unwind": "$products"}, {"$group": {"_id": "$products.id_product", "totalSales": {"$sum": "$products.quantity"}}}], "description": "Obtenir le total des ventes pour chaque produit."},
    {"collection": "orders", "query": [{"$unwind": "$products"}, {"$group": {"_id": "$products.id_product", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}], "description": "Identifier les produits les plus populaires basés sur le nombre de commandes."},
    {"collection": "reviews", "query": [{"$match": {"review_date": {"$lt": "2023-01-01"}}}], "description": "Trouver les avis publiés avant une certaine date."},
    {"collection": "products", "query": [{"$group": {"_id": "$category_id", "count": {"$sum": 1}}}], "description": "Compter le nombre de produits dans chaque catégorie."},
    {"collection": "reviews", "query": [{"$group": {"_id": "$user_id", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}, {"$limit": 1}], "description": "Trouver les utilisateurs qui ont laissé le plus d'avis."},
    {"collection": "orders", "query": [{"$match": {"order_total": {"$gt": 500}}}], "description": "Lister les commandes avec un total supérieur à un certain montant, par exemple, 500."},
    {"collection": "products", "query": [{"$sort": {"date_added": -1}}, {"$limit": 5}], "description": "Trouver les produits récemment ajoutés au catalogue."},
    {"collection": "products", "query": [{"$group": {"_id": "$category_id", "averagePrice": {"$avg": "$price"}}}, {"$sort": {"averagePrice": -1}}, {"$limit": 1}], "description": "Déterminer la catégorie avec le prix moyen le plus élevé."}
]

with open('results.txt', 'w', encoding='utf-8') as file:
    for query_info in queries_info:
        cursor = db[query_info['collection']].aggregate(query_info['query'])
        results = list(cursor)
        file.write(f"Problématique: {query_info['description']}\n")
        file.write(f"Résultats:\n{json.dumps(results, indent=4, default=str)}\n\n")

client.close()
