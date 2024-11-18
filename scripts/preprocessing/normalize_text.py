import unicodedata
import re

def normalize_text(text, language):
    if language == "arabe":
        text = unicodedata.normalize("NFKD", text)  # Normaliser les caractères
        text = re.sub(r"[إأآا]", "ا", text)
        text = re.sub(r"ؤ", "و", text)
        text = re.sub(r"ئ", "ي", text)
    elif language == "francais" or language == "anglais":
        text = text.lower()  # Mettre en minuscule
    return text
