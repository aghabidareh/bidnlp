import os
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from gensim.models import Word2Vec, FastText
import joblib


class TextVectorizer:
    def __init__(self, method='tfidf', max_features=5000, model_path=None):
        self.method = method.lower()
        self.max_features = max_features

        if self.method == "bow":
            self.vectorizer = CountVectorizer(max_features=self.max_features)
        elif self.method == "tfidf":
            self.vectorizer = TfidfVectorizer(max_features=self.max_features)
        elif self.method in ["word2vec", "fasttext"]:
            self.model = Word2Vec.load(model_path) if model_path else None
        else:
            raise ValueError("Invalid vectorization method. Choose 'bow', 'tfidf', 'word2vec', or 'fasttext'.")

    def fit(self, corpus):
        if self.method in ['bow', 'tfidf']:
            self.vectorizer.fit(corpus)
        elif self.method in ['word2vec', 'fasttext']:
            tokenized_sequences = [sentence.split() for sentence in corpus]
            self.model = Word2Vec(sentences=tokenized_sequences, vector_size=100, window=5, min_count=2, workers=4) \
                if self.method == "word2vec" else FastText(sentences=tokenized_sequences, vector_size=100, window=5,
                                                           min_count=2, workers=4)

    def transform(self, text):
        if self.method in ['bow', 'tfidf']:
            return self.vectorizer.transform([text]).toarray()
        elif self.method in ['word2vec', 'fasttext']:
            words = text.split()
            vectors = [self.model.wv[word] for word in words if word in self.model.wv]
            return np.mean(vectors, axis=0) if vectors else np.zeros(self.model.vector_size)

    def save_model(self, path):
        if self.method in ['word2vec', 'fasttext']:
            self.model.save(path)
        else:
            joblib.dump(self.model, path)

    def load_model(self, path):
        if self.method in ["word2vec", "fasttext"]:
            self.model = Word2Vec.load(path) if self.method == "word2vec" else FastText.load(path)
        else:
            self.vectorizer = joblib.load(path)
