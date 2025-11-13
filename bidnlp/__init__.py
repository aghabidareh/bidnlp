"""
BidNLP - Persian (Farsi) Natural Language Processing Library
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from . import preprocessing
from . import stemming
from . import lemmatization
from . import classification
from . import tokenization
from . import utils
from . import pos

__all__ = [
    "preprocessing",
    "stemming",
    "lemmatization",
    "classification",
    "tokenization",
    "utils",
    "pos",
]
