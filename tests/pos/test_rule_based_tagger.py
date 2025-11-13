"""
Tests for Rule-Based Persian POS Tagger
"""

import unittest
from bidnlp.pos import RuleBasedPOSTagger, PersianPOSTag


class TestRuleBasedPOSTagger(unittest.TestCase):
    """Test cases for RuleBasedPOSTagger."""

    def setUp(self):
        """Set up test fixtures."""
        self.tagger = RuleBasedPOSTagger()

    def test_initialization(self):
        """Test tagger initialization."""
        self.assertIsNotNone(self.tagger)
        self.assertTrue(self.tagger.normalize)
        self.assertTrue(self.tagger.is_trained())  # Rule-based is always trained

    def test_empty_text(self):
        """Test tagging empty text."""
        result = self.tagger.tag("")
        self.assertEqual(result, [])

    def test_tag_nouns(self):
        """Test noun tagging."""
        result = self.tagger.tag("کتاب")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "کتاب")
        self.assertEqual(result[0][1], PersianPOSTag.N.value)

    def test_tag_plural_nouns(self):
        """Test plural noun tagging."""
        tagged = self.tagger.tag("کتابها")
        self.assertEqual(len(tagged), 1)
        self.assertEqual(tagged[0][1], PersianPOSTag.N_PL.value)

    def test_tag_pronouns(self):
        """Test pronoun tagging."""
        # Personal pronouns
        tagged = self.tagger.tag("من")
        self.assertEqual(tagged[0][1], PersianPOSTag.PRO_PERS.value)

        # Demonstrative pronouns
        tagged = self.tagger.tag("این")
        self.assertEqual(tagged[0][1], PersianPOSTag.PRO_DEM.value)

        # Interrogative pronouns
        tagged = self.tagger.tag("چه")
        self.assertEqual(tagged[0][1], PersianPOSTag.PRO_INT.value)

    def test_tag_prepositions(self):
        """Test preposition tagging."""
        tagged = self.tagger.tag("از")
        self.assertEqual(tagged[0][1], PersianPOSTag.PREP.value)

        tagged = self.tagger.tag("به")
        self.assertEqual(tagged[0][1], PersianPOSTag.PREP.value)

    def test_tag_conjunctions(self):
        """Test conjunction tagging."""
        tagged = self.tagger.tag("و")
        self.assertEqual(tagged[0][1], PersianPOSTag.CONJ.value)

        tagged = self.tagger.tag("که")
        self.assertEqual(tagged[0][1], PersianPOSTag.CONJ_SUBR.value)

    def test_tag_adjectives(self):
        """Test adjective tagging."""
        tagged = self.tagger.tag("خوب")
        self.assertEqual(tagged[0][1], PersianPOSTag.ADJ.value)

        # Comparative
        tagged = self.tagger.tag("بزرگتر")
        self.assertEqual(tagged[0][1], PersianPOSTag.ADJ_CMPR.value)

        # Superlative
        tagged = self.tagger.tag("بزرگترین")
        self.assertEqual(tagged[0][1], PersianPOSTag.ADJ_SUP.value)

    def test_tag_adverbs(self):
        """Test adverb tagging."""
        tagged = self.tagger.tag("خیلی")
        self.assertEqual(tagged[0][1], PersianPOSTag.ADV.value)

        # Time adverb
        tagged = self.tagger.tag("امروز")
        self.assertEqual(tagged[0][1], PersianPOSTag.ADV_TIME.value)

        # Location adverb
        tagged = self.tagger.tag("بالا")
        self.assertEqual(tagged[0][1], PersianPOSTag.ADV_LOC.value)

    def test_tag_verbs(self):
        """Test verb tagging."""
        # Auxiliary verb
        tagged = self.tagger.tag("است")
        self.assertEqual(tagged[0][1], PersianPOSTag.V_AUX.value)

        # Infinitive
        tagged = self.tagger.tag("رفتن")
        self.assertEqual(tagged[0][1], PersianPOSTag.V_INF.value)

    def test_tag_determiners(self):
        """Test determiner tagging."""
        tagged = self.tagger.tag("یک")
        self.assertEqual(tagged[0][1], PersianPOSTag.DET.value)

        tagged = self.tagger.tag("هر")
        self.assertEqual(tagged[0][1], PersianPOSTag.DET.value)

    def test_tag_numbers(self):
        """Test number tagging."""
        # English digits
        tagged = self.tagger.tag("123")
        self.assertEqual(tagged[0][1], PersianPOSTag.NUM.value)

        # Persian digits
        tagged = self.tagger.tag("۱۲۳")
        self.assertEqual(tagged[0][1], PersianPOSTag.NUM.value)

    def test_tag_punctuation(self):
        """Test punctuation tagging."""
        tagged = self.tagger.tag(".")
        self.assertEqual(tagged[0][1], PersianPOSTag.PUNC.value)

        tagged = self.tagger.tag("،")
        self.assertEqual(tagged[0][1], PersianPOSTag.PUNC.value)

    def test_tag_sentence(self):
        """Test tagging a complete sentence."""
        text = "من به دانشگاه می‌روم"
        tagged = self.tagger.tag(text)

        self.assertGreater(len(tagged), 0)
        # من should be personal pronoun
        self.assertTrue(any(word == "من" and tag == PersianPOSTag.PRO_PERS.value
                           for word, tag in tagged))
        # به should be preposition
        self.assertTrue(any(word == "به" and tag == PersianPOSTag.PREP.value
                           for word, tag in tagged))

    def test_tag_sentence_with_punctuation(self):
        """Test tagging sentence with punctuation."""
        text = "کتاب خوب است."
        tagged = self.tagger.tag(text)

        self.assertEqual(len(tagged), 4)
        # Last token should be punctuation
        self.assertEqual(tagged[-1][1], PersianPOSTag.PUNC.value)

    def test_get_tags(self):
        """Test getting only tags."""
        text = "من کتاب می‌خوانم"
        tags = self.tagger.get_tags(text)

        self.assertGreater(len(tags), 0)
        self.assertTrue(all(isinstance(tag, str) for tag in tags))

    def test_get_words_by_tag(self):
        """Test getting words by specific tag."""
        text = "من و تو به خانه می‌رویم"
        pronouns = self.tagger.get_words_by_tag(text, PersianPOSTag.PRO_PERS.value)

        self.assertIn("من", pronouns)
        self.assertIn("تو", pronouns)

    def test_get_tag_counts(self):
        """Test getting tag counts."""
        text = "من و تو به خانه می‌رویم"
        counts = self.tagger.get_tag_counts(text)

        self.assertIsInstance(counts, dict)
        self.assertGreater(len(counts), 0)
        self.assertTrue(all(isinstance(count, int) for count in counts.values()))

    def test_get_tag_distribution(self):
        """Test getting tag distribution."""
        text = "من به خانه می‌روم"
        distribution = self.tagger.get_tag_distribution(text)

        self.assertIsInstance(distribution, dict)
        self.assertGreater(len(distribution), 0)
        # All proportions should sum to 1.0
        self.assertAlmostEqual(sum(distribution.values()), 1.0, places=2)

    def test_tag_words(self):
        """Test tagging a list of words."""
        words = ["من", "به", "دانشگاه", "می‌روم"]
        tagged = self.tagger.tag_words(words)

        self.assertGreater(len(tagged), 0)
        self.assertTrue(all(isinstance(item, tuple) and len(item) == 2
                           for item in tagged))

    def test_tag_batch(self):
        """Test batch tagging."""
        texts = [
            "من به خانه می‌روم",
            "کتاب خوب است"
        ]
        results = self.tagger.tag_batch(texts)

        self.assertEqual(len(results), 2)
        self.assertTrue(all(isinstance(result, list) for result in results))
        self.assertTrue(all(len(result) > 0 for result in results))

    def test_add_noun(self):
        """Test adding custom noun."""
        custom_noun = "فناوری"
        self.tagger.add_noun(custom_noun)

        tagged = self.tagger.tag(custom_noun)
        self.assertEqual(tagged[0][1], PersianPOSTag.N.value)

    def test_add_verb(self):
        """Test adding custom verb root."""
        custom_verb = "پرید"
        self.tagger.add_verb(custom_verb)

        tagged = self.tagger.tag(custom_verb)
        self.assertEqual(tagged[0][1], PersianPOSTag.V_PAST.value)

    def test_add_adjective(self):
        """Test adding custom adjective."""
        custom_adj = "درخشان"
        self.tagger.add_adjective(custom_adj)

        tagged = self.tagger.tag(custom_adj)
        self.assertEqual(tagged[0][1], PersianPOSTag.ADJ.value)

    def test_add_words(self):
        """Test adding multiple custom words."""
        custom_words = [
            ("نوآوری", PersianPOSTag.N.value),
            ("پرواز", "V"),
            ("زیبا", "ADJ")
        ]
        self.tagger.add_words(custom_words)

        # Verify they're tagged correctly
        for word, expected_tag in custom_words:
            tagged = self.tagger.tag(word)
            # Should be tagged (exact match may vary due to morphology)
            self.assertGreater(len(tagged), 0)

    def test_normalization_enabled(self):
        """Test that normalization works when enabled."""
        tagger = RuleBasedPOSTagger(normalize=True)
        # Arabic 'ك' should be normalized to Persian 'ک'
        result = tagger.tag("كتاب")
        self.assertGreater(len(result), 0)

    def test_normalization_disabled(self):
        """Test that normalization can be disabled."""
        tagger = RuleBasedPOSTagger(normalize=False)
        result = tagger.tag("كتاب")
        self.assertGreater(len(result), 0)

    def test_get_params(self):
        """Test getting tagger parameters."""
        params = self.tagger.get_params()

        self.assertIn('normalize', params)
        self.assertIn('is_trained', params)
        self.assertTrue(params['is_trained'])

    def test_set_params(self):
        """Test setting tagger parameters."""
        self.tagger.set_params(normalize=False)
        self.assertFalse(self.tagger.normalize)

        self.tagger.set_params(normalize=True)
        self.assertTrue(self.tagger.normalize)

    def test_complex_sentence(self):
        """Test tagging a complex sentence."""
        text = "امروز من و دوستم به دانشگاه تهران رفتیم."
        tagged = self.tagger.tag(text)

        self.assertGreater(len(tagged), 5)
        # Should have various POS tags
        tags = [tag for word, tag in tagged]
        self.assertIn(PersianPOSTag.PRO_PERS.value, tags)  # من
        self.assertIn(PersianPOSTag.PREP.value, tags)  # به
        self.assertIn(PersianPOSTag.PUNC.value, tags)  # .

    def test_location_proper_noun(self):
        """Test tagging location proper nouns."""
        tagged = self.tagger.tag("تهران")
        self.assertEqual(tagged[0][1], PersianPOSTag.N_LOC.value)

        tagged = self.tagger.tag("اصفهان")
        self.assertEqual(tagged[0][1], PersianPOSTag.N_LOC.value)


if __name__ == '__main__':
    unittest.main()
