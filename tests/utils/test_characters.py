"""
Tests for Persian character utilities
"""

import pytest
from bidnlp.utils import PersianCharacters


class TestPersianCharacters:
    """Test cases for PersianCharacters class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.char_utils = PersianCharacters()

    def test_is_persian(self):
        """Test Persian character detection."""
        assert PersianCharacters.is_persian('ا')
        assert PersianCharacters.is_persian('ب')
        assert PersianCharacters.is_persian('پ')
        assert PersianCharacters.is_persian('ک')
        assert not PersianCharacters.is_persian('a')
        assert not PersianCharacters.is_persian('1')
        assert not PersianCharacters.is_persian('ك')  # Arabic kaf

    def test_is_arabic(self):
        """Test Arabic character detection."""
        assert PersianCharacters.is_arabic('ك')  # Arabic kaf
        assert PersianCharacters.is_arabic('ي')  # Arabic yeh
        assert PersianCharacters.is_arabic('ة')  # Teh marbuta
        assert not PersianCharacters.is_arabic('ک')  # Persian kaf
        assert not PersianCharacters.is_arabic('a')

    def test_is_persian_digit(self):
        """Test Persian digit detection."""
        assert PersianCharacters.is_persian_digit('۰')
        assert PersianCharacters.is_persian_digit('۵')
        assert PersianCharacters.is_persian_digit('۹')
        assert not PersianCharacters.is_persian_digit('0')
        assert not PersianCharacters.is_persian_digit('٥')

    def test_is_arabic_indic_digit(self):
        """Test Arabic-Indic digit detection."""
        assert PersianCharacters.is_arabic_indic_digit('٠')
        assert PersianCharacters.is_arabic_indic_digit('٥')
        assert not PersianCharacters.is_arabic_indic_digit('۵')
        assert not PersianCharacters.is_arabic_indic_digit('5')

    def test_is_digit(self):
        """Test digit detection (all types)."""
        assert PersianCharacters.is_digit('۵')  # Persian
        assert PersianCharacters.is_digit('٥')  # Arabic-Indic
        assert PersianCharacters.is_digit('5')  # English
        assert not PersianCharacters.is_digit('ا')

    def test_is_diacritic(self):
        """Test diacritic detection."""
        assert PersianCharacters.is_diacritic('\u064B')  # Fathatan
        assert PersianCharacters.is_diacritic('\u064E')  # Fatha
        assert not PersianCharacters.is_diacritic('ا')

    def test_is_persian_punctuation(self):
        """Test Persian punctuation detection."""
        assert PersianCharacters.is_persian_punctuation('،')
        assert PersianCharacters.is_persian_punctuation('؛')
        assert PersianCharacters.is_persian_punctuation('؟')
        assert not PersianCharacters.is_persian_punctuation('.')
        assert not PersianCharacters.is_persian_punctuation(',')

    def test_is_zwnj(self):
        """Test ZWNJ detection."""
        assert PersianCharacters.is_zwnj('\u200c')
        assert not PersianCharacters.is_zwnj(' ')
        assert not PersianCharacters.is_zwnj('ا')

    def test_is_kashida(self):
        """Test kashida detection."""
        assert PersianCharacters.is_kashida('\u0640')
        assert not PersianCharacters.is_kashida('-')
        assert not PersianCharacters.is_kashida('ا')

    def test_get_character_type(self):
        """Test character type detection."""
        assert PersianCharacters.get_character_type('ا') == 'persian'
        assert PersianCharacters.get_character_type('ك') == 'arabic'
        assert PersianCharacters.get_character_type('۵') == 'persian_digit'
        assert PersianCharacters.get_character_type('٥') == 'arabic_indic_digit'
        assert PersianCharacters.get_character_type('5') == 'english_digit'
        assert PersianCharacters.get_character_type('،') == 'persian_punctuation'
        assert PersianCharacters.get_character_type('\u200c') == 'zwnj'
        assert PersianCharacters.get_character_type(' ') == 'space'
        assert PersianCharacters.get_character_type('a') == 'other'

    def test_count_character_types(self):
        """Test character type counting."""
        text = "سلام ۱۲۳ hello"
        counts = PersianCharacters.count_character_types(text)

        assert counts['persian'] == 4  # س ل ا م
        assert counts['persian_digit'] == 3  # ۱ ۲ ۳
        assert counts['space'] == 2
        assert counts['other'] == 5  # h e l l o

    def test_remove_diacritics(self):
        """Test diacritic removal."""
        text_with_diacritics = "سَلام"
        text_without = PersianCharacters.remove_diacritics(text_with_diacritics)
        assert text_without == "سلام"

    def test_get_persian_alphabet(self):
        """Test getting Persian alphabet."""
        alphabet = PersianCharacters.get_persian_alphabet()
        assert isinstance(alphabet, set)
        assert 'ا' in alphabet
        assert 'پ' in alphabet
        assert 'ک' in alphabet

    def test_get_persian_consonants(self):
        """Test getting Persian consonants."""
        consonants = PersianCharacters.get_persian_consonants()
        assert 'ب' in consonants
        assert 'پ' in consonants
        assert 'ا' not in consonants  # Vowel
        assert 'و' not in consonants  # Vowel

    def test_get_persian_vowels(self):
        """Test getting Persian vowels."""
        vowels = PersianCharacters.get_persian_vowels()
        assert vowels == {'ا', 'و', 'ی'}

    def test_has_diacritics(self):
        """Test checking for diacritics."""
        assert PersianCharacters.has_diacritics("سَلام")
        assert not PersianCharacters.has_diacritics("سلام")

    def test_has_persian(self):
        """Test checking for Persian characters."""
        assert PersianCharacters.has_persian("سلام")
        assert PersianCharacters.has_persian("hello سلام")
        assert not PersianCharacters.has_persian("hello")

    def test_has_arabic(self):
        """Test checking for Arabic characters."""
        assert PersianCharacters.has_arabic("كتاب")  # Arabic kaf
        assert not PersianCharacters.has_arabic("کتاب")  # Persian kaf

    def test_is_persian_text(self):
        """Test Persian text detection."""
        assert PersianCharacters.is_persian_text("سلام دنیا", threshold=0.5)
        assert not PersianCharacters.is_persian_text("hello world", threshold=0.5)
        assert PersianCharacters.is_persian_text("سلام hello", threshold=0.3)

    def test_get_variant_group(self):
        """Test variant group detection."""
        assert PersianCharacters.get_variant_group('ی') == 'yeh'
        assert PersianCharacters.get_variant_group('ي') == 'yeh'
        assert PersianCharacters.get_variant_group('ک') == 'kaf'
        assert PersianCharacters.get_variant_group('ك') == 'kaf'
        assert PersianCharacters.get_variant_group('ا') is None

    def test_empty_and_none(self):
        """Test edge cases with empty/None inputs."""
        assert not PersianCharacters.is_persian_text("")
        assert not PersianCharacters.has_persian("")
        assert not PersianCharacters.has_diacritics("")

    def test_mixed_text(self):
        """Test mixed Persian/English text."""
        text = "سلام Hello ۱۲۳"
        counts = PersianCharacters.count_character_types(text)

        assert counts['persian'] > 0
        assert counts['persian_digit'] == 3
        assert counts['other'] > 0  # English letters
