"""
Persian Subword Tokenizer

Implements character-level and morphological subword tokenization for Persian.
Useful for handling rare words and morphological analysis.
"""

import re
from typing import List, Dict, Set, Tuple
from collections import Counter


class PersianCharacterTokenizer:
    """
    Character-level tokenizer for Persian.

    Breaks text into individual characters while preserving
    character combinations where appropriate.
    """

    def __init__(self, preserve_diacritics: bool = True):
        """
        Initialize character tokenizer.

        Args:
            preserve_diacritics: Keep Arabic diacritics as separate tokens
        """
        self.preserve_diacritics = preserve_diacritics

        # Diacritic marks
        self.diacritics = '\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652\u0653\u0654\u0655'

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into characters.

        Args:
            text: Input text

        Returns:
            List of characters
        """
        if not text:
            return []

        chars = list(text)

        if not self.preserve_diacritics:
            chars = [c for c in chars if c not in self.diacritics]

        return chars

    def detokenize(self, chars: List[str]) -> str:
        """
        Reconstruct text from characters.

        Args:
            chars: List of characters

        Returns:
            Reconstructed text
        """
        return ''.join(chars)


class PersianMorphemeTokenizer:
    """
    Morpheme-based tokenizer for Persian.

    Attempts to split words into morphological components
    (prefixes, stems, suffixes).
    """

    def __init__(self):
        """Initialize morpheme tokenizer."""

        # Common Persian prefixes
        self.prefixes = {
            'می': 'PRES',       # Present tense marker
            'نمی': 'NEG_PRES',  # Negative present
            'بی': 'WITHOUT',    # Without
            'با': 'WITH',       # With
            'هم': 'CO',         # Co-, together
            'نا': 'UN',         # Un-, in-
            'غیر': 'NON',       # Non-
            'پیش': 'PRE',       # Pre-, before
            'پس': 'POST',       # Post-, after
            'بر': 'ON',         # On
            'در': 'IN',         # In
            'فرا': 'TRANS',     # Trans-, beyond
        }

        # Common Persian suffixes
        self.suffixes = {
            # Plural
            'ها': 'PL',
            'ان': 'PL',
            'ات': 'PL',

            # Possessive pronouns
            'م': 'POSS_1S',
            'ت': 'POSS_2S',
            'ش': 'POSS_3S',
            'مان': 'POSS_1P',
            'تان': 'POSS_2P',
            'شان': 'POSS_3P',

            # Comparative
            'تر': 'COMP',
            'ترین': 'SUPER',

            # Adverbial/adjectival
            'انه': 'MANNER',
            'وار': 'LIKE',
            'ناک': 'FULL_OF',
            'گر': 'AGENT',
            'گری': 'ACT_OF',

            # Verb endings
            'ید': 'PAST_2P',
            'یم': 'PRES_1P',
            'ند': 'PRES_3P',
            'د': 'PAST_3S',
        }

    def tokenize(self, word: str, return_tags: bool = False) -> List[str]:
        """
        Tokenize word into morphemes.

        Args:
            word: Input word
            return_tags: If True, returns (morpheme, tag) tuples

        Returns:
            List of morphemes or (morpheme, tag) tuples
        """
        if not word:
            return []

        morphemes = []
        remaining = word
        original = word

        # Check for prefixes (longest first)
        for prefix in sorted(self.prefixes.keys(), key=len, reverse=True):
            if remaining.startswith(prefix):
                if return_tags:
                    morphemes.append((prefix, self.prefixes[prefix]))
                else:
                    morphemes.append(prefix)
                remaining = remaining[len(prefix):]
                break

        # Check for suffixes (longest first)
        suffix_found = None
        for suffix in sorted(self.suffixes.keys(), key=len, reverse=True):
            if remaining.endswith(suffix):
                suffix_found = suffix
                remaining = remaining[:-len(suffix)]
                break

        # Add the stem (what's left)
        if remaining:
            if return_tags:
                morphemes.append((remaining, 'STEM'))
            else:
                morphemes.append(remaining)

        # Add the suffix
        if suffix_found:
            if return_tags:
                morphemes.append((suffix_found, self.suffixes[suffix_found]))
            else:
                morphemes.append(suffix_found)

        # If no morphemes found, return original word
        if not morphemes:
            if return_tags:
                return [(original, 'WORD')]
            else:
                return [original]

        return morphemes

    def tokenize_with_tags(self, word: str) -> List[Tuple[str, str]]:
        """
        Tokenize word and return morphemes with tags.

        Returns:
            List of (morpheme, tag) tuples
        """
        return self.tokenize(word, return_tags=True)


class PersianSyllableTokenizer:
    """
    Syllable-based tokenizer for Persian.

    Attempts to break words into syllables based on Persian
    phonological rules.
    """

    def __init__(self):
        """Initialize syllable tokenizer."""

        # Persian vowels (long and short)
        self.vowels = 'aeiouاوی'  # Simplified

        # Persian consonants pattern
        self.persian_consonants = r'[بپتثجچحخدذرزژسشصضطظعغفقکگلمنهی]'

    def tokenize(self, word: str) -> List[str]:
        """
        Tokenize word into syllables.

        This is a simplified syllabification based on common patterns.

        Args:
            word: Input word

        Returns:
            List of syllables
        """
        if not word:
            return []

        # Simple approach: split on vowel boundaries
        # This is a basic implementation and may not be perfect

        syllables = []
        current = []

        for i, char in enumerate(word):
            current.append(char)

            # Check if we should break here
            if char in self.vowels:
                # Look ahead - if next is consonant followed by vowel, break
                if i + 2 < len(word):
                    next_char = word[i + 1]
                    next_next = word[i + 2]

                    if next_char not in self.vowels and next_next in self.vowels:
                        syllables.append(''.join(current))
                        current = []

        # Add remaining
        if current:
            syllables.append(''.join(current))

        return syllables if syllables else [word]

    def count_syllables(self, word: str) -> int:
        """
        Count syllables in a word.

        Args:
            word: Input word

        Returns:
            Number of syllables
        """
        return len(self.tokenize(word))
