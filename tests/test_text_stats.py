import pytest
from bidnlp.fe.text_stats import TextStats

@pytest.fixture
def sample_text_en():
    return "Natural Language Processing is fascinating!"