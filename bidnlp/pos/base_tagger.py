"""
Base POS Tagger

Provides abstract base class for Persian POS taggers.
"""

from typing import List, Tuple, Dict, Optional, Any
from abc import ABC, abstractmethod


class BasePOSTagger(ABC):
    """Base class for POS taggers."""

    def __init__(self, normalize: bool = True):
        """
        Initialize the base POS tagger.

        Args:
            normalize: Whether to normalize text before tagging
        """
        self.normalize = normalize
        self._is_trained = False

    def preprocess(self, text: str) -> str:
        """
        Preprocess text before tagging.

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

        return processed_text

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words.

        Args:
            text: Input text

        Returns:
            List of tokens
        """
        try:
            from ..tokenization import PersianWordTokenizer
            tokenizer = PersianWordTokenizer()
            return tokenizer.tokenize(text)
        except ImportError:
            # Fallback to simple whitespace tokenization
            return text.split()

    @abstractmethod
    def tag(self, text: str) -> List[Tuple[str, str]]:
        """
        Tag a text with POS tags.

        Args:
            text: Input text

        Returns:
            List of (word, tag) tuples
        """
        pass

    def tag_words(self, words: List[str]) -> List[Tuple[str, str]]:
        """
        Tag a list of words.

        Args:
            words: List of words

        Returns:
            List of (word, tag) tuples
        """
        # Join words and tag the text
        text = ' '.join(words)
        return self.tag(text)

    def tag_batch(self, texts: List[str]) -> List[List[Tuple[str, str]]]:
        """
        Tag multiple texts.

        Args:
            texts: List of input texts

        Returns:
            List of tagged results
        """
        return [self.tag(text) for text in texts]

    def get_tags(self, text: str) -> List[str]:
        """
        Get only the POS tags for a text.

        Args:
            text: Input text

        Returns:
            List of POS tags
        """
        tagged = self.tag(text)
        return [tag for word, tag in tagged]

    def get_words_by_tag(self, text: str, tag: str) -> List[str]:
        """
        Get all words with a specific POS tag.

        Args:
            text: Input text
            tag: POS tag to filter by

        Returns:
            List of words with the specified tag
        """
        tagged = self.tag(text)
        return [word for word, word_tag in tagged if word_tag == tag]

    def get_tag_counts(self, text: str) -> Dict[str, int]:
        """
        Get counts of each POS tag in text.

        Args:
            text: Input text

        Returns:
            Dictionary mapping tags to counts
        """
        tags = self.get_tags(text)
        tag_counts: Dict[str, int] = {}
        for tag in tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        return tag_counts

    def get_tag_distribution(self, text: str) -> Dict[str, float]:
        """
        Get distribution of POS tags in text.

        Args:
            text: Input text

        Returns:
            Dictionary mapping tags to their proportion
        """
        tag_counts = self.get_tag_counts(text)
        total = sum(tag_counts.values())
        if total == 0:
            return {}
        return {tag: count / total for tag, count in tag_counts.items()}

    def is_trained(self) -> bool:
        """
        Check if the tagger has been trained.

        Returns:
            True if trained
        """
        return self._is_trained

    def get_params(self) -> Dict[str, Any]:
        """
        Get tagger parameters.

        Returns:
            Dictionary of parameters
        """
        return {
            'normalize': self.normalize,
            'is_trained': self._is_trained
        }

    def set_params(self, **params) -> None:
        """
        Set tagger parameters.

        Args:
            **params: Parameters to set
        """
        for key, value in params.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def evaluate(self, texts: List[str], true_tags: List[List[str]]) -> Dict[str, float]:
        """
        Evaluate tagger performance.

        Args:
            texts: List of test texts
            true_tags: List of true tag sequences

        Returns:
            Dictionary with evaluation metrics
        """
        predicted_tags = [self.get_tags(text) for text in texts]

        # Calculate accuracy
        total = 0
        correct = 0
        for pred, true in zip(predicted_tags, true_tags):
            for p, t in zip(pred, true):
                total += 1
                if p == t:
                    correct += 1

        accuracy = correct / total if total > 0 else 0.0

        return {
            'accuracy': accuracy,
            'total_tags': total,
            'correct_tags': correct
        }
