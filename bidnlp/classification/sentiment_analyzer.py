"""
Persian Sentiment Analyzer

Provides sentiment analysis for Persian text using keyword-based approach.
"""

from typing import List, Dict, Optional
from .base_classifier import BaseTextClassifier


class PersianSentimentAnalyzer(BaseTextClassifier):
    """Keyword-based sentiment analyzer for Persian text."""

    # Positive keywords
    DEFAULT_POSITIVE_KEYWORDS = {
        'خوب', 'عالی', 'فوق‌العاده', 'بهترین', 'عظیم', 'خیلی خوب', 'خوشحال',
        'شاد', 'مثبت', 'موفق', 'موفقیت', 'برنده', 'پیروز', 'پیروزی',
        'دوست', 'محبوب', 'محبت', 'عشق', 'لذت', 'خوشمزه', 'زیبا',
        'قشنگ', 'جذاب', 'باکیفیت', 'کیفیت', 'حرفه‌ای', 'تحسین', 'ستودنی',
        'رضایت', 'راضی', 'خوشایند', 'لذت‌بخش', 'مفید', 'کارآمد', 'اعتماد',
        'معتبر', 'درست', 'صحیح', 'دقیق', 'سریع', 'آسان', 'راحت',
        'ممنون', 'متشکر', 'سپاس', 'تشکر', 'احسنت', 'آفرین', 'درود',
    }

    # Negative keywords
    DEFAULT_NEGATIVE_KEYWORDS = {
        'بد', 'ضعیف', 'افتضاح', 'وحشتناک', 'بدترین', 'ناامید', 'غمگین',
        'ناراحت', 'منفی', 'شکست', 'ناموفق', 'بازنده', 'متاسف', 'تاسف',
        'نفرت', 'متنفر', 'عصبانی', 'خشم', 'درد', 'رنج', 'مشکل',
        'اشکال', 'خراب', 'خرابی', 'نقص', 'کند', 'سخت', 'دشوار',
        'بی‌کیفیت', 'ناکارآمد', 'گران', 'گرانی', 'کلاهبرداری', 'تقلبی',
        'دروغ', 'دروغین', 'تاخیر', 'تعطیل', 'نامناسب', 'ناپسند',
        'متاسفانه', 'انتقاد', 'شکایت', 'اعتراض', 'جنجال', 'پایین',
    }

    # Neutral/negation keywords
    NEGATION_KEYWORDS = {
        'نه', 'نی', 'نمی', 'ن', 'بدون', 'بی', 'غیر', 'هیچ',
        'نیست', 'نبود', 'ن\u200cیست', 'ن\u200cبود',  # With ZWNJ
    }

    def __init__(self,
                 normalize: bool = True,
                 remove_stopwords: bool = False,
                 positive_keywords: Optional[set] = None,
                 negative_keywords: Optional[set] = None,
                 custom_keywords: Optional[Dict[str, set]] = None):
        """
        Initialize sentiment analyzer.

        Args:
            normalize: Whether to normalize text
            remove_stopwords: Whether to remove stop words
            positive_keywords: Custom positive keywords (if None, use defaults)
            negative_keywords: Custom negative keywords (if None, use defaults)
            custom_keywords: Dictionary with 'positive' and 'negative' keys
        """
        super().__init__(normalize=normalize, remove_stopwords=remove_stopwords)

        # Initialize keywords
        if custom_keywords:
            self.positive_keywords = custom_keywords.get('positive', set())
            self.negative_keywords = custom_keywords.get('negative', set())
        else:
            self.positive_keywords = positive_keywords or self.DEFAULT_POSITIVE_KEYWORDS.copy()
            self.negative_keywords = negative_keywords or self.DEFAULT_NEGATIVE_KEYWORDS.copy()

        self.negation_keywords = self.NEGATION_KEYWORDS.copy()
        self._is_trained = True  # Keyword-based, no training needed

    def train(self, texts: List[str], labels: List[str]) -> None:
        """
        Train is not required for keyword-based sentiment analysis.
        This method can be used to extract keywords from training data.

        Args:
            texts: List of training texts (not used)
            labels: List of corresponding labels (not used)
        """
        # Keyword-based approach doesn't require training
        # But we mark it as trained
        self._is_trained = True

    def add_positive_keyword(self, keyword: str) -> None:
        """Add a positive keyword."""
        self.positive_keywords.add(keyword)

    def add_negative_keyword(self, keyword: str) -> None:
        """Add a negative keyword."""
        self.negative_keywords.add(keyword)

    def add_positive_keywords(self, keywords: List[str]) -> None:
        """Add multiple positive keywords."""
        self.positive_keywords.update(keywords)

    def add_negative_keywords(self, keywords: List[str]) -> None:
        """Add multiple negative keywords."""
        self.negative_keywords.update(keywords)

    def _check_negation(self, words: List[str], index: int) -> bool:
        """
        Check if a word at given index is negated.

        Args:
            words: List of words
            index: Index to check

        Returns:
            True if word is negated
        """
        # Check 2 words before for negation
        for i in range(max(0, index - 2), index):
            if words[i] in self.negation_keywords:
                return True

        # Check 2 words after for negation (Persian often puts negation after)
        for i in range(index + 1, min(len(words), index + 3)):
            if words[i] in self.negation_keywords:
                return True

        return False

    def analyze(self, text: str) -> Dict[str, any]:
        """
        Analyze sentiment of text.

        Args:
            text: Input text

        Returns:
            Dictionary with sentiment analysis results
        """
        # Preprocess
        processed_text = self.preprocess(text)
        words = processed_text.split()

        # Count sentiments
        positive_count = 0
        negative_count = 0
        positive_words = []
        negative_words = []

        for i, word in enumerate(words):
            is_negated = self._check_negation(words, i)

            if word in self.positive_keywords:
                if is_negated:
                    negative_count += 1
                    negative_words.append(f"NOT {word}")
                else:
                    positive_count += 1
                    positive_words.append(word)

            elif word in self.negative_keywords:
                if is_negated:
                    positive_count += 1
                    positive_words.append(f"NOT {word}")
                else:
                    negative_count += 1
                    negative_words.append(word)

        # Calculate sentiment
        total = positive_count + negative_count

        if total == 0:
            sentiment = 'neutral'
            score = 0.0
        elif positive_count > negative_count:
            sentiment = 'positive'
            score = (positive_count - negative_count) / total
        elif negative_count > positive_count:
            sentiment = 'negative'
            score = (negative_count - positive_count) / total
        else:
            sentiment = 'neutral'
            score = 0.0

        return {
            'sentiment': sentiment,
            'score': score,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'positive_words': positive_words,
            'negative_words': negative_words,
        }

    def predict(self, text: str) -> str:
        """
        Predict sentiment class.

        Args:
            text: Input text

        Returns:
            Sentiment label: 'positive', 'negative', or 'neutral'
        """
        result = self.analyze(text)
        return result['sentiment']

    def predict_proba(self, text: str) -> Dict[str, float]:
        """
        Predict sentiment probabilities.

        Args:
            text: Input text

        Returns:
            Dictionary mapping sentiments to probabilities
        """
        result = self.analyze(text)
        sentiment = result['sentiment']
        score = result['score']

        if sentiment == 'neutral':
            return {
                'positive': 0.33,
                'negative': 0.33,
                'neutral': 0.34
            }
        elif sentiment == 'positive':
            positive_prob = 0.5 + (score * 0.5)
            negative_prob = (1.0 - positive_prob) / 2
            neutral_prob = (1.0 - positive_prob) / 2
            return {
                'positive': positive_prob,
                'negative': negative_prob,
                'neutral': neutral_prob
            }
        else:  # negative
            negative_prob = 0.5 + (score * 0.5)
            positive_prob = (1.0 - negative_prob) / 2
            neutral_prob = (1.0 - negative_prob) / 2
            return {
                'positive': positive_prob,
                'negative': negative_prob,
                'neutral': neutral_prob
            }

    def get_sentiment_score(self, text: str) -> float:
        """
        Get sentiment score (-1.0 to 1.0).

        Args:
            text: Input text

        Returns:
            Score: -1.0 (very negative) to 1.0 (very positive)
        """
        result = self.analyze(text)
        if result['sentiment'] == 'positive':
            return result['score']
        elif result['sentiment'] == 'negative':
            return -result['score']
        else:
            return 0.0

    def get_params(self) -> Dict[str, any]:
        """Get analyzer parameters."""
        params = super().get_params()
        params.update({
            'positive_keywords_count': len(self.positive_keywords),
            'negative_keywords_count': len(self.negative_keywords),
        })
        return params
