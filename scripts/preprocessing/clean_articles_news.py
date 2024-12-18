# ========= Import Libraries
import pandas as pd
import re
import unicodedata
import emoji
import spacy
import json
from bs4 import BeautifulSoup  # Pour enlever les balises HTML

# ========= Charger les modèles NLP pour chaque langue
# 'en_core_web_sm' pour anglais, 'fr_core_news_sm' pour français, et 'ar_core_web_sm' pour arabe
nlp_models = {
    'en': spacy.load("en_core_web_sm"),
    'fr': spacy.load("fr_core_news_sm"),
    'ar': spacy.load("xx_ent_wiki_sm")  # Modèle multi-langue pour arabe
}

# Fonction de nettoyage des tweets
def clean_tweet(tweet, stopwords, lang='en'):
    if not tweet:
        return ""
    
    # ========= Nettoyage des tweets
    tweet = BeautifulSoup(tweet, "html.parser").get_text()  # Enlever les balises HTML
    # Nettoyer les balises spécifiques et les retours à la ligne
    tweet = re.sub(r"<ul>|</ul>|<li>|</li>|<br>|<p>|</p>|\r\n|\n", " ", tweet)  # Supprimer les balises <ul>, <li> et les retours à la ligne

    # Normaliser les lettres accentuées (applicable pour le français)
    if lang in ['fr', 'en']:  # On inclut l'anglais si besoin
        tweet = unicodedata.normalize('NFD', tweet)  # Décompose les caractères accentués en lettre de base + diacritiques
        tweet = ''.join(c for c in tweet if unicodedata.category(c) != 'Mn')  # Supprime les diacritiques (accents)
        
    tweet = re.sub(r'[^\w\s]', '', tweet)  # Enlever les caractères de ponctuation
    tweet = re.sub(r'(\w+)ing\b', r'\1', tweet) # Supprimer le suffixe ing
    # Supprimer les mentions et les hashtags
    tweet = re.sub(r"@[A-Za-z0-9]+", "", tweet)  # Supprimer les mentions (@user)
    tweet = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", tweet)  # Supprimer les liens
    tweet = re.sub(r"[^a-zA-Z\u0621-\u064A\s]", "", tweet)  # Garder uniquement les lettres et espaces

    # Traitement spécifique pour l'arabe (normalisation des lettres)
    if lang == 'ar':
        tweet = re.sub(r"[إأآا]", "ا", tweet)  # Normalisation de l'alphabet arabe
        tweet = re.sub(r"ؤ", "و", tweet)
        tweet = re.sub(r"ئ", "ي", tweet)

    # Suppression des espaces multiples, emojis et hashtags
    tweet = " ".join(tweet.split())  # Suppression des espaces multiples
    tweet = ''.join(c for c in tweet if c not in emoji.EMOJI_DATA)  # Enlever les emojis
    tweet = tweet.replace("#", "").replace("_", " ")  # Enlever les hashtags et underscores
    
    # Convertir tout en minuscules
    tweet = tweet.lower()  

    # Supprimer les stopwords
    tweet = " ".join(word for word in tweet.split() if word not in stopwords)
    
    return tweet

# Fonction pour la lemmatisation et l'extraction des entités (NER)
def lemmatize_and_extract_entities(tweet, lang):
    nlp = nlp_models.get(lang)  # Charger le modèle NLP pour la langue
    doc = nlp(tweet)
    
    # Lemmatisation
    lemmatized_text = " ".join([token.lemma_ for token in doc])

    # Extraction des entités
    entities = {"diseases": [], "vaccines": [], "treatments": []}
    for ent in doc.ents:
        if ent.label_ in ["DISEASE", "VACCINE", "TREATMENT"]:  # Adapter les labels pour votre cas
            if ent.label_ == "DISEASE":
                entities["diseases"].append(ent.text)
            elif ent.label_ == "VACCINE":
                entities["vaccines"].append(ent.text)
            elif ent.label_ == "TREATMENT":
                entities["treatments"].append(ent.text)
    
    return lemmatized_text, entities

# =========== Fonction load_stopwords
def load_stopwords(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return set(word.strip().lower() for word in file.readlines())

# =========== Fonction process_data
def process_data(lang):
    # Charger le fichier JSON
    file_path = f"data/raw/articles_news_{lang}.json"
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    # Extraire la liste d'articles depuis la clé principale
    key = list(data.keys())[0]  # Exemple : "coronavirus"
    articles = data[key]
    
    # Charger les stopwords
    stopwords = load_stopwords(f"config/stopwords/stopwords_{lang}.txt")
    
    # Préparer une liste pour stocker les résultats
    results = []

    for article in articles:
        # Extraire et concaténer les textes pertinents
        # Nettoyer chaque partie du texte avant de les concaténer
        title = clean_tweet(article.get("title", ""), stopwords, lang)
        description = clean_tweet(article.get("description", ""), stopwords, lang)
        content = clean_tweet(article.get("content", ""), stopwords, lang)
        
        # Extraire et concaténer les textes pertinents après nettoyage
        text = " ".join(filter(None, [title, description, content]))
        
        # Lemmatisation et extraction des entités
        lemmatized_text, entities = lemmatize_and_extract_entities(text, lang)

        # Ajouter les résultats
        results.append({
            "title": title,
            "description": description,
            "content": content,
            "lemmatized_text": lemmatized_text,
            "diseases": entities["diseases"],
            "vaccines": entities["vaccines"],
            "treatments": entities["treatments"],
        })
    
    # Convertir en DataFrame et sauvegarder
    df = pd.DataFrame(results)
    output_file = f"data/cleaned/cleaned_articles_news_{lang}.json"
    df.to_json(output_file, force_ascii=False, orient="records", indent=4)
    print(f"Data cleaned and saved to {output_file}")

# =======================================
# Appeler la fonction process_data pour chaque langue
for lang in ['en', 'ar', 'fr']:
    process_data(lang)
