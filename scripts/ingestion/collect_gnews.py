from serpapi import GoogleSearch
import json
import os

def get_google_news(query, language, location, num_requests=5, articles_per_request=100):
    """
    Collecte des articles Google News pour une requête donnée avec pagination.
    
    :param query: Mot-clé de recherche.
    :param language: Langue pour les résultats ('ar', 'fr', 'en', etc.).
    :param location: Code de localisation (par exemple, 'ma' pour le Maroc, 'us' pour les États-Unis).
    :param num_requests: Nombre de requêtes à faire (par défaut 5).
    :param articles_per_request: Nombre d'articles par requête (par défaut 100).
    :return: Liste des articles collectés.
    """
    all_articles = []
    for i in range(num_requests):
        params = {
            "engine": "google_news",
            "q": query,
            "hl": language,
            "gl": location,
            "api_key": "d5d3c22a44c999cd9caea78296d85f3e53965db5ce5c3e61b6ed633a68f61789",  #
            "start": i * articles_per_request  # Pagination : start = 0, 100, 200, etc.
        }

        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            all_articles.extend(results.get("news_results", []))
        except Exception as e:
            print(f"Erreur lors de la collecte pour '{query}' (requête {i + 1}) : {e}")

    return all_articles

def save_to_json(data, filepath):
    """
    Sauvegarde les données dans un fichier JSON.
    
    :param data: Données à sauvegarder.
    :param filepath: Chemin du fichier où sauvegarder les données.
    """
    # Si le fichier existe déjà, on ouvre le fichier pour ajouter les données
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []

    # Ajouter les nouveaux articles aux anciens
    existing_data.extend(data)

    # Sauvegarder dans le fichier JSON
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)
    print(f"{len(data)} nouveaux articles ajoutés au fichier : {filepath}")

# Définir les mots-clés et paramètres
keywords_ar = ["كورونا", "لقاح كورونا", "كوفيد"]
keywords_fr = ["coronavirus", "vaccin covid", "pandémie covid"]
keywords_en = ["coronavirus", "covid vaccine", "covid pandemic"]

languages = {
    "ar": {"keywords": keywords_ar, "location": "ma", "hl": "ar"},  # Maroc et arabe
    "fr": {"keywords": keywords_fr, "location": "fr", "hl": "fr"},  # France et français
    "en": {"keywords": keywords_en, "location": "us", "hl": "en"},  # USA et anglais
}

base_path = "data/raw"

# Collecte des articles
for lang, config in languages.items():
    print(f"Collecte des articles pour la langue : {lang}")
    all_articles = []

    for keyword in config["keywords"]:
        print(f"  - Collecte des articles pour le mot-clé : {keyword} (langue : {lang}, localisation : {config['location']})")
        articles = get_google_news(query=keyword, language=config["hl"], location=config["location"])
        all_articles.extend(articles)

    # Sauvegarder dans un fichier JSON
    save_to_json(all_articles, os.path.join(base_path, f"google_news_{lang}.json"))
