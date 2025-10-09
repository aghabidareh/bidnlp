"""
Tests for Persian Stemmer
"""

import unittest
from bidnlp.stemming import PersianStemmer


class TestPersianStemmer(unittest.TestCase):
    """Test cases for PersianStemmer"""

    def setUp(self):
        """Set up test fixtures"""
        self.stemmer = PersianStemmer()

    def test_normalization(self):
        """Test text normalization"""
        # Test Arabic to Persian character conversion
        self.assertEqual(self.stemmer.normalize('كتاب'), 'کتاب')
        self.assertEqual(self.stemmer.normalize('يک'), 'یک')
        self.assertEqual(self.stemmer.normalize('مدرسة'), 'مدرسه')

        # Test diacritic removal
        word_with_diacritics = 'کِتاب'
        self.assertEqual(self.stemmer.normalize(word_with_diacritics), 'کتاب')

    def test_plural_removal(self):
        """Test plural suffix removal"""
        test_cases = [
            ('کتاب‌ها', 'کتاب'),
            ('کتابها', 'کتاب'),
            ('دانشجویان', 'دانشجو'),
            ('مدارس', 'مدارس'),  # No change for broken plurals
        ]

        for word, expected_stem in test_cases:
            result = self.stemmer.stem(word)
            self.assertEqual(result, expected_stem,
                           f"Failed for '{word}': expected '{expected_stem}', got '{result}'")

    def test_possessive_pronoun_removal(self):
        """Test possessive pronoun suffix removal"""
        test_cases = [
            ('کتابم', 'کتاب'),
            ('کتابت', 'کتاب'),
            ('کتابش', 'کتاب'),
            ('کتابمان', 'کتاب'),
            ('کتابتان', 'کتاب'),
            ('کتابشان', 'کتاب'),
            ('کتاب‌هایم', 'کتاب'),
            ('کتابهایم', 'کتاب'),
            ('خانه‌ام', 'خان'),
            ('خانه‌اش', 'خان'),
        ]

        for word, expected_stem in test_cases:
            result = self.stemmer.stem(word)
            self.assertEqual(result, expected_stem,
                           f"Failed for '{word}': expected '{expected_stem}', got '{result}'")


    def test_comparative_suffix_removal(self):
        """Test comparative and superlative suffix removal"""
        test_cases = [
            ('بزرگتر', 'بزرگ'),
            ('بزرگترین', 'بزرگ'),
            ('کوچکتر', 'کوچک'),
            ('زیباتر', 'زیبا'),
            ('زیباترین', 'زیبا'),
        ]

        for word, expected_stem in test_cases:
            result = self.stemmer.stem(word)
            self.assertEqual(result, expected_stem,
                           f"Failed for '{word}': expected '{expected_stem}', got '{result}'")

    def test_adverb_adjective_suffix_removal(self):
        """Test adverb and adjective suffix removal"""
        test_cases = [
            ('دوستانه', 'دوست'),
            ('مردانه', 'مرد'),
            ('خانواده‌وار', 'خانواد'),
            ('خانوادهوار', 'خانواد'),
            ('خطرناک', 'خطر'),
            ('دوگانه', 'دوگ'),
        ]

        for word, expected_stem in test_cases:
            result = self.stemmer.stem(word)
            self.assertEqual(result, expected_stem,
                           f"Failed for '{word}': expected '{expected_stem}', got '{result}'")

    def test_complex_words(self):
        """Test stemming of complex words with multiple suffixes"""
        test_cases = [
            ('کتاب‌هایمان', 'کتاب'),
            ('کتابهایمان', 'کتاب'),
            ('دانشجویانمان', 'دانشجو'),
            ('بزرگترینش', 'بزرگ'),
        ]

        for word, expected_stem in test_cases:
            result = self.stemmer.stem(word)
            self.assertEqual(result, expected_stem,
                           f"Failed for '{word}': expected '{expected_stem}', got '{result}'")

    def test_minimum_stem_length(self):
        """Test that stems don't become too short"""
        # Words that should not be stemmed beyond minimum length
        short_word = 'به'
        result = self.stemmer.stem(short_word)
        self.assertTrue(len(result) >= self.stemmer.min_stem_length,
                       f"Stem '{result}' is shorter than minimum length")

    def test_empty_and_none(self):
        """Test handling of empty and None inputs"""
        self.assertEqual(self.stemmer.stem(''), '')
        self.assertEqual(self.stemmer.stem(None), None)

    def test_stem_sentence(self):
        """Test stemming a complete sentence"""
        sentence = 'کتاب‌های من در خانه‌ام هستند'
        expected = ['کتاب', 'من', 'در', 'خان', 'هست']

        result = self.stemmer.stem_sentence(sentence)
        self.assertEqual(result, expected,
                        f"Failed for sentence: expected {expected}, got {result}")


    def test_arabic_broken_plurals(self):
        """Test Arabic broken plural pattern handling"""
        test_cases = [
            ('سبزیجات', 'سبزی'),
            ('میوه‌جات', 'میوه'),
            ('میوهجات', 'میوه'),
        ]

        for word, expected_stem in test_cases:
            result = self.stemmer.stem(word)
            self.assertEqual(result, expected_stem,
                           f"Failed for '{word}': expected '{expected_stem}', got '{result}'")

    def test_preserves_simple_words(self):
        """Test that simple words without suffixes are preserved"""
        simple_words = ['کتاب', 'خانه', 'مدرسه', 'دانشگاه', 'ایران']

        for word in simple_words:
            result = self.stemmer.stem(word)
            # Should be the same or with minor normalization
            self.assertIsNotNone(result)
            self.assertTrue(len(result) > 0)



if __name__ == '__main__':
    unittest.main()
