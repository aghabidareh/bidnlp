import re
import os
import nltk
from nltk.corpus import stopwords , wordnet
from nltk.stem import PorterStemmer, LancasterStemmer , WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import functools

nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")

class TextPreprocessor:
    PERSIAN_SUFFIXES = ["ها", "های", "تر", "ترین", "ای", "ام", "ات", "اش", "مان", "تان", "شان"]
    PERSIAN_LEMMA_DICT = {
        "دوید": "دویدن", "رفت": "رفتن", "آمد": "آمدن", "گفت": "گفتن",
        "خواست": "خواستن", "دید": "دیدن", "نوشت": "نوشتن", "خواند": "خواندن",
        "گرفت": "گرفتن", "داد": "دادن"
    }
    POS_TAG_MAP = {
        "N": wordnet.NOUN,
        "V": wordnet.VERB,
        "J": wordnet.ADJ,
        "R": wordnet.ADV
    }

    def __init__(self , stopwords_file=None , language="english", stemmer_type="porter" , use_lemmatization=False):
        self.stopwords = set(stopwords.words(language)) if language in stopwords.fileids() else set()
        if stopwords_file:
            self.load_stopwords(stopwords_file)

        self.language = language
        self.use_lemmatization = use_lemmatization

        if use_lemmatization:
            self.lemmatizer = WordNetLemmatizer() if language == "english" else None
        else:
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
        text = re.sub(regex , replace , text)
        return text

    def remove_stopwords(self, text):
        words = text.split()
        words = [word for word in words if word not in self.stopwords]
        text = ' '.join(words)
        return text

    def lemmatize(self , text):
        words = word_tokenize(text)
        if self.language == "english" and self.lemmatizer:
            words = [self.lemmatizer.lemmatize(word, self.get_pos(word)) for word in words]
        elif self.language == "persian":
            words = [self.persian_lemmatizer(word) for word in words]
        return " ".join(words)

    @functools.lru_cache(maxsize=10000)
    def persian_lemmatizer(self, word):
        if word in self.PERSIAN_LEMMA_DICT:
            return self.PERSIAN_LEMMA_DICT[word]
        for suffix in self.PERSIAN_SUFFIXES:
            if word.endswith(suffix):
                return word[:-len(suffix)]
        return word

    def stem(self, text):
        words = text.split()
        if self.language == "english" and self.stemmer:
            words = [self.stemmer.stem(word) for word in words]
        elif self.language == "persian":
            words = [self.persian_stemmer(word) for word in words]
        return " ".join(words)

    def persian_stemmer(self , word):
        return self.persian_lemmatizer(word)

    def get_pos(self, word):
        tag = pos_tag([word])[0][1][0].upper()
        return self.POS_TAG_MAP.get(tag, wordnet.NOUN)

    def preprocess(self , text , apply_stemming=True):
        text = self.normalize(text)
        text = self.remove_punctuation(text)
        text = self.remove_stopwords(text)
        if self.use_lemmatization:
            text = self.lemmatize(text)
        elif apply_stemming:
            text = self.stem(text)
        return text