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
        pass