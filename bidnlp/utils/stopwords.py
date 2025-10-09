"""
Persian Stop Words

Provides Persian stop words list and utilities.
"""

import os
from typing import Set, List, Optional


class PersianStopWords:
    """Persian stop words management."""

    # Load default stopwords from file
    _DEFAULT_STOPWORDS = None

    @classmethod
    def _load_default_stopwords(cls) -> Set[str]:
        """Load default stopwords from stopwords.txt file."""
        if cls._DEFAULT_STOPWORDS is not None:
            return cls._DEFAULT_STOPWORDS

        # Get the path to stopwords.txt in the project root
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        stopwords_path = os.path.join(project_root, 'stopwords.txt')

        stopwords = set()
        if os.path.exists(stopwords_path):
            with open(stopwords_path, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word:  # Skip empty lines
                        stopwords.add(word)

        cls._DEFAULT_STOPWORDS = stopwords
        return stopwords

    @property
    def DEFAULT_STOPWORDS(self) -> Set[str]:
        """Get default stopwords."""
        return self._load_default_stopwords()

    def __init__(self, custom_stopwords: Optional[Set[str]] = None,
                 include_defaults: bool = True):
        """
        Initialize stop words manager.

        Args:
            custom_stopwords: Additional custom stop words
            include_defaults: Whether to include default stop words
        """
        self.stopwords = set()

        if include_defaults:
            self.stopwords.update(self.DEFAULT_STOPWORDS)

        if custom_stopwords:
            self.stopwords.update(custom_stopwords)

    def is_stopword(self, word: str) -> bool:
        """
        Check if a word is a stop word.

        Args:
            word: Word to check

        Returns:
            True if word is a stop word
        """
        return word.strip() in self.stopwords

    def remove_stopwords(self, text: str) -> str:
        """
        Remove stop words from text.

        Args:
            text: Input text

        Returns:
            Text with stop words removed
        """
        words = text.split()
        filtered_words = [word for word in words if not self.is_stopword(word)]
        return ' '.join(filtered_words)

    def filter_stopwords(self, words: List[str]) -> List[str]:
        """
        Filter stop words from a list of words.

        Args:
            words: List of words

        Returns:
            List with stop words removed
        """
        return [word for word in words if not self.is_stopword(word)]

    def add_stopword(self, word: str) -> None:
        """
        Add a custom stop word.

        Args:
            word: Stop word to add
        """
        self.stopwords.add(word.strip())

    def add_stopwords(self, words: List[str]) -> None:
        """
        Add multiple custom stop words.

        Args:
            words: List of stop words to add
        """
        self.stopwords.update(word.strip() for word in words)

    def remove_stopword(self, word: str) -> None:
        """
        Remove a word from stop words list.

        Args:
            word: Word to remove
        """
        self.stopwords.discard(word.strip())

    def remove_stopwords_from_list(self, words: List[str]) -> None:
        """
        Remove multiple words from stop words list.

        Args:
            words: List of words to remove
        """
        for word in words:
            self.stopwords.discard(word.strip())

    def get_stopwords(self) -> Set[str]:
        """
        Get the current stop words set.

        Returns:
            Set of stop words
        """
        return self.stopwords.copy()

    def get_stopwords_list(self) -> List[str]:
        """
        Get the current stop words as a sorted list.

        Returns:
            Sorted list of stop words
        """
        return sorted(self.stopwords)

    def count_stopwords(self, text: str) -> int:
        """
        Count stop words in text.

        Args:
            text: Input text

        Returns:
            Number of stop words
        """
        words = text.split()
        return sum(1 for word in words if self.is_stopword(word))

    def stopword_ratio(self, text: str) -> float:
        """
        Calculate ratio of stop words to total words.

        Args:
            text: Input text

        Returns:
            Stop word ratio (0.0-1.0)
        """
        words = text.split()
        if not words:
            return 0.0

        stopword_count = self.count_stopwords(text)
        return stopword_count / len(words)

    def reset_to_defaults(self) -> None:
        """Reset stop words to default list."""
        self.stopwords = self._load_default_stopwords().copy()

    def clear(self) -> None:
        """Clear all stop words."""
        self.stopwords.clear()

    @classmethod
    def get_default_stopwords(cls) -> Set[str]:
        """
        Get the default Persian stop words.

        Returns:
            Set of default stop words
        """
        return cls._load_default_stopwords().copy()

    @classmethod
    def get_default_stopwords_list(cls) -> List[str]:
        """
        Get the default Persian stop words as a sorted list.

        Returns:
            Sorted list of default stop words
        """
        return sorted(cls._load_default_stopwords())
