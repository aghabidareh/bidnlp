import pytest
from bidnlp.preprocessing import TextPreprocessor

@pytest.fixture
def sample_word_en():
    return "running"

@pytest.fixture
def sample_word_fa():
    return "دویدن"