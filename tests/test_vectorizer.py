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