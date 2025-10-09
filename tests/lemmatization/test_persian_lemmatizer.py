"""
Tests for Persian Lemmatizer
"""

import unittest
from bidnlp.lemmatization import PersianLemmatizer


class TestPersianLemmatizer(unittest.TestCase):
    """Test cases for PersianLemmatizer"""

    def setUp(self):
        """Set up test fixtures"""
        self.lemmatizer = PersianLemmatizer()

    def test_normalization(self):
        """Test text normalization"""
        # Test Arabic to Persian character conversion
        self.assertEqual(self.lemmatizer.normalize('كتاب'), 'کتاب')
        self.assertEqual(self.lemmatizer.normalize('يک'), 'یک')
        self.assertEqual(self.lemmatizer.normalize('مدرسة'), 'مدرسه')

        # Test ZWNJ removal
        self.assertEqual(self.lemmatizer.normalize('کتاب\u200cها'), 'کتابها')

    def test_irregular_forms_dictionary(self):
        """Test dictionary lookup for irregular forms"""
        test_cases = [
            ('مردم', 'مرد'),
            ('زنان', 'زن'),
            ('کودکان', 'کودک'),
            ('بود', 'بودن'),
            ('است', 'بودن'),
            ('هست', 'بودن'),
            ('بهتر', 'خوب'),
            ('بهترین', 'خوب'),
            ('بدتر', 'بد'),
            ('بیشتر', 'زیاد'),
            ('کمتر', 'کم'),
        ]

        for word, expected_lemma in test_cases:
            result = self.lemmatizer.lemmatize(word)
            self.assertEqual(result, expected_lemma,
                           f"Failed for '{word}': expected '{expected_lemma}', got '{result}'")



    def test_arabic_broken_plurals(self):
        """Test Arabic broken plural pattern handling"""
        test_cases = [
            ('سبزیجات', 'سبزی'),
            ('میوه‌جات', 'میوه'),
            ('میوهجات', 'میوه'),
        ]

        for word, expected_lemma in test_cases:
            result = self.lemmatizer.lemmatize(word)
            self.assertEqual(result, expected_lemma,
                           f"Failed for '{word}': expected '{expected_lemma}', got '{result}'")









    def test_minimum_length_preservation(self):
        """Test that words don't become too short"""
        short_words = ['به', 'از', 'با', 'در']

        for word in short_words:
            result = self.lemmatizer.lemmatize(word)
            self.assertIsNotNone(result)
            self.assertTrue(len(result) > 0,
                          f"Lemma for '{word}' should not be empty")

    def test_empty_and_none(self):
        """Test handling of empty and None inputs"""
        self.assertEqual(self.lemmatizer.lemmatize(''), '')
        self.assertEqual(self.lemmatizer.lemmatize(None), None)

    def test_lemmatize_sentence(self):
        """Test lemmatizing a complete sentence"""
        sentence = 'کتاب‌های من در خانه‌ام هستند'
        result = self.lemmatizer.lemmatize_sentence(sentence)

        # Check that we get a list of the same length
        words = sentence.split()
        self.assertEqual(len(result), len(words))

        # Check specific lemmas
        self.assertIn('کتاب', result)  # From کتاب‌های
        self.assertEqual(result[4], 'بودن')  # هستند -> بودن

    def test_custom_dictionary(self):
        """Test adding custom word-lemma mappings"""
        custom_dict = {
            'خاص': 'خصوصی',
            'عام': 'عمومی'
        }

        lemmatizer = PersianLemmatizer(custom_dictionary=custom_dict)

        self.assertEqual(lemmatizer.lemmatize('خاص'), 'خصوصی')
        self.assertEqual(lemmatizer.lemmatize('عام'), 'عمومی')

    def test_add_lemma_method(self):
        """Test dynamically adding lemmas"""
        self.lemmatizer.add_lemma('تست', 'آزمایش')
        self.assertEqual(self.lemmatizer.lemmatize('تست'), 'آزمایش')

    def test_add_lemmas_method(self):
        """Test adding multiple lemmas at once"""
        lemmas = {
            'کامپیوتر': 'رایانه',
            'موبایل': 'تلفن همراه'
        }

        self.lemmatizer.add_lemmas(lemmas)

        self.assertEqual(self.lemmatizer.lemmatize('کامپیوتر'), 'رایانه')
        self.assertEqual(self.lemmatizer.lemmatize('موبایل'), 'تلفن همراه')


    def test_preserves_simple_nouns(self):
        """Test that simple nouns are preserved"""
        simple_nouns = ['کتاب', 'خانه', 'مدرسه', 'دانشگاه']

        for noun in simple_nouns:
            result = self.lemmatizer.lemmatize(noun)
            # Should remain the same or have minor changes
            self.assertIsNotNone(result)
            self.assertTrue(len(result) > 0)



if __name__ == '__main__':
    unittest.main()
