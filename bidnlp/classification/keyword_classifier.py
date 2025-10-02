"""
Keyword-Based Text Classifier

Provides keyword-based text classification for Persian text.
"""

from typing import List, Dict, Optional, Set
from collections import defaultdict
from .base_classifier import BaseTextClassifier


class KeywordClassifier(BaseTextClassifier):
    """Keyword-based text classifier."""

    def __init__(self,
                 normalize: bool = True,
                 remove_stopwords: bool = True,
                 categories: Optional[Dict[str, Set[str]]] = None):
        """
        Initialize keyword classifier.

        Args:
            normalize: Whether to normalize text
            remove_stopwords: Whether to remove stop words
            categories: Dictionary mapping category names to keyword sets
        """
        super().__init__(normalize=normalize, remove_stopwords=remove_stopwords)
        self.categories = categories or {}
        self._is_trained = len(self.categories) > 0

    def train(self, texts: List[str], labels: List[str]) -> None:
        """
        Train classifier by extracting keywords from training data.
        This is a simple approach that extracts most frequent words per category.

        Args:
            texts: List of training texts
            labels: List of corresponding category labels
        """
        if len(texts) != len(labels):
            raise ValueError("texts and labels must have the same length")

        # Group texts by category
        category_texts = defaultdict(list)
        for text, label in zip(texts, labels):
            processed = self.preprocess(text)
            category_texts[label].append(processed)

        # Extract keywords for each category (top frequent words)
        self.categories = {}
        for category, cat_texts in category_texts.items():
            # Concatenate all texts for this category
            all_text = ' '.join(cat_texts)
            words = all_text.split()

            # Count word frequencies
            word_freq = defaultdict(int)
            for word in words:
                if len(word) > 2:  # Skip very short words
                    word_freq[word] += 1

            # Get top N keywords
            top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:50]
            self.categories[category] = {word for word, freq in top_keywords}

        self._is_trained = True

    def add_category(self, category: str, keywords: Set[str]) -> None:
        """
        Add a new category with keywords.

        Args:
            category: Category name
            keywords: Set of keywords for this category
        """
        self.categories[category] = keywords
        self._is_trained = True

    def add_keyword_to_category(self, category: str, keyword: str) -> None:
        """
        Add a keyword to an existing category.

        Args:
            category: Category name
            keyword: Keyword to add
        """
        if category not in self.categories:
            self.categories[category] = set()
        self.categories[category].add(keyword)

    def remove_category(self, category: str) -> None:
        """
        Remove a category.

        Args:
            category: Category name
        """
        if category in self.categories:
            del self.categories[category]

    def get_categories(self) -> List[str]:
        """
        Get list of all categories.

        Returns:
            List of category names
        """
        return list(self.categories.keys())

    def get_category_keywords(self, category: str) -> Set[str]:
        """
        Get keywords for a category.

        Args:
            category: Category name

        Returns:
            Set of keywords
        """
        return self.categories.get(category, set())

    def classify(self, text: str) -> Dict[str, any]:
        """
        Classify text with detailed results.

        Args:
            text: Input text

        Returns:
            Dictionary with classification results
        """
        if not self._is_trained:
            raise ValueError("Classifier must be trained or have categories defined")

        # Preprocess
        processed_text = self.preprocess(text)
        words = set(processed_text.split())

        # Score each category
        scores = {}
        matched_keywords = {}

        for category, keywords in self.categories.items():
            # Count matching keywords
            matches = words & keywords
            score = len(matches)
            scores[category] = score
            matched_keywords[category] = list(matches)

        # Find best category
        if not scores or all(score == 0 for score in scores.values()):
            best_category = 'unknown'
            confidence = 0.0
        else:
            best_category = max(scores, key=scores.get)
            total_matches = sum(scores.values())
            confidence = scores[best_category] / total_matches if total_matches > 0 else 0.0

        return {
            'category': best_category,
            'confidence': confidence,
            'scores': scores,
            'matched_keywords': matched_keywords,
        }

    def predict(self, text: str) -> str:
        """
        Predict category for text.

        Args:
            text: Input text

        Returns:
            Predicted category
        """
        result = self.classify(text)
        return result['category']

    def predict_proba(self, text: str) -> Dict[str, float]:
        """
        Predict category probabilities.

        Args:
            text: Input text

        Returns:
            Dictionary mapping categories to probabilities
        """
        result = self.classify(text)
        scores = result['scores']
        total = sum(scores.values())

        if total == 0:
            # Equal probability for all categories
            num_categories = len(self.categories)
            if num_categories == 0:
                return {}
            prob = 1.0 / num_categories
            return {cat: prob for cat in self.categories.keys()}

        # Convert scores to probabilities
        proba = {cat: score / total for cat, score in scores.items()}
        return proba

    def predict_top_k(self, text: str, k: int = 3) -> List[tuple]:
        """
        Predict top K categories.

        Args:
            text: Input text
            k: Number of top categories to return

        Returns:
            List of (category, probability) tuples
        """
        proba = self.predict_proba(text)
        sorted_proba = sorted(proba.items(), key=lambda x: x[1], reverse=True)
        return sorted_proba[:k]

    def get_params(self) -> Dict[str, any]:
        """Get classifier parameters."""
        params = super().get_params()
        params.update({
            'num_categories': len(self.categories),
            'categories': list(self.categories.keys()),
        })
        return params
