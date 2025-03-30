import pytest
from bidnlp.preprocessing import TextPreprocessor

@pytest.fixture
def sample_text_en():
    return "This is an example sentence, with punctuation!"

@pytest.fixture
def sample_text_fa():
    return "این یک جمله‌ی نمونه است، با علائم نگارشی!"