def remove_stopwords(text, language):
    stopwords = {
        "anglais": {"the", "is", "and", "of", "in", "to"},
        "francais": {"le", "la", "et", "les", "des", "dans"},
        "arabe": {"و", "في", "على", "من", "إلى"}
    }
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in stopwords.get(language, set())]
    return " ".join(filtered_words)
