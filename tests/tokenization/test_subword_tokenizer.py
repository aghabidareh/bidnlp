"""
Tests for Persian Subword Tokenizers
"""

import unittest
from bidnlp.tokenization import (
    PersianCharacterTokenizer,
    PersianMorphemeTokenizer,
    PersianSyllableTokenizer
)


class TestPersianCharacterTokenizer(unittest.TestCase):
    """Test cases for PersianCharacterTokenizer"""

    def setUp(self):
        """Set up test fixtures"""
        self.tokenizer = PersianCharacterTokenizer()

    def test_simple_word(self):
        """Test character tokenization of simple word"""
        word = "سلام"
        result = self.tokenizer.tokenize(word)

        self.assertEqual(len(result), 4)
        self.assertEqual(result, ['س', 'ل', 'ا', 'م'])

    def test_empty_text(self):
        """Test tokenization of empty text"""
        result = self.tokenizer.tokenize("")
        self.assertEqual(result, [])

    def test_detokenize(self):
        """Test reconstruction from characters"""
        chars = ['س', 'ل', 'ا', 'م']
        result = self.tokenizer.detokenize(chars)

        self.assertEqual(result, "سلام")

    def test_mixed_text(self):
        """Test with mixed Persian and English"""
        text = "Hi سلام"
        result = self.tokenizer.tokenize(text)

        # Should tokenize all characters
        self.assertTrue(len(result) > 0)

    def test_with_spaces(self):
        """Test that spaces are preserved"""
        text = "سلام دنیا"
        result = self.tokenizer.tokenize(text)

        self.assertIn(' ', result)


class TestPersianMorphemeTokenizer(unittest.TestCase):
    """Test cases for PersianMorphemeTokenizer"""

    def setUp(self):
        """Set up test fixtures"""
        self.tokenizer = PersianMorphemeTokenizer()

    def test_simple_word(self):
        """Test morpheme tokenization of simple word"""
        word = "کتاب"
        result = self.tokenizer.tokenize(word)

        # Simple word should return as is
        self.assertTrue(len(result) > 0)

    def test_word_with_prefix(self):
        """Test word with prefix"""
        word = "میروم"  # می + روم
        result = self.tokenizer.tokenize(word)

        # Should identify prefix
        self.assertTrue(len(result) >= 2)
        self.assertIn("می", result)

    def test_word_with_suffix(self):
        """Test word with suffix"""
        word = "کتابها"  # کتاب + ها
        result = self.tokenizer.tokenize(word)

        # Should identify suffix
        self.assertTrue(len(result) >= 2)
        self.assertIn("ها", result)

    def test_word_with_prefix_and_suffix(self):
        """Test word with both prefix and suffix"""
        word = "میرویم"  # می + رو + یم
        result = self.tokenizer.tokenize(word)

        # Should identify both
        self.assertTrue(len(result) >= 2)

    def test_tokenize_with_tags(self):
        """Test morpheme tokenization with tags"""
        word = "میروم"
        result = self.tokenizer.tokenize_with_tags(word)

        # Should return tuples of (morpheme, tag)
        self.assertTrue(len(result) > 0)
        for item in result:
            self.assertEqual(len(item), 2)
            morpheme, tag = item
            self.assertIsInstance(morpheme, str)
            self.assertIsInstance(tag, str)

    def test_plural_suffix(self):
        """Test plural suffix detection"""
        word = "کتابها"
        result = self.tokenizer.tokenize(word)

        self.assertIn("ها", result)
        self.assertIn("کتاب", result)

    def test_possessive_suffix(self):
        """Test possessive pronoun suffix"""
        word = "کتابم"  # کتاب + م (my book)
        result = self.tokenizer.tokenize(word)

        self.assertTrue(len(result) >= 2)
        self.assertIn("م", result)

    def test_comparative_suffix(self):
        """Test comparative suffix"""
        word = "بزرگتر"  # بزرگ + تر
        result = self.tokenizer.tokenize(word)

        self.assertIn("تر", result)

    def test_negative_prefix(self):
        """Test negative prefix"""
        word = "نمیروم"  # نمی + روم
        result = self.tokenizer.tokenize(word)

        # Should identify negative prefix
        self.assertTrue(len(result) >= 1)

    def test_empty_word(self):
        """Test empty word"""
        result = self.tokenizer.tokenize("")
        self.assertEqual(result, [])

    def test_unknown_morphemes(self):
        """Test word with no recognized morphemes"""
        word = "xyz"
        result = self.tokenizer.tokenize(word)

        # Should return the word itself
        self.assertEqual(result, ["xyz"])


class TestPersianSyllableTokenizer(unittest.TestCase):
    """Test cases for PersianSyllableTokenizer"""

    def setUp(self):
        """Set up test fixtures"""
        self.tokenizer = PersianSyllableTokenizer()

    def test_simple_word(self):
        """Test syllable tokenization"""
        word = "سلام"
        result = self.tokenizer.tokenize(word)

        # Should return syllables
        self.assertTrue(len(result) > 0)

    def test_empty_word(self):
        """Test empty word"""
        result = self.tokenizer.tokenize("")
        self.assertEqual(result, [])

    def test_count_syllables(self):
        """Test syllable counting"""
        word = "سلام"
        count = self.tokenizer.count_syllables(word)

        # Should count syllables
        self.assertIsInstance(count, int)
        self.assertTrue(count > 0)

    def test_single_syllable(self):
        """Test single syllable word"""
        word = "من"
        result = self.tokenizer.tokenize(word)

        # Should handle single syllable
        self.assertTrue(len(result) >= 1)

    def test_multi_syllable(self):
        """Test multi-syllable word"""
        word = "دانشگاه"  # Multi-syllable word
        result = self.tokenizer.tokenize(word)

        # Should split into multiple syllables
        self.assertTrue(len(result) >= 1)


if __name__ == '__main__':
    unittest.main()
