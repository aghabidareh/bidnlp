import re
import os

class TextPreprocessor:
    def __init__(self , stopwords_file=None):
        self.stopwords_file = stopwords_file
        if stopwords_file:
            self.load_stopwords(stopwords_file)

    def load_stopwords(self, file_path):
        pass