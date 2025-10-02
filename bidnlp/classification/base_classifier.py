"""
Base Text Classifier

Provides base class for Persian text classification tasks.
"""

from typing import List, Dict, Optional, Any
from abc import ABC, abstractmethod


class BaseTextClassifier(ABC):
    """Base class for text classifiers."""

    def __init__(self, normalize: bool = True, remove_stopwords: bool = False):
        """
        Initialize the base classifier.

        Args:
            normalize: Whether to normalize text before classification
            remove_stopwords: Whether to remove stop words
        """
        self.normalize = normalize
        self.remove_stopwords = remove_stopwords
        self._is_trained = False

    def preprocess(self, text: str) -> str:
        """
        Preprocess text before classification.

        Args:
            text: Input text

        Returns:
            Preprocessed text
        """
        if not text:
            return ""

        processed_text = text

        if self.normalize:
            try:
                from ..preprocessing import PersianNormalizer
                normalizer = PersianNormalizer()
                processed_text = normalizer.normalize(processed_text)
            except ImportError:
                pass

        if self.remove_stopwords:
            try:
                from ..utils import PersianStopWords
                stopwords = PersianStopWords()
                processed_text = stopwords.remove_stopwords(processed_text)
            except ImportError:
                pass

        return processed_text

    @abstractmethod
    def train(self, texts: List[str], labels: List[str]) -> None:
        """
        Train the classifier.

        Args:
            texts: List of training texts
            labels: List of corresponding labels
        """
        pass

    @abstractmethod
    def predict(self, text: str) -> str:
        """
        Predict the class of a text.

        Args:
            text: Input text

        Returns:
            Predicted class label
        """
        pass

    def predict_batch(self, texts: List[str]) -> List[str]:
        """
        Predict classes for multiple texts.

        Args:
            texts: List of input texts

        Returns:
            List of predicted class labels
        """
        return [self.predict(text) for text in texts]

    def predict_proba(self, text: str) -> Dict[str, float]:
        """
        Predict class probabilities for a text.

        Args:
            text: Input text

        Returns:
            Dictionary mapping class labels to probabilities
        """
        # Default implementation returns confidence 1.0 for predicted class
        predicted = self.predict(text)
        return {predicted: 1.0}

    def is_trained(self) -> bool:
        """
        Check if the classifier has been trained.

        Returns:
            True if trained
        """
        return self._is_trained

    def evaluate(self, texts: List[str], true_labels: List[str]) -> Dict[str, float]:
        """
        Evaluate classifier performance.

        Args:
            texts: List of test texts
            true_labels: List of true labels

        Returns:
            Dictionary with evaluation metrics
        """
        if not self.is_trained():
            raise ValueError("Classifier must be trained before evaluation")

        predicted_labels = self.predict_batch(texts)

        # Calculate accuracy
        correct = sum(1 for pred, true in zip(predicted_labels, true_labels) if pred == true)
        accuracy = correct / len(true_labels) if true_labels else 0.0

        # Calculate per-class metrics
        from ..utils import PersianTextMetrics
        report = PersianTextMetrics.classification_report(predicted_labels, true_labels)

        return {
            'accuracy': accuracy,
            'classification_report': report
        }

    def get_params(self) -> Dict[str, Any]:
        """
        Get classifier parameters.

        Returns:
            Dictionary of parameters
        """
        return {
            'normalize': self.normalize,
            'remove_stopwords': self.remove_stopwords,
            'is_trained': self._is_trained
        }

    def set_params(self, **params) -> None:
        """
        Set classifier parameters.

        Args:
            **params: Parameters to set
        """
        for key, value in params.items():
            if hasattr(self, key):
                setattr(self, key, value)
