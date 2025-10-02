"""
Persian Text Validators

Provides validation utilities for Persian text.
"""

import re
from typing import List, Optional
from .characters import PersianCharacters


class PersianTextValidator:
    """Validators for Persian text quality and correctness."""

    def __init__(self):
        """Initialize the validator."""
        self.char_utils = PersianCharacters()

    def is_valid_persian_text(self, text: str, min_ratio: float = 0.5) -> bool:
        """
        Check if text is valid Persian (contains sufficient Persian characters).

        Args:
            text: Input text
            min_ratio: Minimum ratio of Persian characters required

        Returns:
            True if text meets Persian character ratio threshold
        """
        if not text or not text.strip():
            return False

        return self.char_utils.is_persian_text(text, threshold=min_ratio)

    def has_mixed_arabic_persian(self, text: str) -> bool:
        """
        Check if text contains mixed Arabic and Persian characters.

        Args:
            text: Input text

        Returns:
            True if text contains both Arabic and Persian characters
        """
        has_persian = self.char_utils.has_persian(text)
        has_arabic = self.char_utils.has_arabic(text)
        return has_persian and has_arabic

    def has_mixed_digit_systems(self, text: str) -> bool:
        """
        Check if text contains mixed digit systems.

        Args:
            text: Input text

        Returns:
            True if text contains multiple digit systems
        """
        systems = []

        if any(c in self.char_utils.PERSIAN_DIGITS for c in text):
            systems.append('persian')
        if any(c in self.char_utils.ARABIC_INDIC_DIGITS for c in text):
            systems.append('arabic_indic')
        if any(c in self.char_utils.ENGLISH_DIGITS for c in text):
            systems.append('english')

        return len(systems) > 1

    def has_inconsistent_yeh_kaf(self, text: str) -> bool:
        """
        Check if text has inconsistent yeh/kaf usage (mixing Persian and Arabic).

        Args:
            text: Input text

        Returns:
            True if text mixes different yeh or kaf variants
        """
        # Check for yeh inconsistency
        has_persian_yeh = 'ی' in text
        has_arabic_yeh = 'ي' in text

        # Check for kaf inconsistency
        has_persian_kaf = 'ک' in text
        has_arabic_kaf = 'ك' in text

        return (has_persian_yeh and has_arabic_yeh) or (has_persian_kaf and has_arabic_kaf)

    def is_normalized(self, text: str) -> bool:
        """
        Check if text appears to be normalized (no Arabic chars, consistent digits).

        Args:
            text: Input text

        Returns:
            True if text appears normalized
        """
        # Check for Arabic characters that should be Persian
        if self.char_utils.has_arabic(text):
            return False

        # Check for mixed digit systems
        if self.has_mixed_digit_systems(text):
            return False

        return True

    def has_proper_spacing(self, text: str) -> bool:
        """
        Check if text has proper spacing (no multiple spaces, proper punctuation spacing).

        Args:
            text: Input text

        Returns:
            True if spacing appears correct
        """
        # Check for multiple consecutive spaces
        if '  ' in text:
            return False

        # Check for tabs
        if '\t' in text:
            return False

        # Check for space before Persian punctuation
        persian_punct = ['،', '؛', '؟', '.', '!', '?']
        for punct in persian_punct:
            if f' {punct}' in text:
                return False

        return True

    def has_proper_zwnj_usage(self, text: str) -> bool:
        """
        Check for common ZWNJ issues.

        Args:
            text: Input text

        Returns:
            True if ZWNJ usage appears correct (basic check)
        """
        zwnj = self.char_utils.ZWNJ

        # Check for multiple consecutive ZWNJs
        if zwnj + zwnj in text:
            return False

        # Check for ZWNJ at start or end
        if text.startswith(zwnj) or text.endswith(zwnj):
            return False

        return True

    def check_word_length(self, text: str, max_length: int = 50) -> List[str]:
        """
        Find words that exceed maximum length (likely errors).

        Args:
            text: Input text
            max_length: Maximum acceptable word length

        Returns:
            List of words exceeding max length
        """
        words = text.split()
        long_words = [word for word in words if len(word) > max_length]
        return long_words

    def has_repeated_characters(self, text: str, max_repeats: int = 3) -> bool:
        """
        Check if text has excessively repeated characters.

        Args:
            text: Input text
            max_repeats: Maximum allowed character repetitions

        Returns:
            True if any character repeats more than max_repeats times
        """
        pattern = r'(.)\1{' + str(max_repeats) + r',}'
        return bool(re.search(pattern, text))

    def find_repeated_characters(self, text: str, max_repeats: int = 3) -> List[str]:
        """
        Find sequences of repeated characters.

        Args:
            text: Input text
            max_repeats: Maximum allowed character repetitions

        Returns:
            List of repeated character sequences
        """
        pattern = r'(.)\1{' + str(max_repeats) + r',}'
        matches = re.findall(pattern, text)
        return matches

    def has_url(self, text: str) -> bool:
        """
        Check if text contains URLs.

        Args:
            text: Input text

        Returns:
            True if URLs are found
        """
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return bool(re.search(url_pattern, text))

    def has_email(self, text: str) -> bool:
        """
        Check if text contains email addresses.

        Args:
            text: Input text

        Returns:
            True if emails are found
        """
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return bool(re.search(email_pattern, text))

    def has_mention(self, text: str) -> bool:
        """
        Check if text contains mentions (@username).

        Args:
            text: Input text

        Returns:
            True if mentions are found
        """
        return '@' in text and bool(re.search(r'@\w+', text))

    def has_hashtag(self, text: str) -> bool:
        """
        Check if text contains hashtags.

        Args:
            text: Input text

        Returns:
            True if hashtags are found
        """
        return '#' in text and bool(re.search(r'#\w+', text))

    def is_clean_text(self, text: str) -> bool:
        """
        Check if text is clean (no URLs, emails, mentions, hashtags).

        Args:
            text: Input text

        Returns:
            True if text contains no special elements
        """
        return not (self.has_url(text) or self.has_email(text) or
                   self.has_mention(text) or self.has_hashtag(text))

    def validate_text(self, text: str, strict: bool = False) -> dict:
        """
        Comprehensive text validation.

        Args:
            text: Input text
            strict: If True, apply stricter validation rules

        Returns:
            Dictionary with validation results
        """
        results = {
            'is_valid_persian': self.is_valid_persian_text(text),
            'is_normalized': self.is_normalized(text),
            'has_proper_spacing': self.has_proper_spacing(text),
            'has_proper_zwnj': self.has_proper_zwnj_usage(text),
            'has_repeated_chars': self.has_repeated_characters(text),
            'has_urls': self.has_url(text),
            'has_emails': self.has_email(text),
            'has_mentions': self.has_mention(text),
            'has_hashtags': self.has_hashtag(text),
            'long_words': self.check_word_length(text),
            'has_mixed_arabic_persian': self.has_mixed_arabic_persian(text),
            'has_mixed_digits': self.has_mixed_digit_systems(text),
            'has_inconsistent_yeh_kaf': self.has_inconsistent_yeh_kaf(text),
        }

        # Calculate overall validity
        issues = []
        if not results['is_valid_persian']:
            issues.append('Not enough Persian content')
        if not results['is_normalized']:
            issues.append('Text not normalized')
        if not results['has_proper_spacing']:
            issues.append('Improper spacing')
        if not results['has_proper_zwnj']:
            issues.append('ZWNJ issues')
        if results['has_repeated_chars']:
            issues.append('Repeated characters')
        if results['long_words']:
            issues.append('Unusually long words')
        if results['has_mixed_arabic_persian']:
            issues.append('Mixed Arabic-Persian characters')
        if results['has_inconsistent_yeh_kaf']:
            issues.append('Inconsistent yeh/kaf usage')

        if strict:
            if results['has_urls']:
                issues.append('Contains URLs')
            if results['has_emails']:
                issues.append('Contains emails')
            if results['has_mentions']:
                issues.append('Contains mentions')
            if results['has_hashtags']:
                issues.append('Contains hashtags')
            if results['has_mixed_digits']:
                issues.append('Mixed digit systems')

        results['is_valid'] = len(issues) == 0
        results['issues'] = issues

        return results

    def get_quality_score(self, text: str) -> float:
        """
        Calculate text quality score (0.0-1.0).

        Args:
            text: Input text

        Returns:
            Quality score between 0.0 and 1.0
        """
        if not text or not text.strip():
            return 0.0

        validation = self.validate_text(text, strict=False)

        score = 1.0

        # Deduct points for issues
        if not validation['is_valid_persian']:
            score -= 0.3
        if not validation['is_normalized']:
            score -= 0.2
        if not validation['has_proper_spacing']:
            score -= 0.1
        if not validation['has_proper_zwnj']:
            score -= 0.1
        if validation['has_repeated_chars']:
            score -= 0.1
        if validation['long_words']:
            score -= 0.1
        if validation['has_mixed_arabic_persian']:
            score -= 0.1

        return max(0.0, score)
