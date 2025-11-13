"""
Rule-Based Persian POS Tagger

Implements a rule-based POS tagger using morphological patterns and dictionaries.
"""

from typing import List, Tuple, Set, Optional
from .base_tagger import BasePOSTagger
from .pos_tags import PersianPOSTag, PersianPOSResources


class RuleBasedPOSTagger(BasePOSTagger):
    """Rule-based POS tagger for Persian using morphological rules."""

    def __init__(self, normalize: bool = True):
        """
        Initialize the rule-based POS tagger.

        Args:
            normalize: Whether to normalize text before tagging
        """
        super().__init__(normalize=normalize)
        self.resources = PersianPOSResources()
        self._is_trained = True  # Rule-based doesn't need training

    def tag(self, text: str) -> List[Tuple[str, str]]:
        """
        Tag a text with POS tags using rules.

        Args:
            text: Input text

        Returns:
            List of (word, tag) tuples
        """
        if not text:
            return []

        # Preprocess
        processed_text = self.preprocess(text)

        # Tokenize
        words = self.tokenize(processed_text)

        # Tag each word
        tagged = []
        for i, word in enumerate(words):
            tag = self._tag_word(word, i, words)
            tagged.append((word, tag))

        return tagged

    def _tag_word(self, word: str, position: int, words: List[str]) -> str:
        """
        Tag a single word using rules.

        Args:
            word: The word to tag
            position: Position of word in sentence
            words: All words in sentence (for context)

        Returns:
            POS tag
        """
        if not word:
            return PersianPOSTag.UNKNOWN.value

        # Check punctuation first
        if self.resources.is_punctuation(word):
            return PersianPOSTag.PUNC.value

        # Check for numbers
        if self._is_number(word):
            return PersianPOSTag.NUM.value

        # Check adverbs (before pronouns to catch location adverbs like اینجا)
        if word in self.resources.NEGATIVE_ADVERBS:
            return PersianPOSTag.ADV_NEG.value
        if word in self.resources.TIME_ADVERBS:
            return PersianPOSTag.ADV_TIME.value
        if word in self.resources.LOCATION_ADVERBS:
            return PersianPOSTag.ADV_LOC.value
        if word in self.resources.COMMON_ADVERBS:
            return PersianPOSTag.ADV.value

        # Check pronouns (high priority)
        if word in self.resources.PERSONAL_PRONOUNS:
            return PersianPOSTag.PRO_PERS.value
        if word in self.resources.DEMONSTRATIVE_PRONOUNS:
            return PersianPOSTag.PRO_DEM.value
        if word in self.resources.INTERROGATIVE_PRONOUNS:
            return PersianPOSTag.PRO_INT.value
        if word in self.resources.REFLEXIVE_PRONOUNS:
            return PersianPOSTag.PRO_REF.value

        # Check prepositions
        if word in self.resources.PREPOSITIONS:
            return PersianPOSTag.PREP.value

        # Check conjunctions
        if word in self.resources.SUBORDINATING_CONJUNCTIONS:
            return PersianPOSTag.CONJ_SUBR.value
        if word in self.resources.CONJUNCTIONS:
            return PersianPOSTag.CONJ.value

        # Check determiners
        if word in self.resources.DETERMINERS:
            return PersianPOSTag.DET.value

        # Check negative particles
        if word in self.resources.NEGATIVE_PARTICLES:
            return PersianPOSTag.PART_NEG.value

        # Check auxiliary verbs
        if word in self.resources.AUXILIARY_VERBS:
            return PersianPOSTag.V_AUX.value

        # Check adjectives
        if self.resources.is_superlative(word):
            return PersianPOSTag.ADJ_SUP.value
        if self.resources.is_comparative(word):
            return PersianPOSTag.ADJ_CMPR.value
        if word in self.resources.COMMON_ADJECTIVES:
            return PersianPOSTag.ADJ.value

        # Check verbs
        if self.resources.is_infinitive(word):
            return PersianPOSTag.V_INF.value

        # Check for present tense (می + verb)
        if self._is_present_tense(word, position, words):
            return PersianPOSTag.V_PRES.value

        # Check for verb roots
        if word in self.resources.COMMON_VERB_ROOTS:
            return PersianPOSTag.V_PAST.value

        # Check if it's a verb by suffix patterns
        if self._has_verb_suffix(word):
            return PersianPOSTag.V.value

        # Check proper nouns
        if word in self.resources.PERSIAN_CITIES:
            return PersianPOSTag.N_LOC.value

        # Check if word starts with capital (might be proper noun)
        if self._is_capitalized(word):
            return PersianPOSTag.N_PERS.value

        # Check plural nouns
        if self.resources.is_plural_noun(word):
            return PersianPOSTag.N_PL.value

        # Check common nouns
        if word in self.resources.COMMON_NOUNS:
            return PersianPOSTag.N.value

        # Default: check morphological patterns
        # If it has typical noun patterns, tag as noun
        if self._looks_like_noun(word):
            return PersianPOSTag.N.value

        # If it has typical adjective patterns
        if self._looks_like_adjective(word):
            return PersianPOSTag.ADJ.value

        # Default to noun (most common in Persian)
        return PersianPOSTag.N.value

    def _is_number(self, word: str) -> bool:
        """Check if word is a number."""
        # Check if all digits
        if word.isdigit():
            return True

        # Check Persian digits
        persian_digits = set('۰۱۲۳۴۵۶۷۸۹')
        if all(c in persian_digits for c in word):
            return True

        # Check Arabic-Indic digits
        arabic_digits = set('٠١٢٣٤٥٦٧٨٩')
        if all(c in arabic_digits for c in word):
            return True

        return False

    def _is_present_tense(self, word: str, position: int, words: List[str]) -> bool:
        """Check if word is present tense verb."""
        # Check if word starts with می or نمی
        for prefix in self.resources.PRESENT_PREFIXES:
            if word.startswith(prefix):
                return True

        # Check if previous word is می or نمی
        if position > 0:
            prev_word = words[position - 1]
            if prev_word in self.resources.PRESENT_PREFIXES:
                return True

        return False

    def _has_verb_suffix(self, word: str) -> bool:
        """Check if word has typical verb suffixes."""
        for suffix in self.resources.PAST_SUFFIXES:
            if word.endswith(suffix) and len(word) > len(suffix) + 2:
                return True
        return False

    def _is_capitalized(self, word: str) -> bool:
        """Check if word starts with capital letter (for non-Persian text)."""
        if not word:
            return False
        return word[0].isupper()

    def _looks_like_noun(self, word: str) -> bool:
        """Check if word has typical noun morphology."""
        # Persian nouns often end with specific patterns
        noun_endings = ['ه', 'ی', 'ش', 'ت', 'ن', 'ک', 'گ']
        if len(word) > 2 and word[-1] in noun_endings:
            return True
        return False

    def _looks_like_adjective(self, word: str) -> bool:
        """Check if word has typical adjective morphology."""
        # Check for comparative/superlative
        if self.resources.is_comparative(word) or self.resources.is_superlative(word):
            return True

        # Some adjective patterns
        adj_patterns = ['ناک', 'وار', 'گونه', 'مند', 'آور']
        for pattern in adj_patterns:
            if word.endswith(pattern):
                return True

        return False

    def add_noun(self, noun: str, is_proper: bool = False,
                 location: bool = False, organization: bool = False) -> None:
        """
        Add a custom noun to the dictionary.

        Args:
            noun: The noun to add
            is_proper: Whether it's a proper noun
            location: Whether it's a location name
            organization: Whether it's an organization name
        """
        if location:
            self.resources.PERSIAN_CITIES.add(noun)
        elif not is_proper:
            self.resources.COMMON_NOUNS.add(noun)

    def add_verb(self, verb: str) -> None:
        """
        Add a custom verb root to the dictionary.

        Args:
            verb: The verb root to add
        """
        self.resources.COMMON_VERB_ROOTS.add(verb)

    def add_adjective(self, adjective: str) -> None:
        """
        Add a custom adjective to the dictionary.

        Args:
            adjective: The adjective to add
        """
        self.resources.COMMON_ADJECTIVES.add(adjective)

    def add_words(self, words: List[Tuple[str, str]]) -> None:
        """
        Add multiple custom words with their tags.

        Args:
            words: List of (word, tag) tuples
        """
        for word, tag in words:
            if tag == PersianPOSTag.N.value:
                self.add_noun(word)
            elif tag.startswith('V'):
                self.add_verb(word)
            elif tag.startswith('ADJ'):
                self.add_adjective(word)
