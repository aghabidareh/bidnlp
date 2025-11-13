"""
Tests for Base POS Tagger
"""

import unittest
from bidnlp.pos import BasePOSTagger


class ConcretePOSTagger(BasePOSTagger):
    """Concrete implementation for testing."""

    def tag(self, text):
        """Simple mock implementation."""
        words = self.tokenize(text)
        return [(word, "N") for word in words]


class TestBasePOSTagger(unittest.TestCase):
    """Test cases for BasePOSTagger."""

    def setUp(self):
        """Set up test fixtures."""
        self.tagger = ConcretePOSTagger()

    def test_initialization(self):
        """Test base tagger initialization."""
        self.assertIsNotNone(self.tagger)
        self.assertTrue(self.tagger.normalize)
        self.assertFalse(self.tagger.is_trained())

    def test_initialization_with_params(self):
        """Test initialization with parameters."""
        tagger = ConcretePOSTagger(normalize=False)
        self.assertFalse(tagger.normalize)

    def test_preprocess_empty(self):
        """Test preprocessing empty text."""
        result = self.tagger.preprocess("")
        self.assertEqual(result, "")

    def test_preprocess_text(self):
        """Test preprocessing text."""
        text = "این یک متن است"
        result = self.tagger.preprocess(text)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_tokenize(self):
        """Test tokenization."""
        text = "من به خانه می‌روم"
        tokens = self.tagger.tokenize(text)

        self.assertIsInstance(tokens, list)
        self.assertGreater(len(tokens), 0)
        self.assertTrue(all(isinstance(token, str) for token in tokens))

    def test_tokenize_empty(self):
        """Test tokenizing empty text."""
        tokens = self.tagger.tokenize("")
        self.assertIsInstance(tokens, list)

    def test_tag_abstract_method(self):
        """Test that tag method is implemented."""
        text = "من به خانه می‌روم"
        result = self.tagger.tag(text)

        # Should return list of tuples
        self.assertIsInstance(result, list)
        if result:
            self.assertTrue(all(isinstance(item, tuple) for item in result))

    def test_tag_words(self):
        """Test tagging list of words."""
        words = ["من", "به", "خانه"]
        result = self.tagger.tag_words(words)

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_tag_batch(self):
        """Test batch tagging."""
        texts = [
            "من به خانه می‌روم",
            "کتاب خوب است"
        ]
        results = self.tagger.tag_batch(texts)

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 2)
        self.assertTrue(all(isinstance(result, list) for result in results))

    def test_tag_batch_empty(self):
        """Test batch tagging with empty list."""
        results = self.tagger.tag_batch([])
        self.assertEqual(results, [])

    def test_get_tags(self):
        """Test getting only tags."""
        text = "من به خانه می‌روم"
        tags = self.tagger.get_tags(text)

        self.assertIsInstance(tags, list)
        self.assertGreater(len(tags), 0)
        self.assertTrue(all(isinstance(tag, str) for tag in tags))

    def test_get_tags_empty(self):
        """Test getting tags from empty text."""
        tags = self.tagger.get_tags("")
        self.assertIsInstance(tags, list)

    def test_get_words_by_tag(self):
        """Test getting words by specific tag."""
        text = "من به خانه می‌روم"
        words = self.tagger.get_words_by_tag(text, "N")

        self.assertIsInstance(words, list)
        self.assertTrue(all(isinstance(word, str) for word in words))

    def test_get_words_by_tag_nonexistent(self):
        """Test getting words by non-existent tag."""
        text = "من به خانه می‌روم"
        words = self.tagger.get_words_by_tag(text, "NONEXISTENT")

        self.assertIsInstance(words, list)
        self.assertEqual(len(words), 0)

    def test_get_tag_counts(self):
        """Test getting tag counts."""
        text = "من به خانه می‌روم"
        counts = self.tagger.get_tag_counts(text)

        self.assertIsInstance(counts, dict)
        self.assertTrue(all(isinstance(tag, str) for tag in counts.keys()))
        self.assertTrue(all(isinstance(count, int) for count in counts.values()))
        self.assertTrue(all(count > 0 for count in counts.values()))

    def test_get_tag_counts_empty(self):
        """Test getting tag counts from empty text."""
        counts = self.tagger.get_tag_counts("")
        self.assertIsInstance(counts, dict)
        self.assertEqual(len(counts), 0)

    def test_get_tag_distribution(self):
        """Test getting tag distribution."""
        text = "من به خانه می‌روم"
        distribution = self.tagger.get_tag_distribution(text)

        self.assertIsInstance(distribution, dict)
        # Sum should be approximately 1.0
        if distribution:
            self.assertAlmostEqual(sum(distribution.values()), 1.0, places=2)
        self.assertTrue(all(0 <= prob <= 1 for prob in distribution.values()))

    def test_get_tag_distribution_empty(self):
        """Test getting distribution from empty text."""
        distribution = self.tagger.get_tag_distribution("")
        self.assertIsInstance(distribution, dict)
        self.assertEqual(len(distribution), 0)

    def test_is_trained(self):
        """Test is_trained method."""
        self.assertFalse(self.tagger.is_trained())

        # Simulate training
        self.tagger._is_trained = True
        self.assertTrue(self.tagger.is_trained())

    def test_get_params(self):
        """Test getting parameters."""
        params = self.tagger.get_params()

        self.assertIsInstance(params, dict)
        self.assertIn('normalize', params)
        self.assertIn('is_trained', params)
        self.assertTrue(params['normalize'])
        self.assertFalse(params['is_trained'])

    def test_set_params(self):
        """Test setting parameters."""
        self.tagger.set_params(normalize=False)
        self.assertFalse(self.tagger.normalize)

        self.tagger.set_params(normalize=True)
        self.assertTrue(self.tagger.normalize)

        # Test setting is_trained
        self.tagger.set_params(_is_trained=True)
        self.assertTrue(self.tagger._is_trained)

    def test_set_params_invalid(self):
        """Test setting invalid parameters."""
        # Should not raise error, just ignore
        self.tagger.set_params(invalid_param="value")
        self.assertFalse(hasattr(self.tagger, 'invalid_param'))

    def test_evaluate(self):
        """Test evaluation method."""
        texts = ["من به خانه می‌روم", "کتاب خوب است"]
        # Create true tags matching the number of tokens
        true_tags = [
            ["N", "N", "N", "N"],  # 4 tags for first sentence
            ["N", "N", "N"]         # 3 tags for second sentence
        ]

        metrics = self.tagger.evaluate(texts, true_tags)

        self.assertIsInstance(metrics, dict)
        self.assertIn('accuracy', metrics)
        self.assertIn('total_tags', metrics)
        self.assertIn('correct_tags', metrics)
        self.assertGreaterEqual(metrics['accuracy'], 0)
        self.assertLessEqual(metrics['accuracy'], 1)
        self.assertGreater(metrics['total_tags'], 0)

    def test_evaluate_empty(self):
        """Test evaluation with empty data."""
        metrics = self.tagger.evaluate([], [])

        self.assertEqual(metrics['accuracy'], 0.0)
        self.assertEqual(metrics['total_tags'], 0)
        self.assertEqual(metrics['correct_tags'], 0)

    def test_evaluate_perfect_accuracy(self):
        """Test evaluation with perfect accuracy."""
        texts = ["کتاب خوب"]
        # Get actual tags from tagger
        actual_tagged = self.tagger.tag(texts[0])
        true_tags = [[tag for word, tag in actual_tagged]]

        metrics = self.tagger.evaluate(texts, true_tags)

        self.assertEqual(metrics['accuracy'], 1.0)

    def test_preprocess_normalization(self):
        """Test that preprocessing normalizes when enabled."""
        tagger = ConcretePOSTagger(normalize=True)
        # Arabic 'ك' should be handled
        result = tagger.preprocess("كتاب")
        self.assertIsInstance(result, str)

    def test_preprocess_no_normalization(self):
        """Test that preprocessing doesn't normalize when disabled."""
        tagger = ConcretePOSTagger(normalize=False)
        text = "كتاب"
        result = tagger.preprocess(text)
        self.assertIsInstance(result, str)


if __name__ == '__main__':
    unittest.main()
