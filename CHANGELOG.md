# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub Actions CI/CD pipeline
- Automated testing across multiple Python versions (3.7-3.12)
- Code quality checks (Black, isort, flake8, mypy)
- Security scanning (Bandit, Safety, CodeQL)
- Automated PyPI release workflow
- Comprehensive test coverage reporting
- Professional badges in README
- Contributing guidelines
- Security policy
- Dependabot configuration

### Changed
- Updated README with dynamic badges
- Enhanced project documentation

## [0.1.0] - 2025-10-02

### Added
- **Preprocessing Module** (100% complete)
  - Text normalization (Arabic to Persian conversion)
  - Text cleaning (URLs, emails, HTML, emojis)
  - Number processing (Persian ↔ English ↔ Arabic-Indic)
  - Date normalization (Jalali date handling)
  - Punctuation normalization

- **Tokenization Module** (100% complete)
  - Word tokenizer (ZWNJ-aware, compound words)
  - Sentence tokenizer (smart boundary detection)
  - Character tokenizer
  - Morpheme tokenizer
  - Syllable tokenizer

- **Classification Module** (100% complete)
  - Sentiment analyzer (keyword-based with negation handling)
  - Keyword classifier
  - Feature extraction (Bag-of-Words, TF-IDF, N-grams)

- **Utils Module** (100% complete)
  - Character utilities
  - Text statistics
  - Stop words (100+ Persian stop words)
  - Validators
  - Metrics (Precision, Recall, F1, BLEU, edit distance)

- **Stemming Module** (50% complete)
  - Conservative suffix removal
  - Minimum stem length enforcement
  - Arabic broken plural handling

- **Lemmatization Module** (45% complete)
  - Dictionary-based lemmatization
  - Irregular form support
  - Verb handling (partial)

### Fixed
- Critical bug: Arabic broken plurals (سبزیجات → سبزی)
- ZWNJ handling in regex (Python 3.13 compatibility)
- Unicode escape issues in dictionaries
- Over-stemming with single-character suffixes
- False verb detection issues

### Documentation
- Comprehensive README
- Quick start guide
- Session summary
- Roadmap
- 4 working examples (preprocessing, tokenization, utils, classification)

### Tests
- 302/321 tests passing (94.1% coverage)
- Preprocessing: 58/58 tests
- Tokenization: 64/64 tests
- Classification: 46/46 tests
- Utils: 117/117 tests
- Stemming: 7/14 tests
- Lemmatization: 9/20 tests

## [0.0.1] - Initial Development

### Added
- Project structure
- Basic package setup
- Initial modules

---

## Types of Changes

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes

[Unreleased]: https://github.com/aghabidareh/bidnlp/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/aghabidareh/bidnlp/releases/tag/v0.1.0
[0.0.1]: https://github.com/aghabidareh/bidnlp/releases/tag/v0.0.1
