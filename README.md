# Multilingual Tweet Cleaner

**Multilingual Tweet Cleaner** est un projet d'automatisation du nettoyage et de la normalisation des tweets collectés en plusieurs langues (français, anglais, arabe). Ce projet permet de préparer les données pour des analyses de sentiment, des études de tendance, ou d'autres traitements de données.

## Fonctionnalités

- **Collecte de données** : Récupération des tweets depuis des plateformes sociales (par exemple, Twitter).
- **Nettoyage des tweets** : Suppression des mentions, liens, hashtags, emojis et caractères non pertinents.
- **Normalisation des textes** : Conversion des textes en minuscules, gestion des stopwords pour chaque langue et correction des caractères.
- **Support multilingue** : Traitement des tweets en français, anglais et arabe.
- **Sauvegarde des données** : Enregistrement des données nettoyées dans différents formats (JSON, CSV, Parquet).

## Structure du projet

project_root/
│
├── data/                          # Répertoire pour les données brutes et traitées
│   ├── raw/                       # Données brutes collectées
│   │   ├── tweets_french.json
│   │   ├── tweets_english.json
│   │   └── tweets_arabic.json
│   ├── cleaned/                   # Données nettoyées et prêtes
│   │   ├── cleaned_tweets_french.json
│   │   ├── cleaned_tweets_english.json
│   │   └── cleaned_tweets_arabic.json
│   └── logs/                      # Logs des processus de collecte/prétraitement
│       ├── ingestion.log
│       └── cleaning.log
│
├── notebooks/                     # Notebooks Jupyter pour les tests rapides
│   ├── data_collection.ipynb      # Notebook pour tester la collecte des données
│   ├── preprocessing.ipynb        # Notebook pour tester le nettoyage des données
│   └── eda.ipynb                  # Analyse exploratoire des données
│
├── scripts/                       # Scripts pour automatiser les tâches
│   ├── ingestion/
│   │   ├── collect_tweets.py      # Script pour collecter les tweets via API
│   │   └── validate_ingestion.py  # Script pour valider l'ingestion
│   ├── preprocessing/
│   │   ├── clean_tweets.py        # Script pour le nettoyage des tweets
│   │   ├── remove_stopwords.py    # Utilitaire pour gérer les mots vides
│   │   └── normalize_text.py      # Normalisation et gestion des langues
│   └── utils/
│       ├── logger.py              # Gestion des logs
│       └── config.py              # Configuration globale (API keys, paramètres)
│
├── config/                        # Fichiers de configuration
│   ├── api_keys.json              # Clés API pour Twitter/Facebook
│   ├── stopwords/                 # Listes personnalisées de mots vides
│   │   ├── stopwords_fr.txt
│   │   ├── stopwords_en.txt
│   │   └── stopwords_ar.txt
│   └── spark_config.yaml          # Configuration Spark
│
├── reports/                       # Rapports et résultats intermédiaires
│   ├── eda/                       # Résultats de l'analyse exploratoire
│   │   └── eda_summary.html
│   └── logs/                      # Logs consolidés pour reporting
│
├── tests/                         # Scripts de tests unitaires et d'intégration
│   ├── test_ingestion.py          # Tests pour les scripts d’ingestion
│   ├── test_cleaning.py           # Tests pour le nettoyage et prétraitement
│   └── test_utils.py              # Tests pour les utilitaires
│
├── results/                       # Résultats finaux de la phase 2
│   ├── multilingual_dataset.csv   # Jeu de données final nettoyé
│   └── multilingual_dataset.parquet # Format optimisé pour Big Data
│
├── README.md                      # Documentation sur la phase 2
├── requirements.txt               # Bibliothèques nécessaires (Python, PySpark, etc.)
└── .gitignore                     # Fichiers/dossiers à ignorer par Git
