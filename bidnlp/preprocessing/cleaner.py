"""
Persian Text Cleaner

Advanced cleaning functionality for Persian text including:
- URL removal/replacement
- Email removal/replacement
- Mention and hashtag handling
- HTML tag removal
- Emoji handling
- Special character removal
- Profanity filtering (optional)
"""

import re
from typing import Optional, List, Callable


class PersianTextCleaner:
    """
    Text cleaner for Persian (Farsi) text.

    Provides various cleaning operations to prepare text for NLP tasks.
    """

    def __init__(
        self,
        remove_urls: bool = False,
        remove_emails: bool = False,
        remove_mentions: bool = False,
        remove_hashtags: bool = False,
        remove_emojis: bool = False,
        remove_html: bool = True,
        remove_extra_whitespace: bool = True,
        lowercase_english: bool = False,
        replace_urls_with: Optional[str] = '<URL>',
        replace_emails_with: Optional[str] = '<EMAIL>',
        replace_mentions_with: Optional[str] = '<MENTION>',
        replace_hashtags_with: Optional[str] = '<HASHTAG>',
        replace_emojis_with: Optional[str] = None,
    ):
        """
        Initialize the text cleaner.

        Args:
            remove_urls: Remove URLs from text
            remove_emails: Remove email addresses
            remove_mentions: Remove @ mentions
            remove_hashtags: Remove # hashtags
            remove_emojis: Remove emoji characters
            remove_html: Remove HTML tags
            remove_extra_whitespace: Clean up extra whitespace
            lowercase_english: Convert English text to lowercase
            replace_urls_with: Replacement string for URLs (None to remove)
            replace_emails_with: Replacement string for emails
            replace_mentions_with: Replacement string for mentions
            replace_hashtags_with: Replacement string for hashtags
            replace_emojis_with: Replacement string for emojis
        """
        self.remove_urls = remove_urls
        self.remove_emails = remove_emails
        self.remove_mentions = remove_mentions
        self.remove_hashtags = remove_hashtags
        self.remove_emojis = remove_emojis
        self.remove_html = remove_html
        self.remove_extra_whitespace = remove_extra_whitespace
        self.lowercase_english = lowercase_english

        self.replace_urls_with = replace_urls_with if not remove_urls else ''
        self.replace_emails_with = replace_emails_with if not remove_emails else ''
        self.replace_mentions_with = replace_mentions_with if not remove_mentions else ''
        self.replace_hashtags_with = replace_hashtags_with if not remove_hashtags else ''
        self.replace_emojis_with = replace_emojis_with if not remove_emojis else ''

        # Regex patterns
        self.url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
            r'|(?:www\.)[a-zA-Z0-9-]+(?:\.[a-zA-Z]{2,})+'
        )

        self.email_pattern = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        )

        self.mention_pattern = re.compile(r'@[\w\u0600-\u06FF]+')
        self.hashtag_pattern = re.compile(r'#[\w\u0600-\u06FF]+')

        # HTML tag pattern
        self.html_pattern = re.compile(r'<[^>]+>')

        # Emoji pattern (comprehensive Unicode ranges)
        self.emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            "\U0001FA00-\U0001FA6F"  # Chess Symbols
            "\U00002600-\U000026FF"  # Miscellaneous Symbols
            "]+",
            flags=re.UNICODE
        )

    def clean_urls(self, text: str) -> str:
        """Remove or replace URLs"""
        if self.remove_urls or self.replace_urls_with is not None:
            replacement = self.replace_urls_with or ''
            text = self.url_pattern.sub(replacement, text)
        return text

    def clean_emails(self, text: str) -> str:
        """Remove or replace email addresses"""
        if self.remove_emails or self.replace_emails_with is not None:
            replacement = self.replace_emails_with or ''
            text = self.email_pattern.sub(replacement, text)
        return text

    def clean_mentions(self, text: str) -> str:
        """Remove or replace @ mentions"""
        if self.remove_mentions or self.replace_mentions_with is not None:
            replacement = self.replace_mentions_with or ''
            text = self.mention_pattern.sub(replacement, text)
        return text

    def clean_hashtags(self, text: str) -> str:
        """Remove or replace # hashtags"""
        if self.remove_hashtags or self.replace_hashtags_with is not None:
            replacement = self.replace_hashtags_with or ''
            text = self.hashtag_pattern.sub(replacement, text)
        return text

    def clean_html(self, text: str) -> str:
        """Remove HTML tags"""
        if self.remove_html:
            # First handle common HTML entities
            text = text.replace('&nbsp;', ' ')
            text = text.replace('&lt;', '<')
            text = text.replace('&gt;', '>')
            text = text.replace('&amp;', '&')
            text = text.replace('&quot;', '"')
            text = text.replace('&#39;', "'")

            # Remove HTML tags
            text = self.html_pattern.sub('', text)

        return text

    def clean_emojis(self, text: str) -> str:
        """Remove or replace emojis"""
        if self.remove_emojis or self.replace_emojis_with is not None:
            replacement = self.replace_emojis_with or ''
            text = self.emoji_pattern.sub(replacement, text)
        return text

    def clean_whitespace(self, text: str) -> str:
        """Clean up extra whitespace"""
        if self.remove_extra_whitespace:
            # Replace multiple spaces with single space
            text = re.sub(r' +', ' ', text)

            # Replace multiple newlines with single newline
            text = re.sub(r'\n+', '\n', text)

            # Remove leading/trailing whitespace
            text = text.strip()

            # Remove spaces at start of lines
            text = re.sub(r'\n ', '\n', text)

        return text

    def lowercase_latin(self, text: str) -> str:
        """Convert English/Latin characters to lowercase"""
        if self.lowercase_english:
            # Only lowercase ASCII characters
            result = []
            for char in text:
                if 'A' <= char <= 'Z':
                    result.append(char.lower())
                else:
                    result.append(char)
            text = ''.join(result)

        return text

    def remove_special_chars(self, text: str, keep_chars: str = '') -> str:
        """
        Remove special characters except specified ones.

        Args:
            text: Input text
            keep_chars: Characters to keep (e.g., '!?.')

        Returns:
            Text with special characters removed
        """
        # Keep Persian, English, numbers, whitespace, and specified chars
        pattern = r'[^\u0600-\u06FFa-zA-Z0-9\s' + re.escape(keep_chars) + r']'
        text = re.sub(pattern, ' ', text)
        text = re.sub(r' +', ' ', text)
        return text.strip()

    def remove_punctuation(self, text: str, keep_punctuation: str = '') -> str:
        """
        Remove punctuation marks.

        Args:
            text: Input text
            keep_punctuation: Punctuation to keep

        Returns:
            Text with punctuation removed
        """
        # Persian punctuation
        persian_punct = '،؛؟٪×÷'
        # English punctuation
        english_punct = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

        all_punct = persian_punct + english_punct

        # Remove punctuation not in keep list
        for punct in all_punct:
            if punct not in keep_punctuation:
                text = text.replace(punct, ' ')

        text = re.sub(r' +', ' ', text)
        return text.strip()

    def remove_numbers(self, text: str) -> str:
        """Remove all numbers (Persian and English)"""
        # Remove Persian digits
        text = re.sub(r'[۰-۹]+', '', text)
        # Remove English digits
        text = re.sub(r'[0-9]+', '', text)
        text = re.sub(r' +', ' ', text)
        return text.strip()

    def remove_non_persian(self, text: str, keep_numbers: bool = False) -> str:
        """
        Keep only Persian characters and optionally numbers.

        Args:
            text: Input text
            keep_numbers: If True, keep numbers

        Returns:
            Text with only Persian characters
        """
        if keep_numbers:
            pattern = r'[^\u0600-\u06FF\s۰-۹0-9]'
        else:
            pattern = r'[^\u0600-\u06FF\s]'

        text = re.sub(pattern, ' ', text)
        text = re.sub(r' +', ' ', text)
        return text.strip()

    def remove_repeated_chars(self, text: str, max_repeat: int = 2) -> str:
        """
        Remove repeated characters.

        Args:
            text: Input text
            max_repeat: Maximum allowed repetitions

        Returns:
            Text with repeated characters reduced
        """
        # Replace repeated characters
        pattern = r'(.)\1{' + str(max_repeat) + r',}'
        replacement = r'\1' * max_repeat
        text = re.sub(pattern, replacement, text)
        return text

    def clean(self, text: str) -> str:
        """
        Apply all configured cleaning operations.

        Args:
            text: Input text to clean

        Returns:
            Cleaned text
        """
        if not text:
            return text

        # Apply cleaning operations in order
        text = self.clean_html(text)
        text = self.clean_urls(text)
        text = self.clean_emails(text)
        text = self.clean_mentions(text)
        text = self.clean_hashtags(text)
        text = self.clean_emojis(text)
        text = self.lowercase_latin(text)
        text = self.clean_whitespace(text)

        return text

    def batch_clean(self, texts: List[str]) -> List[str]:
        """
        Clean multiple texts.

        Args:
            texts: List of texts to clean

        Returns:
            List of cleaned texts
        """
        return [self.clean(text) for text in texts]
