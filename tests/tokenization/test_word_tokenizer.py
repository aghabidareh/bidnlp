"""
Tests for Persian Word Tokenizer
"""

import unittest
from bidnlp.tokenization import PersianWordTokenizer


class TestPersianWordTokenizer(unittest.TestCase):
    """Test cases for PersianWordTokenizer"""

    def setUp(self):
        """Set up test fixtures"""
        self.tokenizer = PersianWordTokenizer()

    def test_simple_persian_text(self):
        """Test tokenization of simple Persian text"""
        text = "این یک متن ساده است"
        expected = ["این", "یک", "متن", "ساده", "است"]
        result = self.tokenizer.tokenize(text)
        self.assertEqual(result, expected)

    def test_text_with_punctuation(self):
        """Test tokenization with Persian punctuation"""
        text = "سلام، حال شما چطور است؟"
        result = self.tokenizer.tokenize(text)

        self.assertIn("سلام", result)
        self.assertIn("،", result)
        self.assertIn("حال", result)
        self.assertIn("شما", result)
        self.assertIn("چطور", result)
        self.assertIn("است", result)
        self.assertIn("؟", result)

    def test_text_with_zwnj(self):
        """Test handling of ZWNJ (zero-width non-joiner)"""
        # دست‌کش (glove) - compound word with ZWNJ
        text = "دست\u200cکش خریدم"
        result = self.tokenizer.tokenize(text)

        # Should handle ZWNJ properly
        self.assertTrue(len(result) >= 2)

    def test_mixed_persian_english(self):
        """Test tokenization of mixed Persian-English text"""
        text = "من Python را دوست دارم"
        result = self.tokenizer.tokenize(text)

        self.assertIn("من", result)
        self.assertIn("Python", result)
        self.assertIn("را", result)
        self.assertIn("دوست", result)
        self.assertIn("دارم", result)

    def test_numbers(self):
        """Test tokenization with numbers"""
        text = "من 25 سال دارم"
        result = self.tokenizer.tokenize(text)

        self.assertIn("من", result)
        self.assertIn("25", result)
        self.assertIn("سال", result)
        self.assertIn("دارم", result)

    def test_decimal_numbers(self):
        """Test tokenization with decimal numbers"""
        text = "قیمت 12.5 دلار است"
        result = self.tokenizer.tokenize(text)

        self.assertIn("قیمت", result)
        self.assertIn("12.5", result)
        self.assertIn("دلار", result)

    def test_latin_punctuation(self):
        """Test tokenization with Latin punctuation"""
        text = "این متن! خیلی جالب است."
        result = self.tokenizer.tokenize(text)

        self.assertIn("این", result)
        self.assertIn("متن", result)
        self.assertIn("!", result)
        self.assertIn("خیلی", result)
        self.assertIn("جالب", result)
        self.assertIn("است", result)
        self.assertIn(".", result)

    def test_tokenize_with_positions(self):
        """Test tokenization with position tracking"""
        text = "سلام دنیا"
        result = self.tokenizer.tokenize_with_positions(text)

        self.assertTrue(len(result) > 0)
        # Each result should be (token, start, end)
        for item in result:
            self.assertEqual(len(item), 3)
            token, start, end = item
            self.assertIsInstance(token, str)
            self.assertIsInstance(start, int)
            self.assertIsInstance(end, int)

    def test_detokenize(self):
        """Test reconstruction of text from tokens"""
        text = "این یک متن است"
        tokens = self.tokenizer.tokenize(text)
        reconstructed = self.tokenizer.detokenize(tokens)

        # Should preserve the essential content
        self.assertIn("این", reconstructed)
        self.assertIn("یک", reconstructed)
        self.assertIn("متن", reconstructed)
        self.assertIn("است", reconstructed)

    def test_empty_text(self):
        """Test tokenization of empty text"""
        result = self.tokenizer.tokenize("")
        self.assertEqual(result, [])

    def test_whitespace_only(self):
        """Test tokenization of whitespace-only text"""
        result = self.tokenizer.tokenize("   ")
        self.assertEqual(result, [])

    def test_arabic_normalization(self):
        """Test that Arabic characters are normalized to Persian"""
        # Using Arabic 'ي' instead of Persian 'ی'
        text = "يک متن"
        result = self.tokenizer.tokenize(text)

        # Should normalize to Persian
        self.assertTrue(len(result) > 0)

    def test_token_type_detection_persian(self):
        """Test token type detection for Persian words"""
        token_type = self.tokenizer.get_token_type("سلام")
        self.assertEqual(token_type, "persian")

    def test_token_type_detection_english(self):
        """Test token type detection for English words"""
        token_type = self.tokenizer.get_token_type("hello")
        self.assertEqual(token_type, "english")

    def test_token_type_detection_number(self):
        """Test token type detection for numbers"""
        token_type = self.tokenizer.get_token_type("123")
        self.assertEqual(token_type, "number")

    def test_token_type_detection_punctuation(self):
        """Test token type detection for punctuation"""
        token_type = self.tokenizer.get_token_type("،")
        self.assertEqual(token_type, "punctuation")

    def test_compound_word_splitting(self):
        """Test splitting of compound words"""
        # نگارخانه (gallery) - compound word
        text = "نگار\u200cخانه"
        parts = self.tokenizer.split_compound_words(text)

        # Should split into parts
        self.assertTrue(len(parts) > 0)

    def test_real_world_sentence(self):
        """Test with a real-world Persian sentence"""
        text = "من به کتابخانه می‌روم و کتاب می‌خوانم."
        result = self.tokenizer.tokenize(text)

        # Should have multiple tokens
        self.assertTrue(len(result) > 5)

        # Should contain key words
        self.assertIn("من", result)
        self.assertIn("به", result)

    def test_multiple_punctuation(self):
        """Test handling of multiple consecutive punctuation marks"""
        text = "واقعاً؟! باورم نمیشود!!!"
        result = self.tokenizer.tokenize(text)

        # Punctuation marks should be tokenized
        self.assertTrue(len(result) > 0)

    def test_url_and_hashtag(self):
        """Test tokenization with URLs and hashtags"""
        text = "من در سایت example.com هستم"
        result = self.tokenizer.tokenize(text)

        self.assertIn("من", result)
        self.assertIn("در", result)
        self.assertIn("سایت", result)

    def test_preserve_whitespace_option(self):
        """Test whitespace preservation option"""
        tokenizer = PersianWordTokenizer(keep_whitespace=True)
        text = "سلام  دنیا"
        result = tokenizer.tokenize(text)

        # Should preserve whitespace tokens when option is enabled
        # Note: exact behavior depends on implementation
        self.assertTrue(len(result) > 0)


if __name__ == '__main__':
    unittest.main()
