import pytest
from bidnlp.fe.text_stats import TextStats


@pytest.fixture
def sample_text_en():
    return "Natural Language Processing is fascinating!"


@pytest.fixture
def sample_text_fa():
    return "پردازش زبان طبیعی جذاب است!"


@pytest.mark.parametrize('text', ['sample_text_en', 'sample_text_fa'])
def test_char_count(text, request):
    sample_text = request.getfixturevalue(text)
    assert TextStats.char_count(sample_text) == len(sample_text)


@pytest.mark.parametrize('text, expected', [('sample_text_en', 5), ('sample_text_fa', 4)])
def test_word_count(text, expected, request):
    sample_text = request.getfixturevalue(text)
    assert TextStats.word_count(sample_text) == expected


@pytest.mark.parametrize("text", ["sample_text_en", "sample_text_fa"])
def test_avg_word_length(text, request):
    sample_text = request.getfixturevalue(text)
    words = sample_text.split()
    assert round(TextStats.average_word_length(sample_text), 2) == round(sum(len(w) for w in words) / len(words), 2)
