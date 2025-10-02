"""
Persian Sentence Tokenizer

Handles sentence boundary detection for Persian text, including:
- Persian and Latin punctuation
- Abbreviations and exceptions
- Numbers and dates
- Quotations
"""

import re
from typing import List, Tuple, Optional


class PersianSentenceTokenizer:
    """
    Sentence tokenizer for Persian (Farsi) language.

    Detects sentence boundaries while handling Persian-specific
    punctuation and common abbreviations.
    """

    def __init__(self):
        """Initialize the sentence tokenizer."""

        # Sentence-ending punctuation
        self.sentence_endings = ['.', '!', '?', '؟', '!']  # Persian question mark

        # Persian abbreviations that shouldn't end a sentence
        self.abbreviations = {
            'ص', 'ج', 'ق', 'ه', 'م',  # Common Islamic abbreviations
            'Dr', 'Mr', 'Mrs', 'Ms', 'Prof',  # English titles
            'دکتر', 'آقای', 'خانم',  # Persian titles
            'ش', 'پ',  # Shamsi date abbreviations
        }

        # Patterns that indicate sentence continuation
        self.continuation_patterns = [
            r'\d+\.\d+',  # Decimal numbers
            r'[A-Z]\.',  # Single letter abbreviations
            r'\d+\.',  # Numbers followed by period (might be list)
        ]

        # Quote marks (Persian and Latin)
        self.quote_marks = {
            'open': ['«', '"', "'", '\''],
            'close': ['»', '"', "'", '\'']
        }

    def is_sentence_boundary(self, text: str, pos: int) -> bool:
        """
        Check if position is a sentence boundary.

        Args:
            text: The full text
            pos: Position of potential sentence-ending punctuation

        Returns:
            True if this is a sentence boundary
        """
        if pos >= len(text):
            return True

        # Get the character at position
        char = text[pos]

        # Not a sentence ending punctuation
        if char not in self.sentence_endings:
            return False

        # Check if it's part of a decimal number
        if char == '.':
            # Look before
            if pos > 0 and text[pos - 1].isdigit():
                # Look after
                if pos + 1 < len(text) and text[pos + 1].isdigit():
                    return False  # Decimal number

        # Check for abbreviations
        if char == '.':
            # Get the word before the period
            before = text[:pos].rstrip()
            words = before.split()
            if words and words[-1] in self.abbreviations:
                return False

        # Look ahead for continuation indicators
        if pos + 1 < len(text):
            next_char = text[pos + 1]

            # If followed by whitespace and then lowercase, might not be boundary
            # (except in Persian where there's no case distinction)
            if next_char.isspace():
                # Skip whitespace
                i = pos + 1
                while i < len(text) and text[i].isspace():
                    i += 1

                if i < len(text):
                    next_non_space = text[i]

                    # If next char is lowercase English letter, not a boundary
                    if next_non_space.islower() and next_non_space.isascii():
                        return False

                    # If next char is a closing quote, check after that
                    if next_non_space in self.quote_marks['close']:
                        return True

        return True

    def tokenize(self, text: str, return_spans: bool = False) -> List[str]:
        """
        Tokenize text into sentences.

        Args:
            text: Input text
            return_spans: If True, returns (sentence, start, end) tuples

        Returns:
            List of sentences or list of (sentence, start, end) tuples
        """
        if not text:
            return []

        sentences = []
        current_start = 0
        i = 0

        while i < len(text):
            char = text[i]

            # Check if this is a sentence boundary
            if char in self.sentence_endings:
                if self.is_sentence_boundary(text, i):
                    # Include the punctuation in the sentence
                    sentence = text[current_start:i + 1].strip()

                    if sentence:
                        if return_spans:
                            sentences.append((sentence, current_start, i + 1))
                        else:
                            sentences.append(sentence)

                    current_start = i + 1

            i += 1

        # Add the last sentence if there is one
        if current_start < len(text):
            sentence = text[current_start:].strip()
            if sentence:
                if return_spans:
                    sentences.append((sentence, current_start, len(text)))
                else:
                    sentences.append(sentence)

        return sentences

    def tokenize_with_positions(self, text: str) -> List[Tuple[str, int, int]]:
        """
        Tokenize text into sentences with positions.

        Returns:
            List of (sentence, start_pos, end_pos) tuples
        """
        return self.tokenize(text, return_spans=True)

    def split_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences (alias for tokenize).

        Args:
            text: Input text

        Returns:
            List of sentences
        """
        return self.tokenize(text)

    def detokenize(self, sentences: List[str]) -> str:
        """
        Reconstruct text from sentences.

        Args:
            sentences: List of sentences

        Returns:
            Reconstructed text
        """
        if not sentences:
            return ""

        result = []

        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            result.append(sentence)

            # Add space between sentences if needed
            if i < len(sentences) - 1:
                # Check if sentence already ends with whitespace or punctuation
                if not sentence.endswith((' ', '\n', '\t')):
                    # Check if it ends with sentence-ending punctuation
                    if sentence and sentence[-1] not in self.sentence_endings:
                        result.append(' ')
                    else:
                        result.append(' ')

        return ''.join(result)

    def count_sentences(self, text: str) -> int:
        """
        Count the number of sentences in text.

        Args:
            text: Input text

        Returns:
            Number of sentences
        """
        return len(self.tokenize(text))
