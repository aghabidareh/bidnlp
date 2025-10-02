"""
Persian Character Utilities

Provides utilities for working with Persian characters, alphabets, and character types.
"""

import re
from typing import Set, Optional


class PersianCharacters:
    """Utilities for Persian character handling and classification."""

    # Persian alphabet
    PERSIAN_ALPHABET = set('ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی')

    # Arabic alphabet (additional to Persian - characters that should be normalized)
    ARABIC_ALPHABET = set('أإؤئةىكي')

    # Persian digits
    PERSIAN_DIGITS = set('۰۱۲۳۴۵۶۷۸۹')

    # Arabic-Indic digits
    ARABIC_INDIC_DIGITS = set('٠١٢٣٤٥٦٧٨٩')

    # English digits
    ENGLISH_DIGITS = set('0123456789')

    # Persian punctuation
    PERSIAN_PUNCTUATION = set('،؛؟٪×÷')

    # Diacritics (تشکیل)
    DIACRITICS = set('\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652\u0653\u0654\u0655\u0656\u0657\u0658')

    # Special characters
    ZWNJ = '\u200c'  # Zero-width non-joiner
    ZWJ = '\u200d'   # Zero-width joiner
    KASHIDA = '\u0640'  # Tatweel/Kashida

    # Hamza variants
    HAMZA_VARIANTS = set('ءأإؤئ')

    # Yeh variants
    YEH_VARIANTS = set('يیئى')

    # Kaf variants
    KAF_VARIANTS = set('كک')

    # Heh variants
    HEH_VARIANTS = set('هةۀ')

    # Waw variants
    WAW_VARIANTS = set('وؤ')

    @staticmethod
    def is_persian(char: str) -> bool:
        """
        Check if a character is Persian.

        Args:
            char: Single character to check

        Returns:
            True if character is in Persian alphabet
        """
        return char in PersianCharacters.PERSIAN_ALPHABET

    @staticmethod
    def is_arabic(char: str) -> bool:
        """
        Check if a character is Arabic (but not Persian).

        Args:
            char: Single character to check

        Returns:
            True if character is Arabic-specific
        """
        return char in PersianCharacters.ARABIC_ALPHABET

    @staticmethod
    def is_persian_or_arabic(char: str) -> bool:
        """
        Check if a character is Persian or Arabic.

        Args:
            char: Single character to check

        Returns:
            True if character is Persian or Arabic
        """
        return (char in PersianCharacters.PERSIAN_ALPHABET or
                char in PersianCharacters.ARABIC_ALPHABET)

    @staticmethod
    def is_persian_digit(char: str) -> bool:
        """
        Check if a character is a Persian digit (۰-۹).

        Args:
            char: Single character to check

        Returns:
            True if character is a Persian digit
        """
        return char in PersianCharacters.PERSIAN_DIGITS

    @staticmethod
    def is_arabic_indic_digit(char: str) -> bool:
        """
        Check if a character is an Arabic-Indic digit (٠-٩).

        Args:
            char: Single character to check

        Returns:
            True if character is an Arabic-Indic digit
        """
        return char in PersianCharacters.ARABIC_INDIC_DIGITS

    @staticmethod
    def is_digit(char: str) -> bool:
        """
        Check if a character is any type of digit.

        Args:
            char: Single character to check

        Returns:
            True if character is Persian, Arabic-Indic, or English digit
        """
        return (char in PersianCharacters.PERSIAN_DIGITS or
                char in PersianCharacters.ARABIC_INDIC_DIGITS or
                char in PersianCharacters.ENGLISH_DIGITS)

    @staticmethod
    def is_diacritic(char: str) -> bool:
        """
        Check if a character is a diacritic mark (تشکیل).

        Args:
            char: Single character to check

        Returns:
            True if character is a diacritic
        """
        return char in PersianCharacters.DIACRITICS

    @staticmethod
    def is_persian_punctuation(char: str) -> bool:
        """
        Check if a character is Persian punctuation.

        Args:
            char: Single character to check

        Returns:
            True if character is Persian punctuation
        """
        return char in PersianCharacters.PERSIAN_PUNCTUATION

    @staticmethod
    def is_zwnj(char: str) -> bool:
        """
        Check if a character is zero-width non-joiner.

        Args:
            char: Single character to check

        Returns:
            True if character is ZWNJ
        """
        return char == PersianCharacters.ZWNJ

    @staticmethod
    def is_kashida(char: str) -> bool:
        """
        Check if a character is kashida/tatweel.

        Args:
            char: Single character to check

        Returns:
            True if character is kashida
        """
        return char == PersianCharacters.KASHIDA

    @staticmethod
    def get_character_type(char: str) -> str:
        """
        Get the type of a Persian/Arabic character.

        Args:
            char: Single character to check

        Returns:
            Character type: 'persian', 'arabic', 'persian_digit', 'arabic_indic_digit',
            'english_digit', 'diacritic', 'persian_punctuation', 'zwnj', 'kashida',
            'space', 'other'
        """
        if PersianCharacters.is_persian(char):
            return 'persian'
        elif PersianCharacters.is_arabic(char):
            return 'arabic'
        elif PersianCharacters.is_persian_digit(char):
            return 'persian_digit'
        elif PersianCharacters.is_arabic_indic_digit(char):
            return 'arabic_indic_digit'
        elif char in PersianCharacters.ENGLISH_DIGITS:
            return 'english_digit'
        elif PersianCharacters.is_diacritic(char):
            return 'diacritic'
        elif PersianCharacters.is_persian_punctuation(char):
            return 'persian_punctuation'
        elif PersianCharacters.is_zwnj(char):
            return 'zwnj'
        elif PersianCharacters.is_kashida(char):
            return 'kashida'
        elif char.isspace():
            return 'space'
        else:
            return 'other'

    @staticmethod
    def count_character_types(text: str) -> dict:
        """
        Count different types of characters in text.

        Args:
            text: Input text

        Returns:
            Dictionary with counts for each character type
        """
        counts = {
            'persian': 0,
            'arabic': 0,
            'persian_digit': 0,
            'arabic_indic_digit': 0,
            'english_digit': 0,
            'diacritic': 0,
            'persian_punctuation': 0,
            'zwnj': 0,
            'kashida': 0,
            'space': 0,
            'other': 0
        }

        for char in text:
            char_type = PersianCharacters.get_character_type(char)
            counts[char_type] += 1

        return counts

    @staticmethod
    def remove_diacritics(text: str) -> str:
        """
        Remove all diacritics from text.

        Args:
            text: Input text

        Returns:
            Text without diacritics
        """
        return ''.join(char for char in text if not PersianCharacters.is_diacritic(char))

    @staticmethod
    def get_persian_alphabet() -> Set[str]:
        """
        Get the Persian alphabet as a set.

        Returns:
            Set of Persian alphabet characters
        """
        return PersianCharacters.PERSIAN_ALPHABET.copy()

    @staticmethod
    def get_persian_consonants() -> Set[str]:
        """
        Get Persian consonants.

        Returns:
            Set of Persian consonant characters
        """
        vowels = set('اوی')
        return PersianCharacters.PERSIAN_ALPHABET - vowels

    @staticmethod
    def get_persian_vowels() -> Set[str]:
        """
        Get Persian vowels.

        Returns:
            Set of Persian vowel characters
        """
        return set('اوی')

    @staticmethod
    def has_diacritics(text: str) -> bool:
        """
        Check if text contains any diacritics.

        Args:
            text: Input text

        Returns:
            True if text contains diacritics
        """
        return any(PersianCharacters.is_diacritic(char) for char in text)

    @staticmethod
    def has_persian(text: str) -> bool:
        """
        Check if text contains any Persian characters.

        Args:
            text: Input text

        Returns:
            True if text contains Persian characters
        """
        return any(PersianCharacters.is_persian(char) for char in text)

    @staticmethod
    def has_arabic(text: str) -> bool:
        """
        Check if text contains any Arabic-specific characters.

        Args:
            text: Input text

        Returns:
            True if text contains Arabic characters
        """
        return any(PersianCharacters.is_arabic(char) for char in text)

    @staticmethod
    def is_persian_text(text: str, threshold: float = 0.5) -> bool:
        """
        Check if text is predominantly Persian.

        Args:
            text: Input text
            threshold: Minimum ratio of Persian characters (0.0-1.0)

        Returns:
            True if Persian character ratio >= threshold
        """
        if not text:
            return False

        persian_count = sum(1 for char in text if PersianCharacters.is_persian(char))
        total_letters = sum(1 for char in text if char.isalpha())

        if total_letters == 0:
            return False

        return (persian_count / total_letters) >= threshold

    @staticmethod
    def get_variant_group(char: str) -> Optional[str]:
        """
        Get the variant group a character belongs to.

        Args:
            char: Single character

        Returns:
            Variant group name or None
        """
        if char in PersianCharacters.YEH_VARIANTS:
            return 'yeh'
        elif char in PersianCharacters.KAF_VARIANTS:
            return 'kaf'
        elif char in PersianCharacters.HEH_VARIANTS:
            return 'heh'
        elif char in PersianCharacters.WAW_VARIANTS:
            return 'waw'
        elif char in PersianCharacters.HAMZA_VARIANTS:
            return 'hamza'
        return None
