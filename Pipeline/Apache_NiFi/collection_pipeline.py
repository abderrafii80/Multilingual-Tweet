import requests
import os
import json

def fetch_articles(api_key, keywords, lang, output_file):
    """
    Recherche des articles sur NewsAPI et sauvegarde les résultats dans un fichier JSON.
    """
    base_url = "https://newsapi.org/v2/everything"
    articles_data = {}

    for keyword in keywords:
        print(f"Recherche d'articles pour le mot-clé : {keyword} ({lang})...")
        params = {
            "q": keyword,
            "language": lang,
            "apiKey": api_key,
            "pageSize": 100  # Nombre maximum d'articles par requête
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            articles = response.json()
            articles_data[keyword] = articles.get("articles", [])
        else:
            print(f"Erreur lors de la collecte pour le mot-clé {keyword}: {response.status_code}")
            articles_data[keyword] = {"error": response.json()}

    # Sauvegarder les résultats
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(articles_data, f, ensure_ascii=False, indent=4)
    print(f"Articles sauvegardés dans {output_file}")

if __name__ == "__main__":
    
    API_KEY = "f0d6967b96304b5289030c11b677829c"

    # Définir les mots-clés pour chaque langue
    keywords_ar = ["كورونا", "كوفيد", "كوفيد-19", "جائحة كورونا", "فيروس كورونا", 
               "لقاح كورونا", "أعراض كورونا", "انتشار كورونا", "حجر صحي", 
               "فحص كورونا", "تطعيم كورونا", "علاج كورونا"]

    keywords_fr = ["coronavirus", "covid", "covid-19", "pandémie covid", "vaccin covid", 
               "symptômes covid", "confinement", "propagation covid", 
               "test covid", "isolement", "variant covid", "traitement covid"]

    keywords_en = ["coronavirus", "covid", "covid-19", "covid pandemic", "covid vaccine", 
               "covid symptoms", "lockdown", "covid spread", "covid test", 
               "quarantine", "covid variant", "covid treatment"]


    # Chemin de sauvegarde
    base_path = "data/raw/"

    # Collecte des articles
    fetch_articles(API_KEY, keywords_ar, lang='ar', output_file=os.path.join(base_path, 'articles_news_ar.json'))
    fetch_articles(API_KEY, keywords_fr, lang='fr', output_file=os.path.join(base_path, 'articles_news_fr.json'))
    fetch_articles(API_KEY, keywords_en, lang='en', output_file=os.path.join(base_path, 'articles_news_en.json'))
