"""
Tests for Persian text statistics
"""

import pytest
from bidnlp.utils import PersianTextStatistics


class TestPersianTextStatistics:
    """Test cases for PersianTextStatistics class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.stats = PersianTextStatistics()

    def test_character_count(self):
        """Test character counting."""
        text = "سلام دنیا"
        assert self.stats.character_count(text, include_spaces=True) == 9
        assert self.stats.character_count(text, include_spaces=False) == 8

    def test_word_count(self):
        """Test word counting."""
        text = "سلام دنیا چطوری"
        assert self.stats.word_count(text) == 3

        text_with_extra_spaces = "سلام  دنیا   چطوری"
        assert self.stats.word_count(text_with_extra_spaces) == 3

    def test_sentence_count(self):
        """Test sentence counting."""
        text = "سلام. چطوری؟ خوبم!"
        assert self.stats.sentence_count(text) == 3

        text_persian = "این جمله اول است. این جمله دوم است؟"
        assert self.stats.sentence_count(text_persian) == 2

    def test_line_count(self):
        """Test line counting."""
        text = "خط اول\nخط دوم\nخط سوم"
        assert self.stats.line_count(text) == 3

    def test_paragraph_count(self):
        """Test paragraph counting."""
        text = "پاراگراف اول\n\nپاراگراف دوم\n\nپاراگراف سوم"
        assert self.stats.paragraph_count(text) == 3

    def test_persian_character_count(self):
        """Test Persian character counting."""
        text = "سلام hello"
        assert self.stats.persian_character_count(text) == 4  # س ل ا م

    def test_arabic_character_count(self):
        """Test Arabic character counting."""
        text = "سلام كتاب"  # ك is Arabic kaf
        assert self.stats.arabic_character_count(text) == 1

    def test_digit_count(self):
        """Test digit counting."""
        text = "۱۲۳ ٤٥ 67"
        assert self.stats.digit_count(text) == 7

    def test_average_word_length(self):
        """Test average word length calculation."""
        text = "سلام دنیا"  # 4 chars + 4 chars = 8/2 = 4
        avg = self.stats.average_word_length(text)
        assert avg == 4.0

    def test_average_sentence_length(self):
        """Test average sentence length calculation."""
        text = "یک دو سه. چهار پنج."  # 3 words, 2 words -> 2.5 avg
        avg = self.stats.average_sentence_length(text)
        assert avg == 2.5

    def test_lexical_diversity(self):
        """Test lexical diversity calculation."""
        text = "سلام سلام دنیا"  # 2 unique / 3 total
        diversity = self.stats.lexical_diversity(text)
        assert abs(diversity - 0.6667) < 0.01

    def test_persian_ratio(self):
        """Test Persian character ratio."""
        text = "سلام"  # 4 Persian / 4 total
        ratio = self.stats.persian_ratio(text)
        assert ratio == 1.0

        text_mixed = "سلام hello"  # 4 Persian / 9 total
        ratio = self.stats.persian_ratio(text_mixed)
        assert abs(ratio - 0.444) < 0.01

    def test_get_statistics(self):
        """Test comprehensive statistics."""
        text = "سلام دنیا. چطوری؟"
        stats = self.stats.get_statistics(text)

        assert stats['words'] == 3
        assert stats['sentences'] == 2
        assert stats['persian_characters'] > 0
        assert 'average_word_length' in stats
        assert 'lexical_diversity' in stats

    def test_word_frequency(self):
        """Test word frequency distribution."""
        text = "سلام سلام دنیا سلام"
        freq = self.stats.word_frequency(text)

        assert freq[0] == ('سلام', 3)
        assert freq[1] == ('دنیا', 1)

    def test_word_frequency_top_n(self):
        """Test word frequency with top_n limit."""
        text = "سلام دنیا سلام چطوری سلام"
        freq = self.stats.word_frequency(text, top_n=2)

        assert len(freq) == 2
        assert freq[0][0] == 'سلام'

    def test_character_frequency(self):
        """Test character frequency distribution."""
        text = "ااابب"
        freq = self.stats.character_frequency(text)

        assert freq[0] == ('ا', 3)
        assert freq[1] == ('ب', 2)

    def test_longest_word(self):
        """Test finding longest word."""
        text = "یک دو سلام"
        longest = self.stats.longest_word(text)
        assert longest == "سلام"

    def test_shortest_word(self):
        """Test finding shortest word."""
        text = "یک دو سلام"
        shortest = self.stats.shortest_word(text)
        assert shortest in ["یک", "دو"]

    def test_get_ngrams(self):
        """Test n-gram generation."""
        text = "یک دو سه"
        bigrams = self.stats.get_ngrams(text, n=2)

        assert len(bigrams) == 2
        assert ('یک', 'دو') in bigrams
        assert ('دو', 'سه') in bigrams

    def test_ngram_frequency(self):
        """Test n-gram frequency distribution."""
        text = "یک دو یک دو سه"
        freq = self.stats.ngram_frequency(text, n=2)

        assert freq[0] == (('یک', 'دو'), 2)

    def test_empty_text(self):
        """Test edge cases with empty text."""
        assert self.stats.word_count("") == 0
        assert self.stats.sentence_count("") == 0
        assert self.stats.average_word_length("") == 0.0
        assert self.stats.lexical_diversity("") == 0.0

    def test_text_with_only_spaces(self):
        """Test text with only whitespace."""
        text = "   "
        assert self.stats.word_count(text) == 0
        assert self.stats.character_count(text, include_spaces=False) == 0

    def test_single_word(self):
        """Test statistics on single word."""
        text = "سلام"
        assert self.stats.word_count(text) == 1
        assert self.stats.lexical_diversity(text) == 1.0

    def test_punctuation_count(self):
        """Test punctuation counting."""
        text = "سلام، چطوری؟ خوبم!"
        count = self.stats.punctuation_count(text)
        assert count == 3  # ، ؟ !

    def test_mixed_language_statistics(self):
        """Test statistics on mixed language text."""
        text = "سلام hello دنیا world"
        stats = self.stats.get_statistics(text)

        assert stats['words'] == 4
        assert stats['persian_characters'] > 0
        assert stats['persian_ratio'] < 1.0
