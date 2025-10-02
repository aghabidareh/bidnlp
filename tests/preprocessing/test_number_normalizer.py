"""
Tests for Persian Number Normalizer
"""

import unittest
from bidnlp.preprocessing import PersianNumberNormalizer, PersianDateNormalizer


class TestPersianNumberNormalizer(unittest.TestCase):
    """Test cases for PersianNumberNormalizer"""

    def setUp(self):
        """Set up test fixtures"""
        self.normalizer = PersianNumberNormalizer()

    def test_persian_to_english_digits(self):
        """Test Persian to English digit conversion"""
        text = "۰۱۲۳۴۵۶۷۸۹"
        result = self.normalizer.persian_to_english_digits(text)
        self.assertEqual(result, "0123456789")

    def test_english_to_persian_digits(self):
        """Test English to Persian digit conversion"""
        text = "0123456789"
        result = self.normalizer.english_to_persian_digits(text)
        self.assertEqual(result, "۰۱۲۳۴۵۶۷۸۹")

    def test_arabic_to_persian_digits(self):
        """Test Arabic-Indic to Persian digit conversion"""
        text = "٠١٢٣٤٥٦٧٨٩"
        result = self.normalizer.arabic_to_persian_digits(text)
        self.assertEqual(result, "۰۱۲۳۴۵۶۷۸۹")

    def test_arabic_to_english_digits(self):
        """Test Arabic-Indic to English digit conversion"""
        text = "٠١٢٣٤٥٦٧٨٩"
        result = self.normalizer.arabic_to_english_digits(text)
        self.assertEqual(result, "0123456789")

    def test_normalize_digits_to_english(self):
        """Test normalizing all digits to English"""
        text = "۱۲۳ و ٤٥٦ و 789"
        result = self.normalizer.normalize_digits(text, 'english')

        self.assertIn('123', result)
        self.assertIn('456', result)
        self.assertIn('789', result)
        self.assertNotIn('۱', result)
        self.assertNotIn('٤', result)

    def test_normalize_digits_to_persian(self):
        """Test normalizing all digits to Persian"""
        text = "123 و ٤٥٦"
        result = self.normalizer.normalize_digits(text, 'persian')

        self.assertIn('۱۲۳', result)
        self.assertIn('۴۵۶', result)
        self.assertNotIn('123', result)

    def test_extract_numbers(self):
        """Test number extraction"""
        text = "من ۲۵ سال دارم و 100 کتاب دارم"
        numbers = self.normalizer.extract_numbers(text)

        self.assertIn('25', numbers)
        self.assertIn('100', numbers)

    def test_extract_decimal_numbers(self):
        """Test decimal number extraction"""
        text = "قیمت ۱۲.۵ دلار است"
        numbers = self.normalizer.extract_numbers(text)

        self.assertTrue(any('12.5' in num or '12' in num for num in numbers))

    def test_word_to_number(self):
        """Test Persian word to number conversion"""
        test_cases = [
            ('یک', 1),
            ('دو', 2),
            ('ده', 10),
            ('بیست', 20),
            ('صد', 100),
            ('هزار', 1000),
        ]

        for word, expected in test_cases:
            result = self.normalizer.word_to_number(word)
            self.assertEqual(result, expected)

    def test_number_to_word(self):
        """Test number to Persian word conversion"""
        test_cases = [
            (0, 'صفر'),
            (1, 'یک'),
            (10, 'ده'),
            (20, 'بیست'),
            (100, 'صد'),
        ]

        for number, expected in test_cases:
            result = self.normalizer.number_to_word(number)
            self.assertEqual(result, expected)

    def test_number_to_word_compound(self):
        """Test compound number to word conversion"""
        # 25 = twenty and five
        result = self.normalizer.number_to_word(25)
        self.assertIn('بیست', result)
        self.assertIn('پنج', result)

    def test_convert_words_to_numbers(self):
        """Test converting number words to digits in text"""
        text = "من یک کتاب دارم"
        result = self.normalizer.convert_words_to_numbers(text)

        self.assertIn('1', result)
        self.assertNotIn('یک', result)

    def test_normalize_phone_numbers(self):
        """Test phone number normalization"""
        text = "شماره من ۰۹۱۲۳۴۵۶۷۸۹ است"
        result = self.normalizer.normalize_phone_numbers(text)

        # Should be formatted
        self.assertIn('0912', result)

    def test_normalize_currency(self):
        """Test currency normalization"""
        text = "۱۰۰۰تومان"
        result = self.normalizer.normalize_currency(text, 'تومان')

        # Should have space before currency
        self.assertIn('۱۰۰۰ تومان', result)


class TestPersianDateNormalizer(unittest.TestCase):
    """Test cases for PersianDateNormalizer"""

    def setUp(self):
        """Set up test fixtures"""
        self.normalizer = PersianDateNormalizer()

    def test_month_names(self):
        """Test month name mapping"""
        self.assertEqual(self.normalizer.month_names['فروردین'], 1)
        self.assertEqual(self.normalizer.month_names['اسفند'], 12)

    def test_normalize_date_format(self):
        """Test date format normalization"""
        text = "تاریخ 1400/1/15 است"
        result = self.normalizer.normalize_date_format(text)

        # Should pad with zeros
        self.assertIn('1400/01/15', result)

    def test_normalize_date_with_dashes(self):
        """Test date with dashes"""
        text = "1400-3-7"
        result = self.normalizer.normalize_date_format(text)

        self.assertIn('1400/03/07', result)

    def test_extract_dates(self):
        """Test date extraction"""
        text = "تاریخ‌های 1400/01/01 و 1399/12/29"
        dates = self.normalizer.extract_dates(text)

        self.assertEqual(len(dates), 2)

    def test_two_digit_year(self):
        """Test handling of 2-digit years"""
        text = "تاریخ 00/1/1"
        result = self.normalizer.normalize_date_format(text)

        # Should assume 1300s
        self.assertIn('1300', result)


if __name__ == '__main__':
    unittest.main()
