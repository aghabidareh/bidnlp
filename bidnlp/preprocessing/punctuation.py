"""
Persian Punctuation Normalizer

Handles normalization and standardization of punctuation marks including:
- Persian to Latin punctuation conversion
- Latin to Persian punctuation conversion
- Quotation mark normalization
- Spacing around punctuation
"""

import re
from typing import Optional


class PersianPunctuationNormalizer:
    """
    Punctuation normalizer for Persian (Farsi) text.

    Handles conversion and normalization of punctuation marks.
    """

    def __init__(
        self,
        normalize_quotes: bool = True,
        normalize_question_marks: bool = True,
        normalize_commas: bool = True,
        add_space_after_punctuation: bool = True,
        remove_space_before_punctuation: bool = True,
        target_style: str = 'persian'  # 'persian' or 'latin'
    ):
        """
        Initialize the punctuation normalizer.

        Args:
            normalize_quotes: Normalize quotation marks
            normalize_question_marks: Normalize question marks
            normalize_commas: Normalize commas
            add_space_after_punctuation: Add space after punctuation
            remove_space_before_punctuation: Remove space before punctuation
            target_style: Target punctuation style ('persian' or 'latin')
        """
        self.normalize_quotes = normalize_quotes
        self.normalize_question_marks = normalize_question_marks
        self.normalize_commas = normalize_commas
        self.add_space_after_punctuation = add_space_after_punctuation
        self.remove_space_before_punctuation = remove_space_before_punctuation
        self.target_style = target_style

        # Punctuation mappings
        self.persian_to_latin = {
            '،': ',',   # Persian comma to Latin comma
            '؛': ';',   # Persian semicolon to Latin semicolon
            '؟': '?',   # Persian question mark to Latin question mark
            '٪': '%',   # Persian percent to Latin percent
            '×': '*',   # Multiplication sign
            '÷': '/',   # Division sign
        }

        self.latin_to_persian = {v: k for k, v in self.persian_to_latin.items()}

        # Quote mappings
        self.quote_pairs = {
            # Persian guillemets
            '«': '»',
            '»': '«',
            # Latin quotes
            '"': '"',
            "'": "'",
            # Fancy quotes
            '\u201c': '\u201d',  # Left and right double quotation marks
            '\u2018': '\u2019',  # Left and right single quotation marks
        }

        # Standard Persian quotes
        self.persian_open_quote = '«'
        self.persian_close_quote = '»'

        # Standard Latin quotes
        self.latin_open_quote = '"'
        self.latin_close_quote = '"'

    def normalize_persian_punctuation(self, text: str) -> str:
        """Convert Latin punctuation to Persian"""
        for latin, persian in self.latin_to_persian.items():
            text = text.replace(latin, persian)
        return text

    def normalize_latin_punctuation(self, text: str) -> str:
        """Convert Persian punctuation to Latin"""
        for persian, latin in self.persian_to_latin.items():
            text = text.replace(persian, latin)
        return text

    def normalize_quotation_marks(self, text: str) -> str:
        """Normalize quotation marks to target style"""
        if not self.normalize_quotes:
            return text

        if self.target_style == 'persian':
            # Convert all quotes to Persian guillemets
            # Handle paired quotes
            quote_chars = ['"', "'", '"', '"', ''', ''']
            for quote in quote_chars:
                # Simple replacement (not context-aware)
                text = text.replace(quote, self.persian_open_quote)

            # Try to balance quotes
            text = self._balance_quotes(text, self.persian_open_quote, self.persian_close_quote)

        else:  # latin
            # Convert to Latin quotes
            text = text.replace('«', self.latin_open_quote)
            text = text.replace('»', self.latin_close_quote)

            # Balance quotes
            text = self._balance_quotes(text, self.latin_open_quote, self.latin_close_quote)

        return text

    def _balance_quotes(self, text: str, open_quote: str, close_quote: str) -> str:
        """Balance opening and closing quotes"""
        # Count quotes and alternate between open/close
        parts = text.split(open_quote)
        result = []

        for i, part in enumerate(parts):
            if i == 0:
                result.append(part)
            elif i % 2 == 1:  # Odd index = opening quote
                result.append(open_quote + part)
            else:  # Even index = should be closing quote
                # Replace first occurrence of open quote with close quote
                if open_quote in part:
                    part = part.replace(open_quote, close_quote, 1)
                result.append(part)

        return ''.join(result)

    def fix_spacing_around_punctuation(self, text: str) -> str:
        """Fix spacing around punctuation marks"""
        # Get all punctuation marks
        all_punctuation = list(self.persian_to_latin.keys()) + list(self.persian_to_latin.values())
        all_punctuation.extend(['.', '!', ':', '?', ',', ';'])

        # Remove duplicates
        all_punctuation = list(set(all_punctuation))

        if self.remove_space_before_punctuation:
            # Remove space before punctuation
            for punct in all_punctuation:
                text = re.sub(r'\s+' + re.escape(punct), punct, text)

        if self.add_space_after_punctuation:
            # Add space after punctuation if not present
            for punct in all_punctuation:
                # Don't add space if followed by another punctuation or end of string
                text = re.sub(
                    re.escape(punct) + r'(?=[^\s' + re.escape(''.join(all_punctuation)) + r'])',
                    punct + ' ',
                    text
                )

        return text

    def normalize_ellipsis(self, text: str) -> str:
        """Normalize ellipsis (three dots)"""
        # Convert multiple dots to ellipsis
        text = re.sub(r'\.{3,}', '…', text)

        # Add space after ellipsis if missing
        text = re.sub(r'…(?=\S)', '… ', text)

        return text

    def normalize_dashes(self, text: str) -> str:
        """Normalize various dash characters"""
        # Various dash characters
        dashes = [
            '‒',  # Figure dash
            '–',  # En dash
            '—',  # Em dash
            '―',  # Horizontal bar
        ]

        # Normalize to hyphen or em dash based on context
        for dash in dashes:
            # If surrounded by spaces, use em dash
            text = re.sub(r'\s' + re.escape(dash) + r'\s', ' — ', text)
            # Otherwise use hyphen
            text = text.replace(dash, '-')

        return text

    def remove_duplicate_punctuation(self, text: str) -> str:
        """Remove duplicate punctuation marks"""
        # Remove multiple consecutive punctuation (except periods for ellipsis)
        text = re.sub(r'([،؛؟!?;])\1+', r'\1', text)

        # Remove multiple consecutive commas/semicolons
        text = re.sub(r'[،,]+', '،' if self.target_style == 'persian' else ',', text)

        # Remove multiple question marks
        text = re.sub(r'[؟?]+', '؟' if self.target_style == 'persian' else '?', text)

        return text

    def normalize(self, text: str) -> str:
        """
        Apply all punctuation normalization steps.

        Args:
            text: Input text

        Returns:
            Text with normalized punctuation
        """
        if not text:
            return text

        # Normalize punctuation marks based on target style
        if self.target_style == 'persian':
            if self.normalize_commas or self.normalize_question_marks:
                text = self.normalize_persian_punctuation(text)
        else:
            text = self.normalize_latin_punctuation(text)

        # Normalize quotes
        text = self.normalize_quotation_marks(text)

        # Normalize ellipsis
        text = self.normalize_ellipsis(text)

        # Normalize dashes
        text = self.normalize_dashes(text)

        # Remove duplicate punctuation
        text = self.remove_duplicate_punctuation(text)

        # Fix spacing
        text = self.fix_spacing_around_punctuation(text)

        return text

    def count_punctuation(self, text: str) -> dict:
        """
        Count occurrences of each punctuation mark.

        Args:
            text: Input text

        Returns:
            Dictionary of punctuation counts
        """
        counts = {}

        # Persian punctuation
        for punct in self.persian_to_latin.keys():
            count = text.count(punct)
            if count > 0:
                counts[punct] = count

        # Latin punctuation
        for punct in ['.', ',', '!', '?', ';', ':']:
            count = text.count(punct)
            if count > 0:
                counts[punct] = count

        return counts
