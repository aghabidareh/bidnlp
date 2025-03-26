import re
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, LancasterStemmer

nltk.download("stopwords")

class TextPreprocessor:

    PERSIAN_SUFFIXES = ["ها", "های", "تر", "ترین", "ای", "ام", "ات", "اش", "مان", "تان", "شان"]
    PERSIAN_ROOTS = {
        "دوید": "دو", "رفت": "رو", "آمد": "آی", "گفت": "گو", "خواست": "خواه",
        "دید": "بین", "نوشت": "نویس", "خواند": "خوان", "گرفت": "گیر"
    }

    def __init__(self , stopwords_file=None , language="english", stemmer_type="porter"):
        self.stopwords = set(stopwords.words(language))
        if stopwords_file:
            self.load_stopwords(stopwords_file)

        self.language = language
        self.stemmer = self._initialize_stemmer(language, stemmer_type)

    def load_stopwords(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, "r" , encoding='utf-8') as file:
                user_stopword = set(file.read().splitlines())
                self.stopwords.update(user_stopword)

    @staticmethod
    def _initialize_stemmer(self, language, stemmer_type):
        if language == "english":
            return PorterStemmer() if stemmer_type == "porter" else LancasterStemmer()
        return None

    @staticmethod
    def normalize(self, text):
        regex = r'\s+'
        replace = ' '
        text = text.lower().strip()
        text = re.sub(regex , replace , text)
        return text

    @staticmethod
    def remove_punctuation(self, text):
        regex = '[^\w\s]'
        replace = ''
        return re.sub(regex , replace , text)

    def remove_stopwords(self, text):
        words = text.split()
        words = [word for word in words if word not in self.stopwords]
        return ' '.join(words)

    @staticmethod
    def tokenize(self , text):
        return text.split()

    def preprocess(self , text):
        text = self.normalize(text)
        text = self.remove_punctuation(text)
        text = self.remove_stopwords(text)
        return text