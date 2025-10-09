# BidNLP

**A Comprehensive Persian (Farsi) Natural Language Processing Library**

BidNLP is a production-ready Python library for Persian text processing, offering a complete suite of NLP tools specifically designed for the unique challenges of Persian language processing.

[![CI](https://github.com/aghabidareh/bidnlp/actions/workflows/ci.yml/badge.svg)](https://github.com/aghabidareh/bidnlp/actions/workflows/ci.yml)
[![CodeQL](https://github.com/aghabidareh/bidnlp/actions/workflows/codeql.yml/badge.svg)](https://github.com/aghabidareh/bidnlp/actions/workflows/codeql.yml)
[![codecov](https://codecov.io/gh/aghabidareh/bidnlp/branch/master/graph/badge.svg)](https://codecov.io/gh/aghabidareh/bidnlp)
[![PyPI version](https://badge.fury.io/py/bidnlp.svg)](https://badge.fury.io/py/bidnlp)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/bidnlp)](https://pepy.tech/project/bidnlp)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## ✨ Features

### 🔧 Preprocessing (100% Complete)
- **Text Normalization**: Arabic to Persian character conversion, diacritic removal, ZWNJ normalization
- **Text Cleaning**: URL, email, HTML tag removal, emoji handling
- **Number Processing**: Persian ↔ English ↔ Arabic-Indic digit conversion
- **Date Normalization**: Jalali date handling and formatting
- **Punctuation**: Persian and Latin punctuation normalization

### ✂️ Tokenization (100% Complete)
- **Word Tokenizer**: ZWNJ-aware, handles compound words and mixed scripts
- **Sentence Tokenizer**: Smart boundary detection with abbreviation support
- **Character Tokenizer**: Character-level tokenization with diacritic handling
- **Morpheme Tokenizer**: Prefix/suffix detection and morphological analysis
- **Syllable Tokenizer**: Persian syllable segmentation

### 🔍 Stemming & Lemmatization (Partial)
- **Stemming**: Conservative suffix removal with minimum stem length
- **Lemmatization**: Dictionary-based lemmatization with irregular form support
- **Arabic Plural Handling**: Special support for Arabic broken plurals

### 📊 Classification (100% Complete)
- **Sentiment Analysis**: Keyword-based with 100+ sentiment keywords and negation handling
- **Text Classification**: Keyword-based multi-class categorization
- **Feature Extraction**: Bag-of-Words, TF-IDF, N-gram extraction

### 🛠️ Utilities (100% Complete)
- **Character Utils**: Persian alphabet, character type detection, diacritic handling
- **Statistics**: Word count, sentence count, lexical diversity, n-gram frequency
- **Stop Words**: 100+ Persian stop words with custom support
- **Validators**: Text quality scoring, normalization checking
- **Metrics**: Precision, Recall, F1, BLEU, edit distance, and more

## 📦 Installation

```bash
pip install bidnlp
```

**From source:**
```bash
git clone https://github.com/aghabidareh/bidnlp.git
cd bidnlp
pip install -e .
```

## 🚀 Quick Start

### Preprocessing

```python
from bidnlp.preprocessing import PersianNormalizer, PersianTextCleaner

# Normalize text
normalizer = PersianNormalizer()
text = normalizer.normalize("كتاب يک")  # Converts: کتاب یک

# Clean text
cleaner = PersianTextCleaner(remove_urls=True, remove_emojis=True)
clean_text = cleaner.clean("سلام 😊 https://test.com")  # Output: سلام
```

### Tokenization

```python
from bidnlp.tokenization import PersianWordTokenizer, PersianSentenceTokenizer

# Word tokenization
tokenizer = PersianWordTokenizer()
words = tokenizer.tokenize("من به دانشگاه می‌روم")
# Output: ['من', 'به', 'دانشگاه', 'می', 'روم']

# Sentence tokenization
sent_tokenizer = PersianSentenceTokenizer()
sentences = sent_tokenizer.tokenize("سلام. چطوری؟")
# Output: ['سلام.', 'چطوری؟']
```

### Sentiment Analysis

```python
from bidnlp.classification import PersianSentimentAnalyzer

analyzer = PersianSentimentAnalyzer()

# Simple sentiment
sentiment = analyzer.predict("این کتاب خیلی خوب است")
# Output: 'positive'

# Detailed analysis
result = analyzer.analyze("محصول عالی اما گران است")
# Output: {'sentiment': 'neutral', 'score': 0.0,
#          'positive_words': ['عالی'], 'negative_words': ['گران']}
```

### Text Classification

```python
from bidnlp.classification import KeywordClassifier

classifier = KeywordClassifier()

# Add categories
classifier.add_category('ورزش', {'فوتبال', 'بازیکن', 'تیم'})
classifier.add_category('تکنولوژی', {'کامپیوتر', 'نرم‌افزار', 'برنامه'})

# Classify
category = classifier.predict("تیم فوتبال برد گرفت")
# Output: 'ورزش'
```

### Text Statistics

```python
from bidnlp.utils import PersianTextStatistics

stats = PersianTextStatistics()
text = "من به دانشگاه می‌روم. دانشگاه بزرگ است."

statistics = stats.get_statistics(text)
# Output: {
#   'words': 8, 'sentences': 2, 'characters': 35,
#   'average_word_length': 4.38, 'lexical_diversity': 0.875, ...
# }
```

### Stop Words

```python
from bidnlp.utils import PersianStopWords

stopwords = PersianStopWords()

# Remove stop words
text = "من از دانشگاه به خانه می روم"
filtered = stopwords.remove_stopwords(text)
# Output: "دانشگاه خانه می روم"

# Check if word is stop word
is_stop = stopwords.is_stopword('از')  # True
```

### Feature Extraction

```python
from bidnlp.classification import TfidfVectorizer, BagOfWords

# TF-IDF
tfidf = TfidfVectorizer(max_features=100)
vectors = tfidf.fit_transform(documents)

# Bag of Words
bow = BagOfWords(max_features=50)
vectors = bow.fit_transform(documents)
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific module tests
pytest tests/preprocessing/ -v
pytest tests/tokenization/ -v
pytest tests/classification/ -v
pytest tests/utils/ -v

# Run with coverage
pytest tests/ --cov=bidnlp
```

## 📊 Project Status

| Module | Status | Tests | Coverage |
|--------|--------|-------|----------|
| Preprocessing | ✅ Complete | 58/58 | 100% |
| Tokenization | ✅ Complete | 64/64 | 100% |
| Classification | ✅ Complete | 46/46 | 100% |
| Utils | ✅ Complete | 117/117 | 100% |
| Stemming | 🟡 Partial | 11/14 | 79% |
| Lemmatization | 🟡 Partial | 11/22 | 50% |
| **Overall** | **✅ 93.8%** | **307/321** | **93.8%** |

## 🎯 Key Features

- **Persian-Specific**: Designed specifically for Persian language challenges
- **ZWNJ Handling**: Proper handling of zero-width non-joiner characters
- **Mixed Script Support**: Handles Persian, Arabic, and English text
- **Production Ready**: 93.8% test coverage with comprehensive testing
- **Easy to Use**: Simple, intuitive API with extensive documentation
- **Extensible**: Easy to extend and customize for your needs

## 🌟 Use Cases

- **Text Preprocessing**: Clean and normalize Persian text for ML pipelines
- **Sentiment Analysis**: Analyze sentiment in Persian reviews and social media
- **Text Classification**: Categorize Persian documents and news articles
- **Information Extraction**: Extract meaningful information from Persian text
- **Search & Retrieval**: Build Persian search engines with proper tokenization
- **NLP Research**: Foundation for Persian NLP research and experiments

## 🔄 CI/CD & Quality Assurance

BidNLP uses comprehensive automated workflows to ensure code quality and reliability:

### Continuous Integration
- ✅ **Multi-version Testing**: Automated tests across Python 3.7-3.12 on Ubuntu, macOS, and Windows
- ✅ **Code Coverage**: Comprehensive coverage reporting with Codecov integration
- ✅ **Code Quality**: Automated checks with Black, isort, flake8, and mypy
- ✅ **Security Scanning**: Regular security audits with Bandit, Safety, and CodeQL
- ✅ **Dependency Updates**: Automated dependency management with Dependabot

### Release Pipeline
- ✅ **Automated PyPI Publishing**: Seamless releases on version tags
- ✅ **GitHub Releases**: Automatic changelog and artifact generation
- ✅ **Package Validation**: Pre-release checks ensure package integrity

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

**Quick Start:**

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes and add tests
4. Ensure all tests pass (`pytest tests/`)
5. Format code (`black . && isort .`)
6. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
7. Push to the branch (`git push origin feature/AmazingFeature`)
8. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all contributors who have helped build this library
- Inspired by the need for comprehensive Persian NLP tools
- Built with ❤️ for the Persian NLP community

## 📧 Contact

For questions, issues, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for Persian NLP**
