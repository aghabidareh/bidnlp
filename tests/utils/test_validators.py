"""
Tests for Persian text validators
"""

import pytest
from bidnlp.utils import PersianTextValidator


class TestPersianTextValidator:
    """Test cases for PersianTextValidator class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.validator = PersianTextValidator()

    def test_is_valid_persian_text(self):
        """Test valid Persian text detection."""
        assert self.validator.is_valid_persian_text("سلام دنیا")
        assert not self.validator.is_valid_persian_text("hello world")
        assert self.validator.is_valid_persian_text("سلام hello", min_ratio=0.3)

    def test_has_mixed_arabic_persian(self):
        """Test mixed Arabic-Persian detection."""
        text_mixed = "سلام كتاب"  # ك is Arabic
        assert self.validator.has_mixed_arabic_persian(text_mixed)

        text_pure = "سلام کتاب"  # All Persian
        assert not self.validator.has_mixed_arabic_persian(text_pure)

    def test_has_mixed_digit_systems(self):
        """Test mixed digit system detection."""
        assert self.validator.has_mixed_digit_systems("۱۲ 34")  # Persian + English
        assert self.validator.has_mixed_digit_systems("۱۲ ٣٤")  # Persian + Arabic-Indic
        assert not self.validator.has_mixed_digit_systems("۱۲۳")  # Only Persian

    def test_has_inconsistent_yeh_kaf(self):
        """Test inconsistent yeh/kaf usage."""
        assert self.validator.has_inconsistent_yeh_kaf("کتاب كتاب")  # Mixed kaf
        assert self.validator.has_inconsistent_yeh_kaf("می يک")  # Mixed yeh
        assert not self.validator.has_inconsistent_yeh_kaf("کتاب می")  # Consistent

    def test_is_normalized(self):
        """Test text normalization check."""
        assert self.validator.is_normalized("سلام دنیا ۱۲۳")
        assert not self.validator.is_normalized("سلام كتاب")  # Arabic kaf
        assert not self.validator.is_normalized("سلام ۱۲ 34")  # Mixed digits

    def test_has_proper_spacing(self):
        """Test proper spacing check."""
        assert self.validator.has_proper_spacing("سلام دنیا")
        assert not self.validator.has_proper_spacing("سلام  دنیا")  # Double space
        assert not self.validator.has_proper_spacing("سلام ، دنیا")  # Space before comma

    def test_has_proper_zwnj_usage(self):
        """Test ZWNJ usage check."""
        zwnj = '\u200c'
        assert self.validator.has_proper_zwnj_usage("می" + zwnj + "روم")
        assert not self.validator.has_proper_zwnj_usage(zwnj + "سلام")  # ZWNJ at start
        assert not self.validator.has_proper_zwnj_usage("سلام" + zwnj)  # ZWNJ at end
        assert not self.validator.has_proper_zwnj_usage("می" + zwnj + zwnj + "روم")  # Double ZWNJ

    def test_check_word_length(self):
        """Test checking for overly long words."""
        text = "سلام دنیا"
        long_words = self.validator.check_word_length(text, max_length=10)
        assert len(long_words) == 0

        text_with_long = "سلام " + "ا" * 60
        long_words = self.validator.check_word_length(text_with_long, max_length=50)
        assert len(long_words) == 1

    def test_has_repeated_characters(self):
        """Test repeated character detection."""
        assert self.validator.has_repeated_characters("سلاااام", max_repeats=3)
        assert not self.validator.has_repeated_characters("سلام", max_repeats=3)

    def test_find_repeated_characters(self):
        """Test finding repeated character sequences."""
        text = "سلاااام"
        repeated = self.validator.find_repeated_characters(text, max_repeats=3)
        assert len(repeated) > 0

    def test_has_url(self):
        """Test URL detection."""
        assert self.validator.has_url("سلام https://example.com")
        assert self.validator.has_url("http://test.ir")
        assert not self.validator.has_url("سلام دنیا")

    def test_has_email(self):
        """Test email detection."""
        assert self.validator.has_email("test@example.com")
        assert self.validator.has_email("سلام user@domain.ir")
        assert not self.validator.has_email("سلام دنیا")

    def test_has_mention(self):
        """Test mention detection."""
        assert self.validator.has_mention("سلام @username")
        assert not self.validator.has_mention("سلام دنیا")

    def test_has_hashtag(self):
        """Test hashtag detection."""
        assert self.validator.has_hashtag("سلام #test")
        assert not self.validator.has_hashtag("سلام دنیا")

    def test_is_clean_text(self):
        """Test clean text detection."""
        assert self.validator.is_clean_text("سلام دنیا")
        assert not self.validator.is_clean_text("سلام https://test.com")
        assert not self.validator.is_clean_text("سلام @user")
        assert not self.validator.is_clean_text("سلام #tag")
        assert not self.validator.is_clean_text("test@email.com")

    def test_validate_text_clean(self):
        """Test comprehensive validation on clean text."""
        text = "سلام دنیا چطوری هستید"
        result = self.validator.validate_text(text)

        assert result['is_valid']
        assert result['is_valid_persian']
        assert result['is_normalized']
        assert len(result['issues']) == 0

    def test_validate_text_with_issues(self):
        """Test comprehensive validation on problematic text."""
        text = "سلام كتاب"  # Arabic kaf
        result = self.validator.validate_text(text)

        assert not result['is_valid']
        assert not result['is_normalized']
        assert len(result['issues']) > 0

    def test_validate_text_strict(self):
        """Test strict validation mode."""
        text = "سلام https://test.com"
        result = self.validator.validate_text(text, strict=True)

        assert not result['is_valid']
        assert 'Contains URLs' in result['issues']

    def test_get_quality_score(self):
        """Test quality score calculation."""
        # Perfect text
        good_text = "سلام دنیا چطوری"
        score = self.validator.get_quality_score(good_text)
        assert score >= 0.8

        # Problematic text
        bad_text = "سلام كتاب"  # Arabic kaf
        score = self.validator.get_quality_score(bad_text)
        assert score < 1.0

    def test_empty_text_validation(self):
        """Test validation on empty text."""
        assert not self.validator.is_valid_persian_text("")
        assert self.validator.get_quality_score("") == 0.0

    def test_english_only_text(self):
        """Test validation on English-only text."""
        text = "hello world"
        assert not self.validator.is_valid_persian_text(text)

        result = self.validator.validate_text(text)
        assert not result['is_valid_persian']

    def test_mixed_language_text(self):
        """Test validation on mixed language text."""
        text = "سلام دنیا hello"  # More Persian than English
        result = self.validator.validate_text(text)

        # Should be valid Persian with sufficient ratio
        assert result['is_valid_persian']  # Default threshold is 0.5

    def test_text_with_numbers(self):
        """Test validation on text with numbers."""
        text = "سلام ۱۲۳"
        result = self.validator.validate_text(text)
        assert result['is_valid_persian']
        assert not result['has_mixed_digits']

    def test_all_validation_fields_present(self):
        """Test that all expected fields are in validation result."""
        text = "سلام دنیا"
        result = self.validator.validate_text(text)

        expected_fields = [
            'is_valid_persian', 'is_normalized', 'has_proper_spacing',
            'has_proper_zwnj', 'has_repeated_chars', 'has_urls',
            'has_emails', 'has_mentions', 'has_hashtags', 'long_words',
            'has_mixed_arabic_persian', 'has_mixed_digits',
            'has_inconsistent_yeh_kaf', 'is_valid', 'issues'
        ]

        for field in expected_fields:
            assert field in result, f"Field '{field}' missing from validation result"
