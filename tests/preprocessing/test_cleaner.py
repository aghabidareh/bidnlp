"""
Tests for Persian Text Cleaner
"""

import unittest
from bidnlp.preprocessing import PersianTextCleaner


class TestPersianTextCleaner(unittest.TestCase):
    """Test cases for PersianTextCleaner"""

    def setUp(self):
        """Set up test fixtures"""
        self.cleaner = PersianTextCleaner()

    def test_url_removal(self):
        """Test URL removal"""
        cleaner = PersianTextCleaner(remove_urls=True)
        text = "این سایت https://example.com خوب است"
        result = cleaner.clean(text)

        self.assertNotIn('https://', result)
        self.assertNotIn('example.com', result)

    def test_url_replacement(self):
        """Test URL replacement"""
        cleaner = PersianTextCleaner(replace_urls_with='<URL>')
        text = "ببینید www.example.com"
        result = cleaner.clean(text)

        self.assertIn('<URL>', result)
        self.assertNotIn('www.example.com', result)

    def test_email_removal(self):
        """Test email removal"""
        cleaner = PersianTextCleaner(remove_emails=True)
        text = "ایمیل من test@example.com است"
        result = cleaner.clean(text)

        self.assertNotIn('test@example.com', result)

    def test_email_replacement(self):
        """Test email replacement"""
        cleaner = PersianTextCleaner(replace_emails_with='<EMAIL>')
        text = "contact@domain.com تماس بگیرید"
        result = cleaner.clean(text)

        self.assertIn('<EMAIL>', result)

    def test_mention_removal(self):
        """Test @ mention removal"""
        cleaner = PersianTextCleaner(remove_mentions=True)
        text = "سلام @کاربر چطوری؟"
        result = cleaner.clean(text)

        self.assertNotIn('@کاربر', result)

    def test_hashtag_removal(self):
        """Test # hashtag removal"""
        cleaner = PersianTextCleaner(remove_hashtags=True)
        text = "#ایران زیباست"
        result = cleaner.clean(text)

        self.assertNotIn('#ایران', result)

    def test_html_removal(self):
        """Test HTML tag removal"""
        text = "<p>این یک <strong>متن</strong> است</p>"
        result = self.cleaner.clean(text)

        self.assertNotIn('<p>', result)
        self.assertNotIn('<strong>', result)
        self.assertIn('این', result)
        self.assertIn('متن', result)

    def test_html_entities(self):
        """Test HTML entity conversion"""
        text = "۱۰&nbsp;&lt;۲۰&gt;&amp;test"
        result = self.cleaner.clean(text)

        # Should convert entities
        self.assertNotIn('&nbsp;', result)
        self.assertNotIn('&lt;', result)
        self.assertNotIn('&gt;', result)

    def test_emoji_removal(self):
        """Test emoji removal"""
        cleaner = PersianTextCleaner(remove_emojis=True)
        text = "سلام 😊 چطوری؟ 👍"
        result = cleaner.clean(text)

        self.assertNotIn('😊', result)
        self.assertNotIn('👍', result)

    def test_whitespace_cleaning(self):
        """Test extra whitespace removal"""
        text = "این    یک     متن      است"
        result = self.cleaner.clean(text)

        self.assertNotIn('    ', result)
        self.assertEqual(result.count('  '), 0)

    def test_lowercase_english(self):
        """Test English text lowercasing"""
        cleaner = PersianTextCleaner(lowercase_english=True)
        text = "من PYTHON را دوست دارم"
        result = cleaner.clean(text)

        self.assertIn('python', result)
        self.assertNotIn('PYTHON', result)
        # Persian should remain unchanged
        self.assertIn('من', result)

    def test_remove_special_chars(self):
        """Test special character removal"""
        text = "متن@#$%با^&*کاراکترهای()خاص"
        result = self.cleaner.remove_special_chars(text)

        self.assertNotIn('@', result)
        self.assertNotIn('#', result)
        self.assertNotIn('$', result)
        self.assertIn('متن', result)
        self.assertIn('با', result)

    def test_remove_special_chars_keep_some(self):
        """Test special character removal with keep list"""
        text = "سلام! چطوری؟"
        result = self.cleaner.remove_special_chars(text, keep_chars='!?')

        self.assertIn('!', result)
        self.assertIn('؟', result)

    def test_remove_punctuation(self):
        """Test punctuation removal"""
        text = "سلام، حال شما چطور است؟"
        result = self.cleaner.remove_punctuation(text)

        self.assertNotIn('،', result)
        self.assertNotIn('؟', result)

    def test_remove_punctuation_keep_some(self):
        """Test punctuation removal with keep list"""
        text = "سلام! چطوری؟ خوبم."
        result = self.cleaner.remove_punctuation(text, keep_punctuation='؟')

        self.assertIn('؟', result)
        self.assertNotIn('!', result)
        self.assertNotIn('.', result)

    def test_remove_numbers(self):
        """Test number removal"""
        text = "من ۲۵ سال دارم و 100 کتاب خواندم"
        result = self.cleaner.remove_numbers(text)

        self.assertNotIn('۲۵', result)
        self.assertNotIn('100', result)
        self.assertIn('من', result)
        self.assertIn('سال', result)

    def test_remove_non_persian(self):
        """Test keeping only Persian characters"""
        text = "Persian فارسی with English 123"
        result = self.cleaner.remove_non_persian(text)

        self.assertNotIn('Persian', result)
        self.assertNotIn('English', result)
        self.assertNotIn('123', result)
        self.assertIn('فارسی', result)

    def test_remove_non_persian_keep_numbers(self):
        """Test keeping Persian and numbers"""
        text = "فارسی ۱۲۳ English 456"
        result = self.cleaner.remove_non_persian(text, keep_numbers=True)

        self.assertIn('فارسی', result)
        self.assertIn('۱۲۳', result)
        self.assertIn('456', result)
        self.assertNotIn('English', result)

    def test_remove_repeated_chars(self):
        """Test repeated character removal"""
        text = "واااااای چقدررررر خوووووب"
        result = self.cleaner.remove_repeated_chars(text, max_repeat=2)

        self.assertNotIn('ااااا', result)
        self.assertNotIn('ررررر', result)
        # Should keep max 2 repetitions
        self.assertIn('وا', result)

    def test_batch_clean(self):
        """Test batch cleaning"""
        texts = [
            "متن اول https://example.com",
            "متن دوم @user",
            "متن سوم #hashtag"
        ]

        cleaner = PersianTextCleaner(
            replace_urls_with='<URL>',
            replace_mentions_with='<USER>',
            replace_hashtags_with='<TAG>'
        )

        results = cleaner.batch_clean(texts)

        self.assertEqual(len(results), 3)
        self.assertIn('<URL>', results[0])
        self.assertIn('<USER>', results[1])
        self.assertIn('<TAG>', results[2])

    def test_empty_text(self):
        """Test with empty text"""
        result = self.cleaner.clean("")
        self.assertEqual(result, "")

    def test_multiple_operations(self):
        """Test multiple cleaning operations together"""
        cleaner = PersianTextCleaner(
            remove_urls=True,
            remove_emojis=True,
            remove_html=True,
            lowercase_english=True
        )

        text = "<p>سلام 😊 https://test.com HELLO</p>"
        result = cleaner.clean(text)

        self.assertNotIn('<p>', result)
        self.assertNotIn('😊', result)
        self.assertNotIn('https://', result)
        self.assertIn('hello', result)
        self.assertIn('سلام', result)


if __name__ == '__main__':
    unittest.main()
