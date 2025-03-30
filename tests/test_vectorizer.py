import pytest
import numpy as np
from bidnlp.fe.vectorizer import TextVectorizer

@pytest.fixture
def sample_texts_en():
    return [
        "Machine learning is amazing.",
        "Deep learning is a subset of machine learning.",
        "Artificial Intelligence is the future."
    ]

@pytest.fixture
def sample_texts_fa():
    return [
        "یادگیری ماشین شگفت‌انگیز است.",
        "یادگیری عمیق زیرمجموعه‌ای از یادگیری ماشین است.",
        "هوش مصنوعی آینده است."
    ]

@pytest.mark.parametrize("language, texts", [("en", "sample_texts_en"), ("fa", "sample_texts_fa")])
def test_bow_vectorizer(language, texts, request):
    sample_texts = request.getfixturevalue(texts)
    vectorizer = TextVectorizer(method="bow", max_features=10)
    vectorizer.fit(sample_texts)
    transformed = vectorizer.transform(sample_texts[0])
    assert transformed.shape == (1, 10)
    assert isinstance(transformed, np.ndarray)

@pytest.mark.parametrize("language, texts", [("en", "sample_texts_en"), ("fa", "sample_texts_fa")])
def test_tfidf_vectorizer(language, texts, request):
    sample_texts = request.getfixturevalue(texts)
    vectorizer = TextVectorizer(method="tfidf", max_features=10)
    vectorizer.fit(sample_texts)
    transformed = vectorizer.transform(sample_texts[0])
    assert transformed.shape == (1, 10)
    assert isinstance(transformed, np.ndarray)