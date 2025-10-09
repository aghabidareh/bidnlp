"""
Persian Lemmatizer Implementation

This lemmatizer converts Persian words to their dictionary form (lemma).
It uses a combination of rule-based approaches and a dictionary of common lemmas.
"""

import re
from typing import Dict, Set, Optional


class PersianLemmatizer:
    """
    A lemmatizer for Persian (Farsi) language.

    This lemmatizer attempts to convert words to their dictionary form,
    handling verb conjugations, plural nouns, and various affixes.
    """

    def __init__(self, custom_dictionary: Optional[Dict[str, str]] = None):
        """
        Initialize the lemmatizer.

        Args:
            custom_dictionary: Optional dictionary mapping words to their lemmas
        """
        # Dictionary for irregular forms and common words
        self.lemma_dict = self._build_default_dictionary()

        if custom_dictionary:
            self.lemma_dict.update(custom_dictionary)

        # Verb prefixes
        self.verb_prefixes = ['می', 'نمی', 'بی', 'ن', 'ب']

        # Common verb stems and their lemmas (infinitive forms)
        self.verb_stems = {
            'رفت': 'رفتن',
            'رو': 'رفتن',
            'آ': 'آمدن',
            'آی': 'آمدن',
            'آمد': 'آمدن',
            'کرد': 'کردن',
            'کن': 'کردن',
            'گفت': 'گفتن',
            'گو': 'گفتن',
            'خورد': 'خوردن',
            'خور': 'خوردن',
            'دید': 'دیدن',
            'بین': 'دیدن',
            'نوشت': 'نوشتن',
            'نویس': 'نوشتن',
            'خواند': 'خواندن',
            'خوان': 'خواندن',
            'داد': 'دادن',
            'ده': 'دادن',
            'شد': 'شدن',
            'شو': 'شدن',
            'داشت': 'داشتن',
            'دار': 'داشتن',
            'ماند': 'ماندن',
            'مان': 'ماندن',
            'آورد': 'آوردن',
            'آور': 'آوردن',
            'توانست': 'توانستن',
            'توان': 'توانستن',
            'خواست': 'خواستن',
            'خواه': 'خواستن',
        }

        # Arabic broken plural patterns (handle before regular patterns)
        self.arabic_broken_plurals = [
            ('یجات', 'ی'),  # سبزیجات -> سبزی
            ('جات', ''),    # میوه‌جات -> میوه
        ]

        # Compound suffixes (remove as a unit)
        self.compound_suffixes = [
            'هایمان', 'هایتان', 'هایشان',
            'هایم', 'هایت', 'هایش',
            'انمان', 'انتان', 'انشان',
        ]

        # Plural to singular patterns
        self.plural_patterns = [
            ('های', ''),
            ('ها', ''),
            ('یان', ''),
            ('ان', ''),
            ('ات', ''),
            ('ین', 'ی'),
            ('گان', ''),
        ]

        # Possessive and attached pronouns (excluding 'م', 'ت', 'ند' which may be verb endings)
        self.attached_pronouns = [
            'مان', 'تان', 'شان',
            'ایم', 'اید', 'اند',
            'یم', 'ید',
            'ام', 'ات', 'اش',
            'ش'
        ]

        # Verb conjugation endings
        self.verb_endings = [
            'یدیم', 'یدید', 'یدند', 'ندگان',
            'یده', 'نده',
            'یدم', 'یدی', 'ید',
            'ندم', 'ندی', 'ند',
            'ستم', 'ستی', 'ست',
            'یم', 'ید', 'ند',
            'ده', 'ته',
        ]

        # Personal verb endings (remove carefully)
        self.personal_endings = ['م', 'ی', 'ند', 'د']

        # Comparative/superlative
        self.comparison_suffixes = ['ترین', 'تری', 'تر']

        # Adjectival suffixes
        # Note: 'ی' removed as it's too aggressive and removes valid word endings
        self.adjectival_suffixes = ['انه', 'وار', 'ناک']

        self.min_length = 2

    def _build_default_dictionary(self) -> Dict[str, str]:
        """Build a dictionary of common irregular forms"""
        return {
            # Common irregular plurals
            'مردم': 'مرد',
            'زنان': 'زن',
            'کودکان': 'کودک',
            'بچه‌ها': 'بچه',
            'افراد': 'فرد',
            'اشخاص': 'شخص',
            'اشیا': 'شیء',
            'اشیاء': 'شیء',

            # Common irregular verbs
            'بود': 'بودن',
            'باش': 'بودن',
            'هست': 'بودن',
            'است': 'بودن',
            'هستم': 'بودن',
            'هستی': 'بودن',
            'هستند': 'بودن',
            'بودم': 'بودن',
            'بودی': 'بودن',
            'بودند': 'بودن',

            # Other common words
            'بهتر': 'خوب',
            'بهترین': 'خوب',
            'بدتر': 'بد',
            'بدترین': 'بد',
            'بیشتر': 'زیاد',
            'بیشترین': 'زیاد',
            'کمتر': 'کم',
            'کمترین': 'کم',
        }

    def normalize(self, word: str) -> str:
        """Normalize Persian text"""
        # Remove ZWNJ (zero-width non-joiner)
        word = word.replace('\u200c', '')

        # Remove Arabic diacritics
        word = re.sub(r'[\u064B-\u065F\u0670]', '', word)

        # Normalize Arabic characters to Persian
        replacements = {
            'ي': 'ی',
            'ك': 'ک',
            'ؤ': 'و',
            'إ': 'ا',
            'أ': 'ا',
            'ٱ': 'ا',
            'ة': 'ه',
            'ۀ': 'ه'
        }

        for arabic, persian in replacements.items():
            word = word.replace(arabic, persian)

        return word.strip()

    def _remove_prefix(self, word: str) -> tuple[str, str]:
        """Remove verb prefix and return (prefix, word)"""
        for prefix in sorted(self.verb_prefixes, key=len, reverse=True):
            if word.startswith(prefix):
                return prefix, word[len(prefix):]
        return '', word

    def _remove_suffix(self, word: str, suffixes: list) -> str:
        """Remove suffix if present and word remains valid"""
        for suffix in sorted(suffixes, key=len, reverse=True):
            if word.endswith(suffix):
                stem = word[:-len(suffix)]
                if len(stem) >= self.min_length:
                    return stem
        return word

    def _handle_verb(self, word: str) -> str:
        """Try to convert verb to infinitive form"""
        # Remove prefix
        prefix, word_no_prefix = self._remove_prefix(word)

        # Remove verb endings
        stem = self._remove_suffix(word_no_prefix, self.verb_endings)

        # Check if stem is in known verb stems
        if stem in self.verb_stems:
            return self.verb_stems[stem]

        # Try to form infinitive by adding 'تن' or 'دن'
        # This is a heuristic and may not always be correct
        if stem:
            # If stem ends with a consonant, likely needs 'تن' or 'دن'
            if not stem[-1] in 'اوی':
                # Try common patterns
                for ending in ['تن', 'دن', 'ستن', 'یدن']:
                    potential_infinitive = stem + ending
                    # In a real implementation, you'd check against a dictionary
                    # For now, we'll use 'تن' as default for unknown verbs
                    pass
                return stem + 'تن'
            else:
                return stem + 'دن'

        return word

    def lemmatize(self, word: str, pos: Optional[str] = None) -> str:
        """
        Lemmatize a Persian word.

        Args:
            word: The word to lemmatize
            pos: Optional part-of-speech tag ('verb', 'noun', 'adj')

        Returns:
            The lemmatized form of the word
        """
        if not word:
            return word

        # Normalize
        word = self.normalize(word)
        original = word

        # Check dictionary first
        if word in self.lemma_dict:
            return self.lemma_dict[word]

        # Remove Arabic broken plurals FIRST (before 'ات' in attached pronouns)
        broken_plural_applied = False
        has_jaat_pattern = False
        for plural, singular in self.arabic_broken_plurals:
            if word.endswith(plural):
                potential = word[:-len(plural)] + singular
                if len(potential) >= self.min_length:
                    word = potential
                    broken_plural_applied = word.endswith('ی')
                    has_jaat_pattern = original.endswith('جات') and not word.endswith('ی')
                    break

        # Remove compound suffixes first
        word = self._remove_suffix(word, self.compound_suffixes)

        # Remove attached pronouns
        word = self._remove_suffix(word, self.attached_pronouns)

        # Handle based on POS if provided
        if pos == 'verb':
            return self._handle_verb(word)

        # Try to handle as verb if it has verb prefix
        # Only if the remaining part after prefix is long enough to be a verb stem
        for prefix in self.verb_prefixes:
            if word.startswith(prefix):
                stem = word[len(prefix):]
                # Only treat as verb if stem is substantial (> 2 chars)
                if len(stem) > 2:
                    verb_lemma = self._handle_verb(word)
                    if verb_lemma != word:
                        return verb_lemma
                break

        # Remove comparison suffixes
        word = self._remove_suffix(word, self.comparison_suffixes)

        # Remove plural markers
        for plural, singular in self.plural_patterns:
            if word.endswith(plural):
                potential = word[:-len(plural)] + singular
                if len(potential) >= self.min_length:
                    word = potential
                    break

        # Remove attached pronouns again (for cases like خانه‌ام)
        word = self._remove_suffix(word, self.attached_pronouns)

        # Remove adjectival suffixes
        word = self._remove_suffix(word, self.adjectival_suffixes)

        # Remove verb endings (in case it's a participle)
        word = self._remove_suffix(word, self.verb_endings)

        # Remove personal endings carefully (not if from broken plural)
        if not broken_plural_applied and len(word) >= 3:
            word = self._remove_suffix(word, self.personal_endings)

        # Final cleanup - be conservative with 'ه' removal
        # Only remove if: ends with 'ه', had possessive, not from جات pattern
        keeps_heh = has_jaat_pattern or original.endswith('هها') or original.endswith('های')
        if word != original and word.endswith('ه') and len(word) > 2 and not keeps_heh:
            # Only remove if there was a possessive suffix
            had_possessive = any(original.endswith('ه' + s) for s in ['ام', 'ات', 'اش', 'م', 'ت', 'ش'])
            if had_possessive:
                stem = word[:-1]
                if len(stem) >= self.min_length:
                    word = stem

        return word if word and len(word) >= self.min_length else original

    def lemmatize_sentence(self, sentence: str) -> list:
        """
        Lemmatize all words in a sentence.

        Args:
            sentence: The sentence to lemmatize

        Returns:
            List of lemmatized words
        """
        words = sentence.split()
        return [self.lemmatize(word) for word in words]

    def add_lemma(self, word: str, lemma: str):
        """Add a custom word-lemma mapping"""
        self.lemma_dict[word] = lemma

    def add_lemmas(self, lemmas: Dict[str, str]):
        """Add multiple custom word-lemma mappings"""
        self.lemma_dict.update(lemmas)
