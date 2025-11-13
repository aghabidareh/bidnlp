"""
Tests for Persian POS tags and resources
"""

import unittest
from bidnlp.pos import PersianPOSTag, PersianPOSResources


class TestPersianPOSTag(unittest.TestCase):
    """Test cases for PersianPOSTag enum."""

    def test_tag_values(self):
        """Test that all tags have correct values."""
        self.assertEqual(PersianPOSTag.N.value, "N")
        self.assertEqual(PersianPOSTag.V.value, "V")
        self.assertEqual(PersianPOSTag.ADJ.value, "ADJ")
        self.assertEqual(PersianPOSTag.ADV.value, "ADV")
        self.assertEqual(PersianPOSTag.PRO.value, "PRO")
        self.assertEqual(PersianPOSTag.PREP.value, "PREP")
        self.assertEqual(PersianPOSTag.CONJ.value, "CONJ")
        self.assertEqual(PersianPOSTag.NUM.value, "NUM")
        self.assertEqual(PersianPOSTag.PUNC.value, "PUNC")

    def test_tag_types(self):
        """Test various tag types."""
        # Noun types
        self.assertEqual(PersianPOSTag.N_PL.value, "N_PL")
        self.assertEqual(PersianPOSTag.N_PERS.value, "N_PERS")
        self.assertEqual(PersianPOSTag.N_LOC.value, "N_LOC")

        # Verb types
        self.assertEqual(PersianPOSTag.V_AUX.value, "V_AUX")
        self.assertEqual(PersianPOSTag.V_PAST.value, "V_PAST")
        self.assertEqual(PersianPOSTag.V_PRES.value, "V_PRES")

        # Pronoun types
        self.assertEqual(PersianPOSTag.PRO_PERS.value, "PRO_PERS")
        self.assertEqual(PersianPOSTag.PRO_DEM.value, "PRO_DEM")


class TestPersianPOSResources(unittest.TestCase):
    """Test cases for PersianPOSResources."""

    def setUp(self):
        """Set up test fixtures."""
        self.resources = PersianPOSResources()

    def test_common_nouns(self):
        """Test common nouns set."""
        self.assertIn('کتاب', self.resources.COMMON_NOUNS)
        self.assertIn('خانه', self.resources.COMMON_NOUNS)
        self.assertIn('دانشگاه', self.resources.COMMON_NOUNS)
        self.assertGreater(len(self.resources.COMMON_NOUNS), 0)

    def test_plural_suffixes(self):
        """Test plural suffixes."""
        self.assertIn('ها', self.resources.PLURAL_SUFFIXES)
        self.assertIn('ان', self.resources.PLURAL_SUFFIXES)
        self.assertIn('گان', self.resources.PLURAL_SUFFIXES)

    def test_personal_pronouns(self):
        """Test personal pronouns."""
        self.assertIn('من', self.resources.PERSONAL_PRONOUNS)
        self.assertIn('تو', self.resources.PERSONAL_PRONOUNS)
        self.assertIn('او', self.resources.PERSONAL_PRONOUNS)
        self.assertIn('ما', self.resources.PERSONAL_PRONOUNS)
        self.assertIn('شما', self.resources.PERSONAL_PRONOUNS)

    def test_demonstrative_pronouns(self):
        """Test demonstrative pronouns."""
        self.assertIn('این', self.resources.DEMONSTRATIVE_PRONOUNS)
        self.assertIn('آن', self.resources.DEMONSTRATIVE_PRONOUNS)

    def test_interrogative_pronouns(self):
        """Test interrogative pronouns."""
        self.assertIn('چه', self.resources.INTERROGATIVE_PRONOUNS)
        self.assertIn('کی', self.resources.INTERROGATIVE_PRONOUNS)
        self.assertIn('کجا', self.resources.INTERROGATIVE_PRONOUNS)

    def test_prepositions(self):
        """Test prepositions."""
        self.assertIn('از', self.resources.PREPOSITIONS)
        self.assertIn('به', self.resources.PREPOSITIONS)
        self.assertIn('با', self.resources.PREPOSITIONS)
        self.assertIn('در', self.resources.PREPOSITIONS)

    def test_conjunctions(self):
        """Test conjunctions."""
        self.assertIn('و', self.resources.CONJUNCTIONS)
        self.assertIn('یا', self.resources.CONJUNCTIONS)
        self.assertIn('اما', self.resources.CONJUNCTIONS)

    def test_auxiliary_verbs(self):
        """Test auxiliary verbs."""
        self.assertIn('است', self.resources.AUXILIARY_VERBS)
        self.assertIn('بود', self.resources.AUXILIARY_VERBS)
        self.assertIn('شد', self.resources.AUXILIARY_VERBS)

    def test_common_adjectives(self):
        """Test common adjectives."""
        self.assertIn('خوب', self.resources.COMMON_ADJECTIVES)
        self.assertIn('بد', self.resources.COMMON_ADJECTIVES)
        self.assertIn('بزرگ', self.resources.COMMON_ADJECTIVES)
        self.assertIn('کوچک', self.resources.COMMON_ADJECTIVES)

    def test_common_adverbs(self):
        """Test common adverbs."""
        self.assertIn('خیلی', self.resources.COMMON_ADVERBS)
        self.assertIn('بسیار', self.resources.COMMON_ADVERBS)
        self.assertIn('همیشه', self.resources.COMMON_ADVERBS)

    def test_determiners(self):
        """Test determiners."""
        self.assertIn('یک', self.resources.DETERMINERS)
        self.assertIn('هر', self.resources.DETERMINERS)
        self.assertIn('همه', self.resources.DETERMINERS)

    def test_is_plural_noun(self):
        """Test plural noun detection."""
        self.assertTrue(self.resources.is_plural_noun('کتابها'))
        self.assertTrue(self.resources.is_plural_noun('دانشجویان'))
        self.assertTrue(self.resources.is_plural_noun('معلمان'))
        self.assertFalse(self.resources.is_plural_noun('کتاب'))

    def test_is_comparative(self):
        """Test comparative adjective detection."""
        self.assertTrue(self.resources.is_comparative('بزرگتر'))
        self.assertTrue(self.resources.is_comparative('کوچکتر'))
        self.assertFalse(self.resources.is_comparative('بزرگ'))
        self.assertFalse(self.resources.is_comparative('تر'))  # Too short

    def test_is_superlative(self):
        """Test superlative adjective detection."""
        self.assertTrue(self.resources.is_superlative('بزرگترین'))
        self.assertTrue(self.resources.is_superlative('کوچکترین'))
        self.assertFalse(self.resources.is_superlative('بزرگ'))
        self.assertFalse(self.resources.is_superlative('ترین'))  # Too short

    def test_is_infinitive(self):
        """Test infinitive verb detection."""
        self.assertTrue(self.resources.is_infinitive('رفتن'))
        self.assertTrue(self.resources.is_infinitive('خوردن'))
        self.assertTrue(self.resources.is_infinitive('نوشتن'))
        self.assertFalse(self.resources.is_infinitive('رفت'))

    def test_is_punctuation(self):
        """Test punctuation detection."""
        self.assertTrue(self.resources.is_punctuation('.'))
        self.assertTrue(self.resources.is_punctuation('،'))
        self.assertTrue(self.resources.is_punctuation('؟'))
        self.assertTrue(self.resources.is_punctuation('!'))
        self.assertFalse(self.resources.is_punctuation('کتاب'))

    def test_get_tag_description(self):
        """Test tag description retrieval."""
        self.assertEqual(self.resources.get_tag_description('N'), 'Common noun')
        self.assertEqual(self.resources.get_tag_description('V'), 'Verb')
        self.assertEqual(self.resources.get_tag_description('ADJ'), 'Adjective')
        self.assertEqual(self.resources.get_tag_description('PREP'), 'Preposition')
        self.assertIn('Unknown', self.resources.get_tag_description('INVALID'))


if __name__ == '__main__':
    unittest.main()
