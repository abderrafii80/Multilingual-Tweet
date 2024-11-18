import requests
import json

# Remplacez par vos propres informations
ACCESS_TOKEN = "REPLACE_WITH_YOUR_ACCESS_TOKEN"
PAGE_ID = "REPLACE_WITH_PAGE_ID"  # Exemple : 'bbcnews' pour la page de BBC News
BASE_URL = f"https://graph.facebook.com/v16.0/{PAGE_ID}/posts"

# Fonction pour collecter des données
def fetch_facebook_posts():
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'id,message,created_time,story',
        'limit': 100  # Nombre maximum de publications à récupérer
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        print("Publications récupérées avec succès !")
        # Sauvegarde les données dans un fichier JSON
        with open("facebook_posts.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print("Données sauvegardées dans 'facebook_posts.json'.")
    else:
        print(f"Erreur : {response.status_code}")
        print(response.json())

# Exécuter la collecte
fetch_facebook_posts()
