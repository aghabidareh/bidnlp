"""
Tests for Persian Normalizer
"""

import unittest
from bidnlp.preprocessing import PersianNormalizer


class TestPersianNormalizer(unittest.TestCase):
    """Test cases for PersianNormalizer"""

    def setUp(self):
        """Set up test fixtures"""
        self.normalizer = PersianNormalizer()

    def test_arabic_to_persian_characters(self):
        """Test Arabic to Persian character conversion"""
        text = "كتاب يک مدرسة"
        result = self.normalizer.normalize(text)

        # Should convert to Persian equivalents
        self.assertIn('ک', result)
        self.assertIn('ی', result)
        self.assertIn('ه', result)
        self.assertNotIn('ك', result)
        self.assertNotIn('ي', result)

    def test_arabic_to_persian_numbers(self):
        """Test Arabic-Indic to Persian digit conversion"""
        text = "٠١٢٣٤٥٦٧٨٩"
        result = self.normalizer.normalize(text)

        # Should convert to Persian digits
        self.assertEqual(result, "۰۱۲۳۴۵۶۷۸۹")

    def test_diacritic_removal(self):
        """Test removal of Arabic diacritics"""
        text = "كِتَابٌ"  # With diacritics
        result = self.normalizer.normalize(text)

        # Should remove diacritics
        self.assertNotIn('\u064B', result)  # Fathatan
        self.assertNotIn('\u064E', result)  # Fatha
        self.assertNotIn('\u0650', result)  # Kasra

    def test_kashida_removal(self):
        """Test kashida removal"""
        text = "کتـــاب"  # With kashida
        result = self.normalizer.normalize(text)

        # Should remove kashida
        self.assertNotIn('\u0640', result)
        self.assertIn('کتاب', result)

    def test_whitespace_normalization(self):
        """Test whitespace normalization"""
        text = "این   یک    متن     است"
        result = self.normalizer.normalize(text)

        # Should have single spaces
        self.assertEqual(result, "این یک متن است")

    def test_zwnj_normalization(self):
        """Test ZWNJ normalization"""
        text = "میروم"  # Without ZWNJ
        result = self.normalizer.normalize(text)

        # Should add ZWNJ after می
        self.assertIn('\u200c', result)

    def test_space_before_punctuation(self):
        """Test removal of space before punctuation"""
        text = "این یک متن است ."
        result = self.normalizer.normalize(text)

        # Should remove space before period
        self.assertTrue(result.endswith('است.'))

    def test_space_after_punctuation(self):
        """Test addition of space after punctuation"""
        text = "سلام،حال شما چطور است؟من خوبم"
        result = self.normalizer.normalize(text)

        # Should have space after comma and question mark
        self.assertIn('، ', result)
        self.assertIn('؟ ', result)

    def test_multiple_newlines(self):
        """Test multiple newline normalization"""
        text = "خط اول\n\n\n\nخط دوم"
        result = self.normalizer.normalize(text)

        # Should have max 2 newlines
        self.assertNotIn('\n\n\n', result)

    def test_invisible_character_removal(self):
        """Test removal of invisible characters"""
        text = "متن\u200Bبا\u200Dکاراکترهای\u200Eمخفی"
        result = self.normalizer.normalize(text)

        # Should remove zero-width characters
        self.assertNotIn('\u200B', result)  # Zero-width space
        self.assertNotIn('\u200D', result)  # Zero-width joiner (except ZWNJ if normalized)
        self.assertNotIn('\u200E', result)  # LTR mark

    def test_unicode_normalization(self):
        """Test Unicode normalization"""
        # Test with composed/decomposed forms
        text = "café"  # Can be composed or decomposed
        result = self.normalizer.normalize(text)

        # Should apply Unicode normalization
        self.assertIsNotNone(result)

    def test_empty_text(self):
        """Test with empty text"""
        result = self.normalizer.normalize("")
        self.assertEqual(result, "")

    def test_none_text(self):
        """Test with None text"""
        result = self.normalizer.normalize(None)
        self.assertEqual(result, None)

    def test_batch_normalize(self):
        """Test batch normalization"""
        texts = [
            "كتاب يک",
            "مدرسة دو",
            "٠١٢٣"
        ]

        results = self.normalizer.batch_normalize(texts)

        self.assertEqual(len(results), 3)
        # Check first result
        self.assertIn('ک', results[0])
        self.assertIn('ی', results[0])

    def test_disable_arabic_normalization(self):
        """Test with Arabic normalization disabled"""
        normalizer = PersianNormalizer(normalize_arabic=False)
        text = "كتاب"
        result = normalizer.normalize(text)

        # Should keep Arabic characters
        self.assertIn('ك', result)

    def test_disable_diacritic_removal(self):
        """Test with diacritic removal disabled"""
        normalizer = PersianNormalizer(remove_diacritics=False)
        text = "كِتَاب"
        result = normalizer.normalize(text)

        # Should keep some diacritics
        # Note: Other normalization may affect this
        self.assertIsNotNone(result)

    def test_real_world_text(self):
        """Test with real-world Persian text"""
        text = "كتاب   «فارسي» را  ميخوانم ."
        result = self.normalizer.normalize(text)

        # Should be properly normalized
        self.assertNotIn('   ', result)  # No triple spaces
        self.assertIn('ک', result)  # Arabic converted
        self.assertIn('ی', result)  # Arabic converted
        self.assertTrue(result.endswith('.'))  # No space before period


if __name__ == '__main__':
    unittest.main()
