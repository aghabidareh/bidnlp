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
        words = text.split()
        return len(set(words)) / len(words) if words else 0

    @staticmethod
    def digit_ratio(text):
        digits = sum(1 for char in text if char.isdigit())
        return digits / len(text) if text else 0
