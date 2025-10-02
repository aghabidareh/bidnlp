"""
Persian Text Statistics

Provides utilities for calculating statistics on Persian text.
"""

import re
from typing import Dict, List, Optional
from .characters import PersianCharacters


class PersianTextStatistics:
    """Calculate various statistics for Persian text."""

    def __init__(self):
        """Initialize the statistics calculator."""
        self.char_utils = PersianCharacters()

    def character_count(self, text: str, include_spaces: bool = False) -> int:
        """
        Count characters in text.

        Args:
            text: Input text
            include_spaces: Whether to include spaces in count

        Returns:
            Number of characters
        """
        if include_spaces:
            return len(text)
        return len(text.replace(' ', '').replace('\n', '').replace('\t', ''))

    def word_count(self, text: str) -> int:
        """
        Count words in text.

        Args:
            text: Input text

        Returns:
            Number of words
        """
        if not text:
            return 0

        # Split on whitespace and filter empty strings
        words = [w for w in text.split() if w.strip()]
        return len(words)

    def sentence_count(self, text: str) -> int:
        """
        Count sentences in text.

        Args:
            text: Input text

        Returns:
            Number of sentences
        """
        if not text:
            return 0

        # Persian and English sentence-ending punctuation
        sentence_endings = r'[.!?؟]+'
        sentences = re.split(sentence_endings, text)
        # Filter out empty strings
        sentences = [s.strip() for s in sentences if s.strip()]
        return len(sentences)

    def line_count(self, text: str) -> int:
        """
        Count lines in text.

        Args:
            text: Input text

        Returns:
            Number of lines
        """
        if not text:
            return 0
        return len(text.splitlines())

    def paragraph_count(self, text: str) -> int:
        """
        Count paragraphs in text (separated by blank lines).

        Args:
            text: Input text

        Returns:
            Number of paragraphs
        """
        if not text:
            return 0

        # Split by multiple newlines
        paragraphs = re.split(r'\n\s*\n', text)
        # Filter out empty strings
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        return len(paragraphs)

    def persian_character_count(self, text: str) -> int:
        """
        Count Persian characters only.

        Args:
            text: Input text

        Returns:
            Number of Persian characters
        """
        return sum(1 for char in text if self.char_utils.is_persian(char))

    def arabic_character_count(self, text: str) -> int:
        """
        Count Arabic-specific characters.

        Args:
            text: Input text

        Returns:
            Number of Arabic characters
        """
        return sum(1 for char in text if self.char_utils.is_arabic(char))

    def digit_count(self, text: str) -> int:
        """
        Count all digits (Persian, Arabic-Indic, English).

        Args:
            text: Input text

        Returns:
            Number of digits
        """
        return sum(1 for char in text if self.char_utils.is_digit(char))

    def punctuation_count(self, text: str) -> int:
        """
        Count punctuation marks.

        Args:
            text: Input text

        Returns:
            Number of punctuation marks
        """
        import string
        persian_punct = self.char_utils.PERSIAN_PUNCTUATION
        return sum(1 for char in text if char in string.punctuation or char in persian_punct)

    def average_word_length(self, text: str) -> float:
        """
        Calculate average word length.

        Args:
            text: Input text

        Returns:
            Average word length (0 if no words)
        """
        words = text.split()
        if not words:
            return 0.0

        total_length = sum(len(word) for word in words)
        return total_length / len(words)

    def average_sentence_length(self, text: str) -> float:
        """
        Calculate average sentence length in words.

        Args:
            text: Input text

        Returns:
            Average sentence length (0 if no sentences)
        """
        num_sentences = self.sentence_count(text)
        if num_sentences == 0:
            return 0.0

        num_words = self.word_count(text)
        return num_words / num_sentences

    def lexical_diversity(self, text: str) -> float:
        """
        Calculate lexical diversity (unique words / total words).

        Args:
            text: Input text

        Returns:
            Lexical diversity ratio (0.0-1.0)
        """
        words = text.split()
        if not words:
            return 0.0

        unique_words = set(words)
        return len(unique_words) / len(words)

    def persian_ratio(self, text: str) -> float:
        """
        Calculate ratio of Persian characters to total alphabetic characters.

        Args:
            text: Input text

        Returns:
            Persian character ratio (0.0-1.0)
        """
        total_alpha = sum(1 for char in text if char.isalpha())
        if total_alpha == 0:
            return 0.0

        persian_count = self.persian_character_count(text)
        return persian_count / total_alpha

    def get_statistics(self, text: str) -> Dict[str, any]:
        """
        Get comprehensive statistics for text.

        Args:
            text: Input text

        Returns:
            Dictionary containing all statistics
        """
        char_types = self.char_utils.count_character_types(text)

        return {
            'total_characters': len(text),
            'characters_no_spaces': self.character_count(text, include_spaces=False),
            'words': self.word_count(text),
            'sentences': self.sentence_count(text),
            'lines': self.line_count(text),
            'paragraphs': self.paragraph_count(text),
            'persian_characters': char_types['persian'],
            'arabic_characters': char_types['arabic'],
            'persian_digits': char_types['persian_digit'],
            'arabic_indic_digits': char_types['arabic_indic_digit'],
            'english_digits': char_types['english_digit'],
            'punctuation': self.punctuation_count(text),
            'spaces': char_types['space'],
            'diacritics': char_types['diacritic'],
            'zwnj_count': char_types['zwnj'],
            'average_word_length': round(self.average_word_length(text), 2),
            'average_sentence_length': round(self.average_sentence_length(text), 2),
            'lexical_diversity': round(self.lexical_diversity(text), 4),
            'persian_ratio': round(self.persian_ratio(text), 4),
        }

    def word_frequency(self, text: str, top_n: Optional[int] = None) -> List[tuple]:
        """
        Get word frequency distribution.

        Args:
            text: Input text
            top_n: Number of most frequent words to return (None for all)

        Returns:
            List of (word, frequency) tuples, sorted by frequency (descending)
        """
        from collections import Counter

        words = text.split()
        frequency = Counter(words)

        # Sort by frequency (descending)
        sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)

        if top_n:
            return sorted_freq[:top_n]
        return sorted_freq

    def character_frequency(self, text: str, top_n: Optional[int] = None) -> List[tuple]:
        """
        Get character frequency distribution.

        Args:
            text: Input text
            top_n: Number of most frequent characters to return (None for all)

        Returns:
            List of (character, frequency) tuples, sorted by frequency (descending)
        """
        from collections import Counter

        # Remove spaces for cleaner results
        chars = [c for c in text if not c.isspace()]
        frequency = Counter(chars)

        # Sort by frequency (descending)
        sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)

        if top_n:
            return sorted_freq[:top_n]
        return sorted_freq

    def longest_word(self, text: str) -> str:
        """
        Find the longest word in text.

        Args:
            text: Input text

        Returns:
            Longest word (empty string if no words)
        """
        words = text.split()
        if not words:
            return ""
        return max(words, key=len)

    def shortest_word(self, text: str) -> str:
        """
        Find the shortest word in text.

        Args:
            text: Input text

        Returns:
            Shortest word (empty string if no words)
        """
        words = text.split()
        if not words:
            return ""
        return min(words, key=len)

    def get_ngrams(self, text: str, n: int = 2) -> List[tuple]:
        """
        Get n-grams from text.

        Args:
            text: Input text
            n: Size of n-grams

        Returns:
            List of n-gram tuples
        """
        words = text.split()
        ngrams = []

        for i in range(len(words) - n + 1):
            ngram = tuple(words[i:i+n])
            ngrams.append(ngram)

        return ngrams

    def ngram_frequency(self, text: str, n: int = 2, top_k: Optional[int] = None) -> List[tuple]:
        """
        Get n-gram frequency distribution.

        Args:
            text: Input text
            n: Size of n-grams
            top_k: Number of most frequent n-grams to return (None for all)

        Returns:
            List of (ngram, frequency) tuples, sorted by frequency (descending)
        """
        from collections import Counter

        ngrams = self.get_ngrams(text, n)
        frequency = Counter(ngrams)

        # Sort by frequency (descending)
        sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)

        if top_k:
            return sorted_freq[:top_k]
        return sorted_freq
