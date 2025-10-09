# Contributing to BidNLP

First off, thank you for considering contributing to BidNLP! It's people like you that make BidNLP such a great tool for the Persian NLP community.

## Code of Conduct

This project and everyone participating in it is governed by respect and professionalism. By participating, you are expected to uphold this standard.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps to reproduce the problem**
* **Provide specific examples** (code snippets, input/output)
* **Describe the behavior you observed and what you expected**
* **Include your environment details** (Python version, OS, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

* **Use a clear and descriptive title**
* **Provide a detailed description of the proposed functionality**
* **Explain why this enhancement would be useful**
* **List any similar features in other libraries**

### Pull Requests

1. Fork the repository
2. Create a new branch from `master` (`git checkout -b feature/amazing-feature`)
3. Make your changes following our style guide
4. Add tests for your changes
5. Ensure all tests pass (`pytest tests/`)
6. Update documentation if needed
7. Commit your changes (`git commit -m 'Add some amazing feature'`)
8. Push to your branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/bidnlp.git
cd bidnlp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e .
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run code formatting
black bidnlp/ tests/
isort bidnlp/ tests/

# Run linting
flake8 bidnlp/
mypy bidnlp/
```

## Style Guide

### Python Code Style

We follow PEP 8 with some modifications:

* Line length: 100 characters (enforced by Black)
* Use Black for code formatting
* Use isort for import sorting
* Use type hints where possible
* Write docstrings for all public modules, functions, classes, and methods

### Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters
* Reference issues and pull requests liberally after the first line

Example:
```
Add Persian verb lemmatization support

- Implement irregular verb dictionary
- Add present to past stem conversion
- Update tests for verb handling

Fixes #123
```

### Testing

* Write tests for all new features
* Ensure all tests pass before submitting PR
* Aim for >80% code coverage for new code
* Use descriptive test names
* Follow the existing test structure

```python
def test_feature_does_something_expected():
    """Test that feature behaves correctly under normal conditions."""
    # Arrange
    input_text = "test input"

    # Act
    result = some_function(input_text)

    # Assert
    assert result == expected_output
```

### Documentation

* Update README.md for new features
* Add docstrings to all public APIs
* Update examples/ if adding new functionality
* Keep CHANGELOG.md updated

## Project Structure

```
bidnlp/
├── bidnlp/              # Main package
│   ├── preprocessing/   # Text preprocessing
│   ├── tokenization/    # Tokenizers
│   ├── stemming/        # Stemming
│   ├── lemmatization/   # Lemmatization
│   ├── classification/  # Classification & sentiment
│   └── utils/           # Utilities
├── tests/               # Test suite
├── examples/            # Usage examples
└── docs/                # Documentation
```

## Testing Guidelines

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific module
pytest tests/preprocessing/ -v

# Run with coverage
pytest tests/ --cov=bidnlp --cov-report=html

# Run in parallel
pytest tests/ -n auto
```

### Test Organization

* Mirror the package structure in tests/
* One test file per module
* Group related tests in test classes
* Use fixtures for common setup

## Persian NLP Considerations

When contributing, keep these Persian language specifics in mind:

1. **ZWNJ Handling**: Always consider zero-width non-joiner (‌ / U+200C)
2. **Arabic vs Persian**: Handle both character sets (ك vs ک, ي vs ی)
3. **Number Systems**: Support Persian (۰-۹), Arabic-Indic (٠-٩), and English (0-9)
4. **RTL Support**: Consider right-to-left text rendering
5. **Diacritics**: Handle optional diacritics properly

## Code Review Process

1. At least one maintainer review is required
2. All CI checks must pass
3. Code coverage should not decrease
4. Documentation must be updated
5. Semantic versioning is followed

## Release Process

Releases are automated via GitHub Actions:

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create and push a version tag: `git tag -a v1.0.0 -m "Release v1.0.0"`
4. GitHub Actions will automatically:
   - Run all tests
   - Build the package
   - Publish to PyPI
   - Create GitHub release

## Recognition

Contributors will be recognized in:
* README.md acknowledgments section
* Release notes
* GitHub contributors page

## Questions?

Feel free to open an issue with the label `question` or reach out to the maintainers.

---

**Thank you for contributing to BidNLP!** 🎉
