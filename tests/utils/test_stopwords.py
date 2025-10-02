"""
Tests for Persian stop words
"""

import pytest
from bidnlp.utils import PersianStopWords


class TestPersianStopWords:
    """Test cases for PersianStopWords class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.stopwords = PersianStopWords()

    def test_is_stopword(self):
        """Test stop word detection."""
        assert self.stopwords.is_stopword('از')
        assert self.stopwords.is_stopword('به')
        assert self.stopwords.is_stopword('و')
        assert not self.stopwords.is_stopword('کتاب')
        assert not self.stopwords.is_stopword('دانشگاه')

    def test_remove_stopwords(self):
        """Test stop word removal from text."""
        text = "من به دانشگاه می روم"
        filtered = self.stopwords.remove_stopwords(text)

        # 'من' and 'به' are stop words
        assert 'من' not in filtered
        assert 'به' not in filtered
        assert 'دانشگاه' in filtered

    def test_filter_stopwords(self):
        """Test filtering stop words from word list."""
        words = ['من', 'به', 'دانشگاه', 'می', 'روم']
        filtered = self.stopwords.filter_stopwords(words)

        assert 'دانشگاه' in filtered
        assert 'من' not in filtered
        assert 'به' not in filtered

    def test_add_stopword(self):
        """Test adding custom stop word."""
        self.stopwords.add_stopword('کتاب')
        assert self.stopwords.is_stopword('کتاب')

    def test_add_stopwords(self):
        """Test adding multiple stop words."""
        self.stopwords.add_stopwords(['کتاب', 'مداد'])
        assert self.stopwords.is_stopword('کتاب')
        assert self.stopwords.is_stopword('مداد')

    def test_remove_stopword(self):
        """Test removing a stop word."""
        assert self.stopwords.is_stopword('از')
        self.stopwords.remove_stopword('از')
        assert not self.stopwords.is_stopword('از')

    def test_get_stopwords(self):
        """Test getting stop words set."""
        stopwords_set = self.stopwords.get_stopwords()
        assert isinstance(stopwords_set, set)
        assert 'از' in stopwords_set
        assert 'به' in stopwords_set

    def test_get_stopwords_list(self):
        """Test getting stop words as sorted list."""
        stopwords_list = self.stopwords.get_stopwords_list()
        assert isinstance(stopwords_list, list)
        assert stopwords_list == sorted(stopwords_list)

    def test_count_stopwords(self):
        """Test counting stop words in text."""
        text = "من از دانشگاه به خانه می روم"
        count = self.stopwords.count_stopwords(text)
        assert count >= 3  # من، از، به are stop words

    def test_stopword_ratio(self):
        """Test calculating stop word ratio."""
        text = "من از دانشگاه به خانه می روم"
        ratio = self.stopwords.stopword_ratio(text)
        assert 0.0 <= ratio <= 1.0

    def test_reset_to_defaults(self):
        """Test resetting to default stop words."""
        self.stopwords.add_stopword('custom')
        assert self.stopwords.is_stopword('custom')

        self.stopwords.reset_to_defaults()
        assert not self.stopwords.is_stopword('custom')
        assert self.stopwords.is_stopword('از')

    def test_clear(self):
        """Test clearing all stop words."""
        self.stopwords.clear()
        assert len(self.stopwords.get_stopwords()) == 0
        assert not self.stopwords.is_stopword('از')

    def test_custom_stopwords_only(self):
        """Test using only custom stop words."""
        custom_stops = PersianStopWords(
            custom_stopwords={'کتاب', 'مداد'},
            include_defaults=False
        )

        assert custom_stops.is_stopword('کتاب')
        assert custom_stops.is_stopword('مداد')
        assert not custom_stops.is_stopword('از')  # Default stop word

    def test_custom_with_defaults(self):
        """Test combining custom and default stop words."""
        custom_stops = PersianStopWords(
            custom_stopwords={'کتاب'},
            include_defaults=True
        )

        assert custom_stops.is_stopword('کتاب')  # Custom
        assert custom_stops.is_stopword('از')    # Default

    def test_get_default_stopwords(self):
        """Test getting default stop words (static method)."""
        defaults = PersianStopWords.get_default_stopwords()
        assert isinstance(defaults, set)
        assert 'از' in defaults
        assert 'به' in defaults

    def test_get_default_stopwords_list(self):
        """Test getting default stop words list (static method)."""
        defaults = PersianStopWords.get_default_stopwords_list()
        assert isinstance(defaults, list)
        assert defaults == sorted(defaults)

    def test_common_stopwords_present(self):
        """Test that common Persian stop words are included."""
        common_stopwords = ['از', 'به', 'با', 'در', 'که', 'و', 'است', 'این', 'آن']

        for word in common_stopwords:
            assert self.stopwords.is_stopword(word), f"'{word}' should be a stop word"

    def test_empty_text(self):
        """Test edge cases with empty text."""
        assert self.stopwords.count_stopwords("") == 0
        assert self.stopwords.stopword_ratio("") == 0.0
        assert self.stopwords.remove_stopwords("") == ""

    def test_whitespace_handling(self):
        """Test that whitespace is handled correctly."""
        assert self.stopwords.is_stopword('  از  ')  # Should strip whitespace
        self.stopwords.add_stopword('  تست  ')
        assert self.stopwords.is_stopword('تست')

    def test_text_without_stopwords(self):
        """Test text that contains no stop words."""
        text = "دانشگاه کتابخانه مدرسه"
        count = self.stopwords.count_stopwords(text)
        assert count == 0

    def test_text_only_stopwords(self):
        """Test text containing only stop words."""
        text = "من از به با"
        filtered = self.stopwords.remove_stopwords(text)
        assert filtered.strip() == ""
