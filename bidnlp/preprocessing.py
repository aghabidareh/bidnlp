import re
import os
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords")

class TextPreprocessor:
    def __init__(self , stopwords_file=None , language="english"):
        self.stopwords = set(stopwords.words(language))
        if stopwords_file:
            self.load_stopwords(stopwords_file)

    def load_stopwords(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, "r" , encoding='utf-8') as file:
                user_stopword = set(file.read().splitlines())
                self.stopwords.update(user_stopword)

    def normalize(self, text):
        regex = r'\s+'
        replace = ' '
        text = text.lower().strip()
        text = re.sub(regex , replace , text)
        return text

    def remove_punctuation(self, text):
        regex = '[^\w\s]'
        replace = ''
        return re.sub(regex , replace , text)

    def remove_stopwords(self, text):
        pass