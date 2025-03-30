import pytest
from bidnlp.preprocessing import TextPreprocessor

@pytest.fixture
def sample_word_en():
    return "running"

@pytest.fixture
def sample_word_fa():
    return "دویدن"

def test_stemming_en(sample_word_en):
    stemmer = TextPreprocessor(language="en")
    assert stemmer.stem(sample_word_en) == "run"