import tweepy
import json
import time

# Remplacez par votre propre token Bearer
client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAMwcxAEAAAAALgRvw4rAxx9WF3XBetMRr6nTFwk%3DOxJ6G6gtTi4hvUpT4V5cK7dlkTtFjGOTpAyGViOiZhhUObhzwl')

# Requête de recherche (partagée entre toutes les langues)
query = 'covid -is:retweet'

# Liste des langues et leurs codes
languages = {
    'fr': 'français',
    'en': 'anglais',
    'ar': 'arabe'
}

# Fonction pour collecter et enregistrer les tweets
def collect_tweets(language_code, language_name):
    # Nom du fichier pour chaque langue
    file_name = f'tweets_{language_code}.json'

    # Ajouter le filtre de langue à la requête
    query_with_language = f"{query} lang:{language_code}"

    # Ouvrir le fichier en mode 'a+' pour ajouter ou créer si nécessaire
    with open(file_name, 'a+', encoding='utf-8') as filehandle:
        while True:  # Boucle pour essayer de récupérer les tweets en cas de limite de requêtes
            try:
                for tweet in tweepy.Paginator(client.search_recent_tweets, query=query_with_language,
                                              tweet_fields=['context_annotations', 'created_at', 'author_id', 'text'], 
                                              max_results=10).flatten(limit=10):
                    # Créer un dictionnaire pour chaque tweet
                    tweet_info = {
                        'tweet_id': tweet.id,
                        'text': tweet.text,
                        'created_at': tweet.created_at.isoformat(),
                        'author_id': tweet.author_id,
                        'context_annotations': tweet.context_annotations if tweet.context_annotations else None,
                        'language': language_name  # Ajouter la langue au dictionnaire
                    }

                    # Écrire le dictionnaire sous format JSON dans le fichier
                    json.dump(tweet_info, filehandle, ensure_ascii=False)
                    filehandle.write('\n')  # Ajouter une nouvelle ligne pour chaque tweet pour séparer les entrées

                    # Ajouter une pause pour éviter de dépasser les limites de requêtes
                    time.sleep(1)  # Délai plus court ici, ajustez selon le besoin

                # Si on a récupéré tous les tweets sans erreurs, sortir de la boucle
                break

            except tweepy.errors.TooManyRequests as e:
                # Si le quota est dépassé, attendre jusqu'à la réinitialisation
                reset_time = int(e.response.headers['x-rate-limit-reset'])
                wait_time = reset_time - int(time.time()) + 1
                print(f"Rate limit exceeded, waiting for {wait_time} seconds.")
                time.sleep(wait_time)  # Attendre jusqu'à la réinitialisation du quota
            except Exception as e:
                # Si une autre erreur se produit, l'afficher et sortir de la boucle
                print(f"An error occurred: {e}")
                break

    print(f"Tweets in {language_name} have been written to {file_name}")

# Collecter des tweets pour chaque langue
for code, name in languages.items():
    collect_tweets(code, name)







# ======================================================
# import tweepy
# import json
# import time

# # Remplacez par votre propre token Bearer
# client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAMkSxAEAAAAAGHIwjBexYXOCUCfcrfDeTvp3mIM%3DS6x8gEzGypyI0dxZ9JuSKivDs4f37NRVujue3jrUDYEBYuDDdZ')

# # Remplacez par votre propre requête de recherche
# query = 'covid -is:retweet'

# # Nom et chemin du fichier où vous souhaitez enregistrer les Tweets
# file_name = 'tweets.json'

# # Ouvrir le fichier en mode 'a+' pour ajouter ou créer si nécessaire
# with open(file_name, 'a+', encoding='utf-8') as filehandle:
#     for tweet in tweepy.Paginator(client.search_recent_tweets, query=query,
#                                   tweet_fields=['context_annotations', 'created_at', 'author_id', 'text'], 
#                                   max_results=100).flatten(limit=1000):
#         try:
#             # Créer un dictionnaire pour chaque tweet
#             tweet_info = {
#                 'tweet_id': tweet.id,
#                 'text': tweet.text,
#                 'created_at': tweet.created_at.isoformat(),
#                 'author_id': tweet.author_id,
#                 'context_annotations': tweet.context_annotations if tweet.context_annotations else None
#             }

#             # Écrire le dictionnaire sous format JSON dans le fichier
#             json.dump(tweet_info, filehandle, ensure_ascii=False)
#             filehandle.write('\n')  # Ajouter une nouvelle ligne pour chaque tweet pour séparer les entrées

#             # Ajouter une pause pour éviter de dépasser les limites de requêtes
#             time.sleep(5)  # Augmenter le délai à 5 secondes entre les requêtes

#         except tweepy.errors.TooManyRequests as e:
#             # Si le quota est dépassé, attendre jusqu'à la réinitialisation
#             reset_time = int(e.response.headers['x-rate-limit-reset'])
#             wait_time = reset_time - int(time.time()) + 1
#             print(f"Rate limit exceeded, waiting for {wait_time} seconds.")
#             time.sleep(wait_time)

# print(f"Tweets have been written to {file_name}")
