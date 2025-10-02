"""
Tests for keyword-based classifier
"""

import pytest
from bidnlp.classification import KeywordClassifier


class TestKeywordClassifier:
    """Test cases for KeywordClassifier."""

    def setup_method(self):
        """Set up test fixtures."""
        self.classifier = KeywordClassifier()

    def test_add_category(self):
        """Test adding categories."""
        self.classifier.add_category('ورزش', {'فوتبال', 'بسکتبال', 'والیبال'})
        self.classifier.add_category('تکنولوژی', {'کامپیوتر', 'موبایل', 'نرم‌افزار'})

        categories = self.classifier.get_categories()
        assert 'ورزش' in categories
        assert 'تکنولوژی' in categories

    def test_classify_with_keywords(self):
        """Test classification with predefined keywords."""
        self.classifier.add_category('ورزش', {'فوتبال', 'بازیکن', 'تیم', 'گل'})
        self.classifier.add_category('تکنولوژی', {'کامپیوتر', 'نرم‌افزار', 'برنامه'})

        # Sports text
        text = "بازیکن تیم فوتبال گل زد"
        result = self.classifier.classify(text)
        assert result['category'] == 'ورزش'

        # Technology text
        text = "نرم‌افزار کامپیوتر برنامه جدید"
        result = self.classifier.classify(text)
        assert result['category'] == 'تکنولوژی'

    def test_train_from_data(self):
        """Test training from labeled data."""
        texts = [
            "فوتبال بازی جذابی است",
            "تیم ملی فوتبال برد",
            "کامپیوتر ابزار مفیدی است",
            "نرم‌افزار جدید منتشر شد",
        ]
        labels = ['ورزش', 'ورزش', 'تکنولوژی', 'تکنولوژی']

        self.classifier.train(texts, labels)

        assert self.classifier.is_trained()
        assert 'ورزش' in self.classifier.get_categories()
        assert 'تکنولوژی' in self.classifier.get_categories()

    def test_predict(self):
        """Test prediction."""
        self.classifier.add_category('ورزش', {'فوتبال', 'بازیکن'})
        self.classifier.add_category('سیاست', {'دولت', 'انتخابات'})

        text = "بازیکن فوتبال"
        prediction = self.classifier.predict(text)
        assert prediction == 'ورزش'

    def test_predict_proba(self):
        """Test probability prediction."""
        self.classifier.add_category('ورزش', {'فوتبال'})
        self.classifier.add_category('تکنولوژی', {'کامپیوتر'})

        text = "فوتبال"
        proba = self.classifier.predict_proba(text)

        assert 'ورزش' in proba
        assert 'تکنولوژی' in proba
        assert proba['ورزش'] > proba['تکنولوژی']

    def test_predict_top_k(self):
        """Test top K predictions."""
        self.classifier.add_category('ورزش', {'فوتبال'})
        self.classifier.add_category('تکنولوژی', {'کامپیوتر'})
        self.classifier.add_category('سیاست', {'دولت'})

        text = "فوتبال"
        top_k = self.classifier.predict_top_k(text, k=2)

        assert len(top_k) == 2
        assert top_k[0][0] == 'ورزش'  # First should be sports

    def test_unknown_category(self):
        """Test unknown category for text with no matches."""
        self.classifier.add_category('ورزش', {'فوتبال'})

        text = "کتاب خواندن"
        result = self.classifier.classify(text)
        assert result['category'] == 'unknown'

    def test_add_keyword_to_category(self):
        """Test adding keyword to existing category."""
        self.classifier.add_category('ورزش', {'فوتبال'})
        self.classifier.add_keyword_to_category('ورزش', 'بسکتبال')

        keywords = self.classifier.get_category_keywords('ورزش')
        assert 'بسکتبال' in keywords

    def test_remove_category(self):
        """Test removing category."""
        self.classifier.add_category('ورزش', {'فوتبال'})
        self.classifier.remove_category('ورزش')

        categories = self.classifier.get_categories()
        assert 'ورزش' not in categories

    def test_batch_prediction(self):
        """Test batch prediction."""
        self.classifier.add_category('ورزش', {'فوتبال'})
        self.classifier.add_category('تکنولوژی', {'کامپیوتر'})

        texts = ["فوتبال", "کامپیوتر"]
        results = self.classifier.predict_batch(texts)

        assert len(results) == 2
        assert results[0] == 'ورزش'
        assert results[1] == 'تکنولوژی'

    def test_matched_keywords(self):
        """Test matched keywords in results."""
        self.classifier.add_category('ورزش', {'فوتبال', 'بازیکن', 'تیم'})

        text = "فوتبال بازیکن تیم"
        result = self.classifier.classify(text)

        assert 'matched_keywords' in result
        matched = result['matched_keywords']['ورزش']
        assert 'فوتبال' in matched
        assert 'بازیکن' in matched

    def test_confidence_score(self):
        """Test confidence scoring."""
        self.classifier.add_category('ورزش', {'فوتبال', 'بازیکن'})
        self.classifier.add_category('تکنولوژی', {'کامپیوتر'})

        text = "فوتبال بازیکن"
        result = self.classifier.classify(text)

        assert 'confidence' in result
        assert 0.0 <= result['confidence'] <= 1.0
        assert result['confidence'] > 0

    def test_get_params(self):
        """Test getting parameters."""
        self.classifier.add_category('ورزش', {'فوتبال'})
        params = self.classifier.get_params()

        assert 'num_categories' in params
        assert params['num_categories'] == 1
        assert 'categories' in params

    def test_train_unequal_lengths(self):
        """Test training with unequal text/label lengths."""
        texts = ["text1", "text2"]
        labels = ["label1"]

        with pytest.raises(ValueError):
            self.classifier.train(texts, labels)

    def test_untrained_classification(self):
        """Test classification before training/adding categories."""
        with pytest.raises(ValueError):
            self.classifier.predict("test")
