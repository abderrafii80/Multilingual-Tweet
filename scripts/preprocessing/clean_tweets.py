# ========= Import Library
import pandas as pd
import re
import unicodedata
import emoji



# Fonction clean_tweet
# Fonction de nettoyage des tweets
def clean_tweet(tweet, stopwords, lang='en'):
    # ========= Nettoyage des tweets
    if lang in ['fr', 'en']:  # On inclut l'anglais si besoin
        tweet = unicodedata.normalize('NFD', tweet)  # Décompose les caractères accentués en lettre de base + diacritiques
        tweet = ''.join(c for c in tweet if unicodedata.category(c) != 'Mn')  # Supprime les diacritiques (accents)

    tweet = re.sub("@[A-Za-z0-9]+", "", tweet)  
    tweet = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", tweet)  
    tweet = re.sub(r"[^a-zA-Z\u0621-\u064A\s]", "", tweet)  
    
    if lang == 'ar':
        tweet = re.sub(r"[إأآا]", "ا", tweet)  
        tweet = re.sub(r"ؤ", "و", tweet)
        tweet = re.sub(r"ئ", "ي", tweet)

    tweet = " ".join(tweet.split())  # rm space multi
    tweet = ''.join(c for c in tweet if c not in emoji.EMOJI_DATA)  # rm emoji
    tweet = tweet.replace("#", "").replace("_", " ")  # Hashtag
    tweet = tweet.lower()  # lower

    # Remove stopwords
    tweet = " ".join(word for word in tweet.split() if word not in stopwords)
    return tweet




# ===========  Fonction load_stopwords
# Charger les stopwords à partir des fichiers stopwords_fr/_en/_ar.txt
def load_stopwords(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return set(word.strip().lower() for word in file.readlines())





# ===========  Fonction  process_data 
def process_data(lang):
    if lang == 'en':
        df = pd.read_json('data/raw/tweets_en.json', lines=True)
        stopwords = load_stopwords("config/stopwords/stopwords_en.txt")
    elif lang == 'ar':
        df = pd.read_json('data/raw/tweets_ar.json', lines=True)
        stopwords = load_stopwords("config/stopwords/stopwords_ar.txt")
    elif lang == 'fr':
        df = pd.read_json('data/raw/tweets_fr.json', lines=True)
        stopwords = load_stopwords("config/stopwords/stopwords_fr.txt")
    else:
        raise ValueError("Language not supported")

    # Nettoyage des tweets pour chaque langue
    for i, tweet in enumerate(df['text']):
        df.at[i, 'text'] = clean_tweet(tweet, stopwords, lang)

    # Sauvegarder le DataFrame nettoyé (Save)
    output_file = f'data/cleaned/cleaned_tweets_{lang}.json'
    df.to_json(output_file, force_ascii=False, indent=4)
    print(f"Data cleaned and saved to {output_file}")









# =======================================
# =======================================
# Call Function process_data 
# =======================================
for lang in ['en', 'ar', 'fr']:
    process_data(lang)
