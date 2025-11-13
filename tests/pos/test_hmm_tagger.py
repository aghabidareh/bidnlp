"""
Tests for HMM-Based Persian POS Tagger
"""

import unittest
from bidnlp.pos import HMMPOSTagger, PersianPOSTag


class TestHMMPOSTagger(unittest.TestCase):
    """Test cases for HMMPOSTagger."""

    def setUp(self):
        """Set up test fixtures."""
        self.tagger = HMMPOSTagger()

        # Training data
        self.training_data = [
            [("من", "PRO_PERS"), ("به", "PREP"), ("خانه", "N"), ("می‌روم", "V_PRES")],
            [("او", "PRO_PERS"), ("کتاب", "N"), ("می‌خواند", "V_PRES")],
            [("این", "PRO_DEM"), ("خوب", "ADJ"), ("است", "V_AUX")],
            [("ما", "PRO_PERS"), ("در", "PREP"), ("دانشگاه", "N"), ("هستیم", "V_AUX")],
            [("آنها", "PRO_PERS"), ("امروز", "ADV_TIME"), ("آمدند", "V_PAST")],
        ]

    def test_initialization(self):
        """Test tagger initialization."""
        self.assertIsNotNone(self.tagger)
        self.assertTrue(self.tagger.normalize)
        self.assertFalse(self.tagger.is_trained())  # Not trained initially
        self.assertGreater(self.tagger.smoothing, 0)

    def test_train_basic(self):
        """Test basic training."""
        self.tagger.train(self.training_data)

        self.assertTrue(self.tagger.is_trained())
        self.assertGreater(len(self.tagger.tagset), 0)
        self.assertGreater(len(self.tagger.vocabulary), 0)

    def test_train_empty_data(self):
        """Test training with empty data."""
        self.tagger.train([])
        # Should still mark as trained even with no data
        self.assertTrue(self.tagger.is_trained())

    def test_tag_before_training(self):
        """Test that tagging fails before training."""
        with self.assertRaises(ValueError):
            self.tagger.tag("من به خانه می‌روم")

    def test_tag_after_training(self):
        """Test tagging after training."""
        self.tagger.train(self.training_data)

        text = "من به خانه می‌روم"
        result = self.tagger.tag(text)

        self.assertGreater(len(result), 0)
        self.assertTrue(all(isinstance(item, tuple) and len(item) == 2
                           for item in result))

    def test_tag_empty_text(self):
        """Test tagging empty text."""
        self.tagger.train(self.training_data)
        result = self.tagger.tag("")
        self.assertEqual(result, [])

    def test_tag_known_words(self):
        """Test tagging with known words."""
        self.tagger.train(self.training_data)

        # Test individual known words
        result = self.tagger.tag("من")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "من")
        # Should recognize it as pronoun
        self.assertIn(result[0][1], self.tagger.tagset)

    def test_tag_unknown_words(self):
        """Test tagging with unknown words."""
        self.tagger.train(self.training_data)

        # Test unknown word
        result = self.tagger.tag("ناشناخته")
        self.assertGreater(len(result), 0)
        # Should still assign some tag
        self.assertTrue(all(tag in self.tagger.tagset for word, tag in result))

    def test_tag_mixed_sentence(self):
        """Test tagging sentence with known and unknown words."""
        self.tagger.train(self.training_data)

        text = "من کتاب جدید می‌خوانم"
        result = self.tagger.tag(text)

        self.assertGreater(len(result), 0)
        # Should tag all words
        words = [word for word, tag in result]
        self.assertIn("من", words)
        self.assertIn("کتاب", words)

    def test_transition_probabilities(self):
        """Test transition probability calculation."""
        self.tagger.train(self.training_data)

        # Check that transition probabilities exist
        self.assertGreater(len(self.tagger.transition_probs), 0)

        # Probability should be between 0 and 1
        for prev_tag, next_tags in self.tagger.transition_probs.items():
            for next_tag, prob in next_tags.items():
                self.assertGreaterEqual(prob, 0)
                self.assertLessEqual(prob, 1)

    def test_emission_probabilities(self):
        """Test emission probability calculation."""
        self.tagger.train(self.training_data)

        # Check that emission probabilities exist
        self.assertGreater(len(self.tagger.emission_probs), 0)

        # Probability should be between 0 and 1
        for tag, words in self.tagger.emission_probs.items():
            for word, prob in words.items():
                self.assertGreaterEqual(prob, 0)
                self.assertLessEqual(prob, 1)

    def test_get_transition_prob(self):
        """Test getting specific transition probability."""
        self.tagger.train(self.training_data)

        prob = self.tagger.get_transition_prob("PRO_PERS", "PREP")
        self.assertGreaterEqual(prob, 0)

    def test_get_emission_prob(self):
        """Test getting specific emission probability."""
        self.tagger.train(self.training_data)

        prob = self.tagger.get_emission_prob("PRO_PERS", "من")
        self.assertGreater(prob, 0)  # Should have positive probability for known word

        prob = self.tagger.get_emission_prob("N", "ناشناخته")
        self.assertGreaterEqual(prob, 0)  # Unknown word should use smoothing

    def test_get_most_likely_tag(self):
        """Test getting most likely tag for a word."""
        self.tagger.train(self.training_data)

        tag = self.tagger.get_most_likely_tag("من")
        self.assertIn(tag, self.tagger.tagset)
        # Should be pronoun
        self.assertEqual(tag, "PRO_PERS")

    def test_get_tags(self):
        """Test getting only tags."""
        self.tagger.train(self.training_data)

        text = "من به خانه می‌روم"
        tags = self.tagger.get_tags(text)

        self.assertGreater(len(tags), 0)
        self.assertTrue(all(isinstance(tag, str) for tag in tags))
        self.assertTrue(all(tag in self.tagger.tagset for tag in tags))

    def test_get_words_by_tag(self):
        """Test getting words by specific tag."""
        self.tagger.train(self.training_data)

        text = "من به خانه می‌روم"
        tagged = self.tagger.tag(text)

        # Get all tags present
        all_tags = set(tag for word, tag in tagged)

        for tag in all_tags:
            words = self.tagger.get_words_by_tag(text, tag)
            self.assertIsInstance(words, list)

    def test_get_tag_counts(self):
        """Test getting tag counts."""
        self.tagger.train(self.training_data)

        text = "من به خانه می‌روم"
        counts = self.tagger.get_tag_counts(text)

        self.assertIsInstance(counts, dict)
        self.assertGreater(len(counts), 0)
        self.assertTrue(all(isinstance(count, int) for count in counts.values()))

    def test_get_tag_distribution(self):
        """Test getting tag distribution."""
        self.tagger.train(self.training_data)

        text = "من به خانه می‌روم"
        distribution = self.tagger.get_tag_distribution(text)

        self.assertIsInstance(distribution, dict)
        self.assertGreater(len(distribution), 0)
        # All proportions should sum to 1.0
        self.assertAlmostEqual(sum(distribution.values()), 1.0, places=2)

    def test_tag_batch(self):
        """Test batch tagging."""
        self.tagger.train(self.training_data)

        texts = [
            "من به خانه می‌روم",
            "کتاب خوب است"
        ]
        results = self.tagger.tag_batch(texts)

        self.assertEqual(len(results), 2)
        self.assertTrue(all(isinstance(result, list) for result in results))
        self.assertTrue(all(len(result) > 0 for result in results))

    def test_tag_words(self):
        """Test tagging a list of words."""
        self.tagger.train(self.training_data)

        words = ["من", "به", "خانه", "می‌روم"]
        tagged = self.tagger.tag_words(words)

        self.assertGreater(len(tagged), 0)
        self.assertTrue(all(isinstance(item, tuple) and len(item) == 2
                           for item in tagged))

    def test_smoothing_effect(self):
        """Test that smoothing affects unknown words."""
        # Test with different smoothing values
        tagger1 = HMMPOSTagger(smoothing=1e-10)
        tagger2 = HMMPOSTagger(smoothing=1e-5)

        tagger1.train(self.training_data)
        tagger2.train(self.training_data)

        # Both should handle unknown words
        text = "ناشناخته"
        result1 = tagger1.tag(text)
        result2 = tagger2.tag(text)

        self.assertGreater(len(result1), 0)
        self.assertGreater(len(result2), 0)

    def test_save_model(self):
        """Test saving model parameters."""
        self.tagger.train(self.training_data)

        model_data = self.tagger.save_model()

        self.assertIsInstance(model_data, dict)
        self.assertIn('transition_probs', model_data)
        self.assertIn('emission_probs', model_data)
        self.assertIn('tag_counts', model_data)
        self.assertIn('vocabulary', model_data)
        self.assertIn('tagset', model_data)
        self.assertIn('smoothing', model_data)
        self.assertIn('is_trained', model_data)

    def test_load_model(self):
        """Test loading model parameters."""
        self.tagger.train(self.training_data)

        # Save model
        model_data = self.tagger.save_model()

        # Create new tagger and load
        new_tagger = HMMPOSTagger()
        self.assertFalse(new_tagger.is_trained())

        new_tagger.load_model(model_data)
        self.assertTrue(new_tagger.is_trained())

        # Should produce same results
        text = "من به خانه می‌روم"
        result1 = self.tagger.tag(text)
        result2 = new_tagger.tag(text)

        self.assertEqual(len(result1), len(result2))

    def test_evaluate(self):
        """Test model evaluation."""
        self.tagger.train(self.training_data)

        # Test data
        test_texts = ["من به خانه می‌روم"]
        true_tags = [["PRO_PERS", "PREP", "N", "V_PRES"]]

        metrics = self.tagger.evaluate(test_texts, true_tags)

        self.assertIn('accuracy', metrics)
        self.assertIn('total_tags', metrics)
        self.assertIn('correct_tags', metrics)
        self.assertGreaterEqual(metrics['accuracy'], 0)
        self.assertLessEqual(metrics['accuracy'], 1)

    def test_get_params(self):
        """Test getting tagger parameters."""
        params = self.tagger.get_params()

        self.assertIn('normalize', params)
        self.assertIn('is_trained', params)
        self.assertFalse(params['is_trained'])

    def test_set_params(self):
        """Test setting tagger parameters."""
        self.tagger.set_params(normalize=False)
        self.assertFalse(self.tagger.normalize)

        self.tagger.set_params(normalize=True)
        self.assertTrue(self.tagger.normalize)

    def test_larger_training_set(self):
        """Test with larger training set."""
        # Create larger training set
        large_training_data = self.training_data * 10  # Repeat data

        self.tagger.train(large_training_data)

        self.assertTrue(self.tagger.is_trained())

        text = "من به دانشگاه می‌روم"
        result = self.tagger.tag(text)

        self.assertGreater(len(result), 0)

    def test_vocabulary_expansion(self):
        """Test that vocabulary expands with training."""
        self.tagger.train(self.training_data)

        initial_vocab_size = len(self.tagger.vocabulary)

        # Add more training data
        additional_data = [
            [("شما", "PRO_PERS"), ("کجا", "PRO_INT"), ("می‌روید", "V_PRES")],
        ]

        self.tagger.train(self.training_data + additional_data)

        # Vocabulary should expand
        self.assertGreaterEqual(len(self.tagger.vocabulary), initial_vocab_size)

    def test_normalization_enabled(self):
        """Test that normalization works when enabled."""
        tagger = HMMPOSTagger(normalize=True)
        tagger.train(self.training_data)

        result = tagger.tag("من")
        self.assertGreater(len(result), 0)

    def test_normalization_disabled(self):
        """Test that normalization can be disabled."""
        tagger = HMMPOSTagger(normalize=False)
        tagger.train(self.training_data)

        result = tagger.tag("من")
        self.assertGreater(len(result), 0)

    def test_viterbi_consistency(self):
        """Test that Viterbi produces consistent results."""
        self.tagger.train(self.training_data)

        text = "من به خانه می‌روم"

        # Tag same text multiple times
        result1 = self.tagger.tag(text)
        result2 = self.tagger.tag(text)

        # Should produce identical results
        self.assertEqual(result1, result2)

    def test_single_word_sentence(self):
        """Test tagging single word."""
        self.tagger.train(self.training_data)

        result = self.tagger.tag("من")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "من")


if __name__ == '__main__':
    unittest.main()
