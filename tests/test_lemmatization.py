import pytest
from bidnlp.preprocessing import TextPreprocessor

@pytest.fixture
def sample_word_en():
    return "running"

@pytest.fixture
def sample_word_fa():
    return "می‌روم"

def test_lemmatization_en(sample_word_en):
    lemmatizer = TextPreprocessor(language="en")
    assert lemmatizer.lemmatize(sample_word_en) == "run"