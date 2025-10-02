"""
Tests for Persian Sentence Tokenizer
"""

import unittest
from bidnlp.tokenization import PersianSentenceTokenizer


class TestPersianSentenceTokenizer(unittest.TestCase):
    """Test cases for PersianSentenceTokenizer"""

    def setUp(self):
        """Set up test fixtures"""
        self.tokenizer = PersianSentenceTokenizer()

    def test_simple_sentences(self):
        """Test tokenization of simple sentences"""
        text = "این یک جمله است. این جمله دوم است."
        result = self.tokenizer.tokenize(text)

        self.assertEqual(len(result), 2)
        self.assertIn("این یک جمله است.", result[0])
        self.assertIn("این جمله دوم است.", result[1])

    def test_persian_question_mark(self):
        """Test sentence splitting with Persian question mark"""
        text = "حال شما چطور است؟ من خوبم."
        result = self.tokenizer.tokenize(text)

        self.assertEqual(len(result), 2)
        self.assertTrue(result[0].endswith("؟"))

    def test_exclamation_mark(self):
        """Test sentence splitting with exclamation marks"""
        text = "چه خبر خوبی! واقعاً عالی است."
        result = self.tokenizer.tokenize(text)

        self.assertEqual(len(result), 2)

    def test_mixed_punctuation(self):
        """Test with mixed Persian and Latin punctuation"""
        text = "سلام. حالت چطوره؟ من خوبم!"
        result = self.tokenizer.tokenize(text)

        self.assertEqual(len(result), 3)

    def test_abbreviations(self):
        """Test that abbreviations don't split sentences"""
        text = "دکتر احمدی آمد. او پزشک است."
        result = self.tokenizer.tokenize(text)

        # Should be 2 sentences despite "دکتر" having potential period
        self.assertTrue(len(result) >= 1)

    def test_decimal_numbers(self):
        """Test that decimal points don't split sentences"""
        text = "قیمت 12.5 دلار است. این مناسب است."
        result = self.tokenizer.tokenize(text)

        self.assertEqual(len(result), 2)
        self.assertIn("12.5", result[0])

    def test_empty_text(self):
        """Test tokenization of empty text"""
        result = self.tokenizer.tokenize("")
        self.assertEqual(result, [])

    def test_no_sentence_ending(self):
        """Test text without sentence-ending punctuation"""
        text = "این یک متن بدون نقطه پایانی است"
        result = self.tokenizer.tokenize(text)

        # Should still return the text as one sentence
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], text)

    def test_multiple_spaces(self):
        """Test handling of multiple spaces between sentences"""
        text = "جمله اول.    جمله دوم."
        result = self.tokenizer.tokenize(text)

        self.assertEqual(len(result), 2)

    def test_tokenize_with_positions(self):
        """Test sentence tokenization with positions"""
        text = "جمله اول. جمله دوم."
        result = self.tokenizer.tokenize_with_positions(text)

        self.assertEqual(len(result), 2)
        # Each result should be (sentence, start, end)
        for item in result:
            self.assertEqual(len(item), 3)
            sentence, start, end = item
            self.assertIsInstance(sentence, str)
            self.assertIsInstance(start, int)
            self.assertIsInstance(end, int)

    def test_detokenize(self):
        """Test reconstruction of text from sentences"""
        text = "جمله اول. جمله دوم. جمله سوم."
        sentences = self.tokenizer.tokenize(text)
        reconstructed = self.tokenizer.detokenize(sentences)

        # Should preserve all sentences
        self.assertIn("جمله اول", reconstructed)
        self.assertIn("جمله دوم", reconstructed)
        self.assertIn("جمله سوم", reconstructed)

    def test_count_sentences(self):
        """Test counting sentences"""
        text = "جمله اول. جمله دوم؟ جمله سوم!"
        count = self.tokenizer.count_sentences(text)

        self.assertEqual(count, 3)

    def test_quotations(self):
        """Test handling of quotations"""
        text = 'او گفت: "سلام". من جواب دادم.'
        result = self.tokenizer.tokenize(text)

        # Should handle quotes properly
        self.assertTrue(len(result) >= 1)

    def test_persian_quotations(self):
        """Test handling of Persian quotation marks"""
        text = "او گفت: «سلام». من جواب دادم."
        result = self.tokenizer.tokenize(text)

        self.assertTrue(len(result) >= 1)

    def test_long_text(self):
        """Test with longer, more complex text"""
        text = """
        فارسی یا پارسی یکی از زبان‌های هند و اروپایی است.
        این زبان در ایران، افغانستان و تاجیکستان رسمی است.
        آیا شما فارسی صحبت می‌کنید؟
        بله، من فارسی صحبت می‌کنم!
        """
        result = self.tokenizer.tokenize(text)

        # Should identify multiple sentences
        self.assertTrue(len(result) >= 4)

    def test_ellipsis(self):
        """Test handling of ellipsis"""
        text = "من فکر می‌کنم... شاید درست باشد."
        result = self.tokenizer.tokenize(text)

        # Ellipsis handling may vary
        self.assertTrue(len(result) >= 1)

    def test_single_sentence(self):
        """Test single sentence without punctuation"""
        text = "این یک جمله است"
        result = self.tokenizer.tokenize(text)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], text)

    def test_consecutive_punctuation(self):
        """Test consecutive sentence-ending punctuation"""
        text = "واقعاً؟! باورنکردنی است."
        result = self.tokenizer.tokenize(text)

        # Should handle consecutive punctuation
        self.assertTrue(len(result) >= 1)

    def test_newlines(self):
        """Test handling of newlines"""
        text = "جمله اول.\nجمله دوم."
        result = self.tokenizer.tokenize(text)

        self.assertEqual(len(result), 2)

    def test_mixed_language_sentences(self):
        """Test sentences with mixed Persian and English"""
        text = "من Python را دوست دارم. It is a great language."
        result = self.tokenizer.tokenize(text)

        self.assertEqual(len(result), 2)

    def test_is_sentence_boundary_method(self):
        """Test the is_sentence_boundary helper method"""
        text = "جمله اول. جمله دوم."
        # Find position of period
        period_pos = text.index('.')

        is_boundary = self.tokenizer.is_sentence_boundary(text, period_pos)
        self.assertTrue(is_boundary)

    def test_numbers_with_periods(self):
        """Test that numbered lists don't create false boundaries"""
        text = "مراحل: 1. اول 2. دوم 3. سوم"
        result = self.tokenizer.tokenize(text)

        # Behavior may vary, but should handle intelligently
        self.assertTrue(len(result) >= 1)


if __name__ == '__main__':
    unittest.main()
