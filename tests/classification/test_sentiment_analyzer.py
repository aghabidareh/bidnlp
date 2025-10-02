"""
Tests for Persian sentiment analyzer
"""

import pytest
from bidnlp.classification import PersianSentimentAnalyzer


class TestPersianSentimentAnalyzer:
    """Test cases for PersianSentimentAnalyzer."""

    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = PersianSentimentAnalyzer()

    def test_positive_sentiment(self):
        """Test positive sentiment detection."""
        texts = [
            "این کتاب خیلی خوب است",
            "عالی بود، خیلی راضی هستم",
            "کیفیت فوق‌العاده و قیمت مناسب",
        ]

        for text in texts:
            result = self.analyzer.predict(text)
            assert result == 'positive', f"Failed for: {text}"

    def test_negative_sentiment(self):
        """Test negative sentiment detection."""
        texts = [
            "این محصول بد است",
            "خیلی ضعیف و افتضاح بود",
            "کیفیت بسیار پایین و گران",
        ]

        for text in texts:
            result = self.analyzer.predict(text)
            assert result == 'negative', f"Failed for: {text}"

    def test_neutral_sentiment(self):
        """Test neutral sentiment (no keywords)."""
        texts = [
            "این یک کتاب است",
            "محصول رنگ آبی دارد",
        ]

        for text in texts:
            result = self.analyzer.predict(text)
            assert result == 'neutral', f"Failed for: {text}"

    def test_negation_handling(self):
        """Test negation handling."""
        # "not good" should be negative
        text = "این محصول خوب نیست"
        result = self.analyzer.predict(text)
        # Should detect negation
        assert result in ['negative', 'neutral']

    def test_analyze_detailed(self):
        """Test detailed analysis."""
        text = "این کتاب خیلی خوب و جذاب است"
        result = self.analyzer.analyze(text)

        assert 'sentiment' in result
        assert 'score' in result
        assert 'positive_count' in result
        assert 'negative_count' in result
        assert 'positive_words' in result
        assert 'negative_words' in result

        assert result['sentiment'] == 'positive'
        assert result['positive_count'] > 0

    def test_sentiment_score(self):
        """Test sentiment score calculation."""
        positive_text = "عالی و فوق‌العاده"
        score = self.analyzer.get_sentiment_score(positive_text)
        assert score > 0

        negative_text = "بد و ضعیف"
        score = self.analyzer.get_sentiment_score(negative_text)
        assert score < 0

    def test_predict_proba(self):
        """Test probability prediction."""
        text = "خیلی خوب است"
        proba = self.analyzer.predict_proba(text)

        assert 'positive' in proba
        assert 'negative' in proba
        assert 'neutral' in proba
        assert abs(sum(proba.values()) - 1.0) < 0.01  # Should sum to 1

    def test_custom_keywords(self):
        """Test custom keyword addition."""
        self.analyzer.add_positive_keyword('تست‌مثبت')
        text = "این تست‌مثبت است"
        result = self.analyzer.predict(text)
        assert result == 'positive'

    def test_batch_prediction(self):
        """Test batch prediction."""
        texts = [
            "خوب است",
            "بد است",
            "معمولی است",
        ]
        results = self.analyzer.predict_batch(texts)
        assert len(results) == 3

    def test_is_trained(self):
        """Test is_trained property."""
        # Keyword-based analyzer is always trained
        assert self.analyzer.is_trained()

    def test_empty_text(self):
        """Test empty text handling."""
        result = self.analyzer.predict("")
        assert result == 'neutral'

    def test_mixed_sentiment(self):
        """Test text with mixed sentiment."""
        text = "کتاب خوب بود اما قیمت گران است"
        result = self.analyzer.analyze(text)
        # Should have both positive and negative counts
        assert result['positive_count'] > 0
        assert result['negative_count'] > 0
