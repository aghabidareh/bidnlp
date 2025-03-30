import pytest
from bidnlp.fe.text_stats import TextStats

@pytest.fixture
def sample_text_en():
    return "Natural Language Processing is fascinating!"

@pytest.fixture
def sample_text_fa():
    return "پردازش زبان طبیعی جذاب است!"

@pytest.mark.parametrize('text' , ['sample_text_en', 'sample_text_fa'])
def test_char_count(text , request):
    sample_text = request.getfixturevalue(text)
    assert sample_text.char_count == len(sample_text)
