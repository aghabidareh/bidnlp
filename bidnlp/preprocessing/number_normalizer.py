"""
Persian Number and Date Normalizer

Handles conversion and normalization of numbers and dates including:
- Persian to English digits conversion
- English to Persian digits conversion
- Number word to digit conversion
- Date format normalization
- Ordinal number handling
"""

import re
from typing import Optional, Dict


class PersianNumberNormalizer:
    """
    Number normalizer for Persian (Farsi) text.

    Handles conversion between different number formats.
    """

    def __init__(self):
        """Initialize the number normalizer."""

        # Digit mappings
        self.persian_digits = '۰۱۲۳۴۵۶۷۸۹'
        self.arabic_digits = '٠١٢٣٤٥٦٧٨٩'
        self.english_digits = '0123456789'

        # Persian to English
        self.persian_to_english = str.maketrans(self.persian_digits, self.english_digits)

        # English to Persian
        self.english_to_persian = str.maketrans(self.english_digits, self.persian_digits)

        # Arabic to Persian
        self.arabic_to_persian_nums = str.maketrans(self.arabic_digits, self.persian_digits)

        # Arabic to English
        self.arabic_to_english = str.maketrans(self.arabic_digits, self.english_digits)

        # Persian number words (0-10)
        self.number_words = {
            'صفر': 0,
            'یک': 1,
            'دو': 2,
            'سه': 3,
            'چهار': 4,
            'پنج': 5,
            'شش': 6,
            'هفت': 7,
            'هشت': 8,
            'نه': 9,
            'ده': 10,
            'یازده': 11,
            'دوازده': 12,
            'سیزده': 13,
            'چهارده': 14,
            'پانزده': 15,
            'شانزده': 16,
            'هفده': 17,
            'هجده': 18,
            'نوزده': 19,
            'بیست': 20,
            'سی': 30,
            'چهل': 40,
            'پنجاه': 50,
            'شصت': 60,
            'هفتاد': 70,
            'هشتاد': 80,
            'نود': 90,
            'صد': 100,
            'یکصد': 100,
            'دویست': 200,
            'سیصد': 300,
            'چهارصد': 400,
            'پانصد': 500,
            'ششصد': 600,
            'هفتصد': 700,
            'هشتصد': 800,
            'نهصد': 900,
            'هزار': 1000,
            'میلیون': 1000000,
            'میلیارد': 1000000000,
        }

        # Reverse mapping (digit to word)
        self.digit_to_word = {
            0: 'صفر',
            1: 'یک',
            2: 'دو',
            3: 'سه',
            4: 'چهار',
            5: 'پنج',
            6: 'شش',
            7: 'هفت',
            8: 'هشت',
            9: 'نه',
            10: 'ده',
            11: 'یازده',
            12: 'دوازده',
            13: 'سیزده',
            14: 'چهارده',
            15: 'پانزده',
            16: 'شانزده',
            17: 'هفده',
            18: 'هجده',
            19: 'نوزده',
            20: 'بیست',
            30: 'سی',
            40: 'چهل',
            50: 'پنجاه',
            60: 'شصت',
            70: 'هفتاد',
            80: 'هشتاد',
            90: 'نود',
            100: 'صد',
            200: 'دویست',
            300: 'سیصد',
            400: 'چهارصد',
            500: 'پانصد',
            600: 'ششصد',
            700: 'هفتصد',
            800: 'هشتصد',
            900: 'نهصد',
        }

    def persian_to_english_digits(self, text: str) -> str:
        """Convert Persian digits to English digits"""
        return text.translate(self.persian_to_english)

    def english_to_persian_digits(self, text: str) -> str:
        """Convert English digits to Persian digits"""
        return text.translate(self.english_to_persian)

    def arabic_to_persian_digits(self, text: str) -> str:
        """Convert Arabic-Indic digits to Persian digits"""
        return text.translate(self.arabic_to_persian_nums)

    def arabic_to_english_digits(self, text: str) -> str:
        """Convert Arabic-Indic digits to English digits"""
        return text.translate(self.arabic_to_english)

    def normalize_digits(self, text: str, target: str = 'english') -> str:
        """
        Normalize all digits to target format.

        Args:
            text: Input text
            target: Target format ('english' or 'persian')

        Returns:
            Text with normalized digits
        """
        if target == 'english':
            # Convert both Persian and Arabic digits to English
            text = self.persian_to_english_digits(text)
            text = self.arabic_to_english_digits(text)
        elif target == 'persian':
            # Convert both English and Arabic digits to Persian
            text = self.english_to_persian_digits(text)
            text = self.arabic_to_persian_digits(text)

        return text

    def extract_numbers(self, text: str) -> list:
        """
        Extract all numbers from text.

        Returns:
            List of numbers found in text
        """
        # Normalize to English first
        normalized = self.normalize_digits(text, 'english')

        # Find all numbers (including decimals)
        numbers = re.findall(r'\d+(?:\.\d+)?', normalized)

        return numbers

    def word_to_number(self, word: str) -> Optional[int]:
        """
        Convert Persian number word to digit.

        Args:
            word: Persian number word

        Returns:
            Integer value or None if not found
        """
        return self.number_words.get(word)

    def number_to_word(self, number: int) -> str:
        """
        Convert number to Persian word (limited support).

        Args:
            number: Integer to convert

        Returns:
            Persian word representation
        """
        if number in self.digit_to_word:
            return self.digit_to_word[number]

        # Handle compound numbers (21-99)
        if 20 < number < 100:
            tens = (number // 10) * 10
            ones = number % 10
            if tens in self.digit_to_word and ones in self.digit_to_word:
                return f"{self.digit_to_word[tens]} و {self.digit_to_word[ones]}"

        # Handle hundreds
        if 100 < number < 1000:
            hundreds = (number // 100) * 100
            remainder = number % 100

            result = self.digit_to_word.get(hundreds, '')

            if remainder > 0:
                if remainder in self.digit_to_word:
                    result += f" و {self.digit_to_word[remainder]}"
                else:
                    # Recursive call for compound remainder
                    result += f" و {self.number_to_word(remainder)}"

            return result

        return str(number)  # Fallback to digit

    def convert_words_to_numbers(self, text: str) -> str:
        """
        Convert Persian number words to digits in text.

        Args:
            text: Input text with number words

        Returns:
            Text with number words converted to digits
        """
        # Sort by length to match longer phrases first
        sorted_words = sorted(self.number_words.keys(), key=len, reverse=True)

        for word in sorted_words:
            if word in text:
                text = text.replace(word, str(self.number_words[word]))

        return text

    def normalize_phone_numbers(self, text: str, format_style: str = 'standard') -> str:
        """
        Normalize Persian phone numbers.

        Args:
            text: Input text
            format_style: 'standard' or 'compact'

        Returns:
            Text with normalized phone numbers
        """
        # Normalize digits first
        text = self.normalize_digits(text, 'english')

        # Pattern for Iranian mobile numbers (09XX-XXX-XXXX)
        mobile_pattern = r'0?9\d{9}'

        def format_mobile(match):
            number = match.group(0)
            if len(number) == 10:
                number = '0' + number
            if format_style == 'standard':
                return f"{number[:4]}-{number[4:7]}-{number[7:]}"
            return number

        text = re.sub(mobile_pattern, format_mobile, text)

        return text

    def normalize_currency(self, text: str, currency: str = 'تومان') -> str:
        """
        Normalize currency mentions.

        Args:
            text: Input text
            currency: Currency unit (تومان، ریال)

        Returns:
            Text with normalized currency
        """
        # Normalize digits
        text = self.normalize_digits(text, 'persian')

        # Add space before currency if missing
        text = re.sub(f'([۰-۹])({currency})', r'\1 \2', text)

        return text


class PersianDateNormalizer:
    """
    Date normalizer for Persian (Jalali/Shamsi) calendar.
    """

    def __init__(self):
        """Initialize the date normalizer."""

        # Persian month names
        self.month_names = {
            'فروردین': 1,
            'اردیبهشت': 2,
            'خرداد': 3,
            'تیر': 4,
            'مرداد': 5,
            'شهریور': 6,
            'مهر': 7,
            'آبان': 8,
            'آذر': 9,
            'دی': 10,
            'بهمن': 11,
            'اسفند': 12,
        }

        # Reverse mapping
        self.month_numbers = {v: k for k, v in self.month_names.items()}

    def normalize_date_format(self, text: str) -> str:
        """
        Normalize Persian date formats.

        Converts various date formats to standard YYYY/MM/DD.

        Args:
            text: Input text

        Returns:
            Text with normalized dates
        """
        # Pattern for XX/XX/XXXX or XX-XX-XXXX
        date_pattern = r'(\d{2,4})[-/](\d{1,2})[-/](\d{1,2})'

        def normalize_date(match):
            year, month, day = match.groups()

            # Pad with zeros
            month = month.zfill(2)
            day = day.zfill(2)

            # Handle 2-digit years
            if len(year) == 2:
                year = '13' + year  # Assume 1300s for Persian calendar

            return f"{year}/{month}/{day}"

        text = re.sub(date_pattern, normalize_date, text)

        return text

    def extract_dates(self, text: str) -> list:
        """Extract all dates from text"""
        date_pattern = r'\d{2,4}[-/]\d{1,2}[-/]\d{1,2}'
        return re.findall(date_pattern, text)
