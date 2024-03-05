from pymongo import MongoClient
import json

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['projet_nosql_antoine']

# Fonctions pour les différentes requêtes
def total_ventes_par_produit():
    return db.orders.aggregate([
        {"$unwind": "$products"},
        {"$group": {
            "_id": "$products.id_product",
            "totalSales": {"$sum": "$products.quantity"}
        }}
    ])

def produits_populaires():
    return db.orders.aggregate([
        {"$unwind": "$products"},
        {"$group": {
            "_id": "$products.id_product",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}}
    ])

def avis_avant_date(date_limite):
    return db.reviews.find({"review_date": {"$lt": date_limite}})

def compter_produits_par_categorie():
    return db.products.aggregate([
        {"$group": {
            "_id": "$category_id",
            "count": {"$sum": 1}
        }}
    ])

def utilisateurs_plus_actifs():
    return db.reviews.aggregate([
        {"$group": {
            "_id": "$user_id",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}},
        {"$limit": 1}
    ])

def commandes_total_sup(date_limite):
    return db.orders.find({"order_total": {"$gt": date_limite}})

def produits_recentement_ajoutes():
    return db.products.find().sort("date_added", -1).limit(5)

def categorie_prix_moyen_le_plus_eleve():
    return db.products.aggregate([
        {"$group": {
            "_id": "$category_id",
            "averagePrice": {"$avg": "$price"}
        }},
        {"$sort": {"averagePrice": -1}},
        {"$limit": 1}
    ])

# Liste des problématiques et des requêtes correspondantes
queries_info = [
    {"function": total_ventes_par_produit, "description": "Obtenir le total des ventes pour chaque produit"},
    {"function": produits_populaires, "description": "Identifier les produits les plus populaires basés sur le nombre de commandes"},
    {"function": lambda: avis_avant_date("2023-01-01"), "description": "Trouver les avis publiés avant une certaine date"},
    {"function": compter_produits_par_categorie, "description": "Compter le nombre de produits dans chaque catégorie"},
    {"function": utilisateurs_plus_actifs, "description": "Trouver les utilisateurs qui ont laissé le plus d'avis"},
    {"function": lambda: commandes_total_sup(500), "description": "Lister les commandes avec un total supérieur à un certain montant, par exemple, 500"},
    {"function": produits_recentement_ajoutes, "description": "Trouver les produits récemment ajoutés au catalogue"},
    {"function": categorie_prix_moyen_le_plus_eleve, "description": "Déterminer la catégorie avec le prix moyen le plus élevé"}
    # Ajoutez d'autres requêtes et descriptions comme nécessaire
]

# Exécuter les requêtes et écrire les résultats dans un fichier
with open('results.txt', 'w', encoding='utf-8') as file:
    for query_info in queries_info:
        results = query_info["function"]()
        file.write(f"Problématique: {query_info['description']}\n")
        file.write(f"Résultats:\n{json.dumps(list(results), indent=4, default=str)}\n\n")

# Fermer la connexion à la base de données
client.close()
