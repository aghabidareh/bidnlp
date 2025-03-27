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
        pass