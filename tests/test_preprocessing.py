import pytest
from bidnlp.preprocessing import TextPreprocessor

@pytest.fixture
def sample_text_en():
    return "This is an example sentence, with punctuation!"

@pytest.fixture
def sample_text_fa():
    return "این یک جمله‌ی نمونه است، با علائم نگارشی!"

def test_remove_punctuation(sample_text_en, sample_text_fa):
    preprocessor = TextPreprocessor()
    assert preprocessor.remove_punctuation(sample_text_en) == "This is an example sentence with punctuation"
    assert preprocessor.remove_punctuation(sample_text_fa) == "این یک جمله‌ی نمونه است با علائم نگارشی"

def test_remove_stopwords(sample_text_en, sample_text_fa):
    preprocessor = TextPreprocessor()
    assert preprocessor.remove_stopwords(sample_text_en) == "example sentence, punctuation!"
    assert preprocessor.remove_stopwords(sample_text_fa) == "جمله‌ی نمونه است، علائم نگارشی!"