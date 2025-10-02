"""
Feature Extraction for Persian Text

Provides feature extraction methods for text classification.
"""

from typing import List, Dict, Optional
from collections import defaultdict, Counter
import math


class BagOfWords:
    """Bag of Words feature extractor."""

    def __init__(self, max_features: Optional[int] = None, min_df: int = 1):
        """
        Initialize Bag of Words extractor.

        Args:
            max_features: Maximum number of features to extract
            min_df: Minimum document frequency for a word to be included
        """
        self.max_features = max_features
        self.min_df = min_df
        self.vocabulary = {}
        self.document_frequency = defaultdict(int)
        self._is_fitted = False

    def fit(self, documents: List[str]) -> 'BagOfWords':
        """
        Fit the vocabulary from documents.

        Args:
            documents: List of text documents

        Returns:
            Self
        """
        # Count word frequencies across documents
        word_docs = defaultdict(set)
        all_words = Counter()

        for doc_id, doc in enumerate(documents):
            words = doc.split()
            all_words.update(words)
            for word in set(words):
                word_docs[word].add(doc_id)

        # Filter by document frequency
        valid_words = {word for word, docs in word_docs.items()
                      if len(docs) >= self.min_df}

        # Get most common words
        if self.max_features:
            word_counts = {word: count for word, count in all_words.items()
                          if word in valid_words}
            top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
            vocabulary_words = [word for word, _ in top_words[:self.max_features]]
        else:
            vocabulary_words = sorted(valid_words)

        # Create vocabulary mapping
        self.vocabulary = {word: idx for idx, word in enumerate(vocabulary_words)}
        self.document_frequency = {word: len(word_docs[word]) for word in vocabulary_words}
        self._is_fitted = True

        return self

    def transform(self, documents: List[str]) -> List[Dict[int, int]]:
        """
        Transform documents to BoW vectors.

        Args:
            documents: List of text documents

        Returns:
            List of sparse vectors (dict mapping feature index to count)
        """
        if not self._is_fitted:
            raise ValueError("BagOfWords must be fitted before transform")

        vectors = []
        for doc in documents:
            words = doc.split()
            vector = defaultdict(int)

            for word in words:
                if word in self.vocabulary:
                    idx = self.vocabulary[word]
                    vector[idx] += 1

            vectors.append(dict(vector))

        return vectors

    def fit_transform(self, documents: List[str]) -> List[Dict[int, int]]:
        """
        Fit and transform documents.

        Args:
            documents: List of text documents

        Returns:
            List of sparse vectors
        """
        self.fit(documents)
        return self.transform(documents)

    def get_feature_names(self) -> List[str]:
        """Get feature names (words in vocabulary)."""
        if not self._is_fitted:
            return []
        # Sort by index
        sorted_vocab = sorted(self.vocabulary.items(), key=lambda x: x[1])
        return [word for word, idx in sorted_vocab]


class TfidfVectorizer:
    """TF-IDF feature extractor."""

    def __init__(self, max_features: Optional[int] = None, min_df: int = 1):
        """
        Initialize TF-IDF vectorizer.

        Args:
            max_features: Maximum number of features
            min_df: Minimum document frequency
        """
        self.max_features = max_features
        self.min_df = min_df
        self.vocabulary = {}
        self.idf = {}
        self.num_documents = 0
        self._is_fitted = False

    def fit(self, documents: List[str]) -> 'TfidfVectorizer':
        """
        Fit IDF from documents.

        Args:
            documents: List of text documents

        Returns:
            Self
        """
        self.num_documents = len(documents)

        # Count document frequencies
        word_docs = defaultdict(set)
        all_words = Counter()

        for doc_id, doc in enumerate(documents):
            words = doc.split()
            all_words.update(words)
            for word in set(words):
                word_docs[word].add(doc_id)

        # Filter by document frequency
        valid_words = {word for word, docs in word_docs.items()
                      if len(docs) >= self.min_df}

        # Get most common words
        if self.max_features:
            word_counts = {word: count for word, count in all_words.items()
                          if word in valid_words}
            top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
            vocabulary_words = [word for word, _ in top_words[:self.max_features]]
        else:
            vocabulary_words = sorted(valid_words)

        # Create vocabulary and calculate IDF
        self.vocabulary = {word: idx for idx, word in enumerate(vocabulary_words)}
        self.idf = {}

        for word in vocabulary_words:
            df = len(word_docs[word])
            # IDF = log(N / df) + 1
            self.idf[word] = math.log(self.num_documents / df) + 1

        self._is_fitted = True
        return self

    def transform(self, documents: List[str]) -> List[Dict[int, float]]:
        """
        Transform documents to TF-IDF vectors.

        Args:
            documents: List of text documents

        Returns:
            List of sparse TF-IDF vectors
        """
        if not self._is_fitted:
            raise ValueError("TfidfVectorizer must be fitted before transform")

        vectors = []
        for doc in documents:
            words = doc.split()
            word_counts = Counter(words)
            total_words = len(words)

            vector = {}
            for word, count in word_counts.items():
                if word in self.vocabulary:
                    idx = self.vocabulary[word]
                    # TF = count / total_words
                    tf = count / total_words if total_words > 0 else 0
                    # TF-IDF = TF * IDF
                    tfidf = tf * self.idf[word]
                    vector[idx] = tfidf

            # Normalize vector (L2 norm)
            norm = math.sqrt(sum(v * v for v in vector.values()))
            if norm > 0:
                vector = {k: v / norm for k, v in vector.items()}

            vectors.append(vector)

        return vectors

    def fit_transform(self, documents: List[str]) -> List[Dict[int, float]]:
        """
        Fit and transform documents.

        Args:
            documents: List of text documents

        Returns:
            List of sparse TF-IDF vectors
        """
        self.fit(documents)
        return self.transform(documents)

    def get_feature_names(self) -> List[str]:
        """Get feature names (words in vocabulary)."""
        if not self._is_fitted:
            return []
        sorted_vocab = sorted(self.vocabulary.items(), key=lambda x: x[1])
        return [word for word, idx in sorted_vocab]


class NgramExtractor:
    """N-gram feature extractor."""

    def __init__(self, n: int = 2, max_features: Optional[int] = None):
        """
        Initialize N-gram extractor.

        Args:
            n: Size of n-grams (2 for bigrams, 3 for trigrams, etc.)
            max_features: Maximum number of features
        """
        self.n = n
        self.max_features = max_features
        self.vocabulary = {}
        self._is_fitted = False

    def _extract_ngrams(self, text: str) -> List[str]:
        """Extract n-grams from text."""
        words = text.split()
        ngrams = []
        for i in range(len(words) - self.n + 1):
            ngram = ' '.join(words[i:i + self.n])
            ngrams.append(ngram)
        return ngrams

    def fit(self, documents: List[str]) -> 'NgramExtractor':
        """
        Fit vocabulary from documents.

        Args:
            documents: List of text documents

        Returns:
            Self
        """
        # Extract all n-grams
        all_ngrams = Counter()
        for doc in documents:
            ngrams = self._extract_ngrams(doc)
            all_ngrams.update(ngrams)

        # Get top n-grams
        if self.max_features:
            top_ngrams = all_ngrams.most_common(self.max_features)
            vocabulary_ngrams = [ngram for ngram, _ in top_ngrams]
        else:
            vocabulary_ngrams = sorted(all_ngrams.keys())

        # Create vocabulary
        self.vocabulary = {ngram: idx for idx, ngram in enumerate(vocabulary_ngrams)}
        self._is_fitted = True

        return self

    def transform(self, documents: List[str]) -> List[Dict[int, int]]:
        """
        Transform documents to n-gram vectors.

        Args:
            documents: List of text documents

        Returns:
            List of sparse n-gram vectors
        """
        if not self._is_fitted:
            raise ValueError("NgramExtractor must be fitted before transform")

        vectors = []
        for doc in documents:
            ngrams = self._extract_ngrams(doc)
            vector = defaultdict(int)

            for ngram in ngrams:
                if ngram in self.vocabulary:
                    idx = self.vocabulary[ngram]
                    vector[idx] += 1

            vectors.append(dict(vector))

        return vectors

    def fit_transform(self, documents: List[str]) -> List[Dict[int, int]]:
        """
        Fit and transform documents.

        Args:
            documents: List of text documents

        Returns:
            List of sparse n-gram vectors
        """
        self.fit(documents)
        return self.transform(documents)

    def get_feature_names(self) -> List[str]:
        """Get feature names (n-grams in vocabulary)."""
        if not self._is_fitted:
            return []
        sorted_vocab = sorted(self.vocabulary.items(), key=lambda x: x[1])
        return [ngram for ngram, idx in sorted_vocab]
