"""
Tests for feature extraction
"""

import pytest
from bidnlp.classification import BagOfWords, TfidfVectorizer, NgramExtractor


class TestBagOfWords:
    """Test cases for BagOfWords."""

    def test_fit_transform(self):
        """Test fit and transform."""
        docs = [
            "سلام دنیا",
            "سلام ایران",
            "دنیا زیباست",
        ]

        bow = BagOfWords()
        vectors = bow.fit_transform(docs)

        assert len(vectors) == 3
        assert bow._is_fitted

    def test_vocabulary(self):
        """Test vocabulary creation."""
        docs = ["سلام دنیا", "سلام ایران"]

        bow = BagOfWords()
        bow.fit(docs)

        vocab = bow.get_feature_names()
        assert 'سلام' in vocab
        assert 'دنیا' in vocab
        assert 'ایران' in vocab

    def test_max_features(self):
        """Test max features limit."""
        docs = ["یک دو سه چهار پنج شش"]

        bow = BagOfWords(max_features=3)
        bow.fit(docs)

        vocab = bow.get_feature_names()
        assert len(vocab) == 3

    def test_min_df(self):
        """Test minimum document frequency."""
        docs = [
            "سلام دنیا",
            "سلام ایران",
            "دوست خوب",
        ]

        # Only keep words that appear in at least 2 documents
        bow = BagOfWords(min_df=2)
        bow.fit(docs)

        vocab = bow.get_feature_names()
        assert 'سلام' in vocab  # Appears in 2 docs
        assert 'دوست' not in vocab  # Appears in only 1 doc

    def test_transform_counts(self):
        """Test that transform returns correct counts."""
        docs = ["سلام سلام دنیا"]

        bow = BagOfWords()
        vectors = bow.fit_transform(docs)

        # سلام appears twice
        vocab = bow.vocabulary
        salam_idx = vocab['سلام']
        assert vectors[0][salam_idx] == 2

    def test_unfitted_transform(self):
        """Test transform before fit raises error."""
        bow = BagOfWords()

        with pytest.raises(ValueError):
            bow.transform(["test"])


class TestTfidfVectorizer:
    """Test cases for TfidfVectorizer."""

    def test_fit_transform(self):
        """Test fit and transform."""
        docs = [
            "سلام دنیا",
            "سلام ایران",
            "دنیا زیباست",
        ]

        tfidf = TfidfVectorizer()
        vectors = tfidf.fit_transform(docs)

        assert len(vectors) == 3
        assert tfidf._is_fitted

    def test_idf_calculation(self):
        """Test IDF calculation."""
        docs = [
            "سلام دنیا",
            "سلام ایران",
        ]

        tfidf = TfidfVectorizer()
        tfidf.fit(docs)

        # سلام appears in all docs, should have lower IDF
        # دنیا and ایران appear in 1 doc each, should have higher IDF
        assert tfidf.idf['سلام'] < tfidf.idf['دنیا']

    def test_normalization(self):
        """Test L2 normalization."""
        docs = ["سلام دنیا"]

        tfidf = TfidfVectorizer()
        vectors = tfidf.fit_transform(docs)

        # Check L2 norm is 1
        vec = vectors[0]
        norm_squared = sum(v * v for v in vec.values())
        assert abs(norm_squared - 1.0) < 0.01

    def test_max_features(self):
        """Test max features limit."""
        docs = ["یک دو سه چهار پنج"]

        tfidf = TfidfVectorizer(max_features=3)
        tfidf.fit(docs)

        vocab = tfidf.get_feature_names()
        assert len(vocab) == 3

    def test_vocabulary(self):
        """Test vocabulary creation."""
        docs = ["سلام دنیا", "سلام ایران"]

        tfidf = TfidfVectorizer()
        tfidf.fit(docs)

        vocab = tfidf.get_feature_names()
        assert 'سلام' in vocab
        assert 'دنیا' in vocab

    def test_unfitted_transform(self):
        """Test transform before fit raises error."""
        tfidf = TfidfVectorizer()

        with pytest.raises(ValueError):
            tfidf.transform(["test"])


class TestNgramExtractor:
    """Test cases for NgramExtractor."""

    def test_bigrams(self):
        """Test bigram extraction."""
        docs = ["من به دانشگاه می روم"]

        ngram = NgramExtractor(n=2)
        vectors = ngram.fit_transform(docs)

        vocab = ngram.get_feature_names()
        assert 'من به' in vocab
        assert 'به دانشگاه' in vocab

    def test_trigrams(self):
        """Test trigram extraction."""
        docs = ["من به دانشگاه می روم"]

        ngram = NgramExtractor(n=3)
        vectors = ngram.fit_transform(docs)

        vocab = ngram.get_feature_names()
        assert 'من به دانشگاه' in vocab
        assert 'به دانشگاه می' in vocab

    def test_max_features(self):
        """Test max features limit."""
        docs = ["یک دو سه چهار پنج شش"]

        ngram = NgramExtractor(n=2, max_features=3)
        ngram.fit(docs)

        vocab = ngram.get_feature_names()
        assert len(vocab) == 3

    def test_ngram_counts(self):
        """Test n-gram count in vector."""
        docs = ["من من من به به"]

        ngram = NgramExtractor(n=2)
        vectors = ngram.fit_transform(docs)

        vocab = ngram.vocabulary
        # 'من من' appears twice
        if 'من من' in vocab:
            idx = vocab['من من']
            assert vectors[0][idx] == 2

    def test_short_text(self):
        """Test with text shorter than n."""
        docs = ["سلام"]

        ngram = NgramExtractor(n=2)
        vectors = ngram.fit_transform(docs)

        # Should handle gracefully (no bigrams possible)
        vocab = ngram.get_feature_names()
        assert len(vocab) == 0

    def test_unfitted_transform(self):
        """Test transform before fit raises error."""
        ngram = NgramExtractor(n=2)

        with pytest.raises(ValueError):
            ngram.transform(["test"])

    def test_fit_and_transform_separately(self):
        """Test separate fit and transform."""
        train_docs = ["سلام دنیا", "سلام ایران"]
        test_docs = ["سلام"]

        ngram = NgramExtractor(n=2)
        ngram.fit(train_docs)
        vectors = ngram.transform(test_docs)

        assert len(vectors) == 1
        assert ngram._is_fitted
