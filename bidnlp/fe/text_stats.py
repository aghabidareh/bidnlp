import numpy as np

class TextStats:
    @staticmethod
    def char_count(text):
        return len(text)

    @staticmethod
    def word_count(text):
        return len(text.split())

    @staticmethod
    def average_word_length(text):
        words = text.split()
        return np.mean([len(word) for word in words]) if words else 0

    @staticmethod
    def lexical_diversity(text):
        pass