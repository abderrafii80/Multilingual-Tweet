import json
import os
import time
from pytrends.request import TrendReq

def get_trending_data(keywords, timeframe='today 12-m', geo='', lang='en'):
    """
    Récupère les données de tendances Google Trends pour une liste de mots-clés.

    Args:
        keywords (list): Liste des mots-clés à analyser.
        timeframe (str): Période à analyser (ex : 'today 12-m' pour les 12 derniers mois).
        geo (str): Code pays (ex : 'US' pour les États-Unis, 'FR' pour la France).
        lang (str): Langue des requêtes Google Trends ('en', 'fr', 'ar').
    
    Returns:
        dict: Données des tendances par mot-clé.
    """
    pytrends = TrendReq(hl=lang, tz=360)  # Langue et fuseau horaire
    
    trends_data = {}
    for keyword in keywords:
        try:
            print(f"Collecte des données pour le mot-clé : {keyword} ({lang})")
            pytrends.build_payload([keyword], timeframe=timeframe, geo=geo)
            interest_over_time = pytrends.interest_over_time()
            
            if not interest_over_time.empty:
                # Convertir les Timestamp en chaînes
                trends_data[keyword] = {str(date): value for date, value in interest_over_time[keyword].items()}
            else:
                trends_data[keyword] = {"message": "Aucune donnée trouvée pour ce mot-clé."}
        
        except Exception as e:
            trends_data[keyword] = {"error": str(e)}
            print(f"Erreur pour le mot-clé {keyword}: {e}")
        
        # Pause entre les requêtes pour éviter le code 429
        time.sleep(10)
    
    return trends_data


def save_to_json(data, output_file):
    """
    Sauvegarde les données de tendances dans un fichier JSON.

    Args:
        data (dict): Données à sauvegarder.
        output_file (str): Chemin du fichier de sortie.
    """
    # Créer le répertoire s'il n'existe pas
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Sauvegarder les données
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Données sauvegardées dans {output_file}")


if __name__ == "__main__":
    # Mots-clés liés au COVID
    keywords_ar = ["كورونا", "لقاح كورونا", "كوفيد"]
    keywords_fr = ["coronavirus", "vaccin covid", "pandémie covid"]
    keywords_en = ["coronavirus", "covid vaccine", "covid pandemic"]

    # Chemin où les fichiers seront sauvegardés
    base_path = "data/raw/"

    # Collecte des données pour chaque langue
    print("Collecte des tendances pour les mots-clés en arabe...")
    trends_ar = get_trending_data(keywords_ar, timeframe='today 12-m', geo='EG', lang='ar')
    save_to_json(trends_ar, os.path.join(base_path, 'trends_ar.json'))

    print("Collecte des tendances pour les mots-clés en français...")
    trends_fr = get_trending_data(keywords_fr, timeframe='today 12-m', geo='FR', lang='fr')
    save_to_json(trends_fr, os.path.join(base_path, 'trends_fr.json'))

    print("Collecte des tendances pour les mots-clés en anglais...")
    trends_en = get_trending_data(keywords_en, timeframe='today 12-m', geo='US', lang='en')
    save_to_json(trends_en, os.path.join(base_path, 'trends_en.json'))
