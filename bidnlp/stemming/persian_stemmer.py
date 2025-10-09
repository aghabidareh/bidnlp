"""
Persian Stemmer Implementation

This stemmer removes common Persian suffixes to extract the root/stem of words.
It handles plural forms, verb conjugations, possessive pronouns, and other affixes.
"""

import re


class PersianStemmer:
    """
    A rule-based stemmer for Persian (Farsi) language.

    This stemmer removes suffixes in multiple passes to handle complex word formations.
    """

    def __init__(self):
        # Define suffix patterns in order of removal (longest first)
        # Arabic broken plural patterns (remove before regular plurals)
        # Format: (pattern, replacement)
        self.arabic_broken_plurals = [
            ('یجات', 'ی'),  # سبزیجات -> سبزی
            ('جات', ''),    # میوه‌جات -> میوه
        ]

        # Compound suffixes (combinations that should be removed together)
        # These are checked before individual suffixes
        self.compound_suffixes = [
            'هایمان', 'هایتان', 'هایشان',
            'هایم', 'هایت', 'هایش',
            'انمان', 'انتان', 'انشان',
        ]

        # Plural and noun suffixes
        self.plural_suffixes = [
            'های', 'ها', 'یان', 'ان', 'ات', 'ین', 'ون'
        ]

        # Possessive pronouns
        self.possessive_suffixes = [
            'مان', 'تان', 'شان',
            'ایم', 'اید', 'اند',
            'یم', 'ید', 'ند',
            'ام', 'ات', 'اش',
            'م', 'ت', 'ش'
        ]

        # Verb suffixes (present and past tense)
        # Start with longer, more specific patterns
        self.verb_suffixes = [
            'یدیم', 'یدید', 'یدند', 'ندگان', 'اندگان',
            'یده', 'نده', 'انده',
            'یدم', 'یدی', 'ید',
            'ندم', 'ندی', 'ند',
            'یم', 'ید', 'ند',
            'ده', 'نده',
        ]

        # Personal endings for verbs (to be removed carefully)
        self.personal_endings = ['م', 'ی', 'ند']

        # Comparative and superlative
        self.comparative_suffixes = [
            'ترین', 'تری', 'تر'
        ]

        # Object pronouns
        self.object_pronouns = [
            'مان', 'تان', 'شان'
        ]

        # Adverb and adjective suffixes
        self.adverb_suffixes = [
            'انه', 'وار', 'ناک', 'گانه'
        ]

        # Arabic plural patterns common in Persian
        self.arabic_plurals = [
            'ین', 'ون', 'ات'
        ]

        # Minimum stem length
        self.min_stem_length = 2

    def normalize(self, word):
        """Normalize Persian text"""
        # Remove ZWNJ (zero-width non-joiner) and other invisible characters
        word = word.replace('\u200c', '')  # ZWNJ
        word = word.replace('\u200b', '')  # Zero-width space
        word = word.replace('\u200d', '')  # Zero-width joiner

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
            'ة': 'ه'
        }

        for arabic, persian in replacements.items():
            word = word.replace(arabic, persian)

        return word.strip()

    def remove_suffix(self, word, suffixes):
        """Remove suffix from word if it exists"""
        for suffix in suffixes:
            if word.endswith(suffix) and len(word) - len(suffix) >= self.min_stem_length:
                return word[:-len(suffix)]
        return word

    def remove_broken_plural(self, word, patterns):
        """Remove Arabic broken plural pattern and apply replacement"""
        for pattern, replacement in patterns:
            if word.endswith(pattern):
                stem = word[:-len(pattern)]
                if len(stem + replacement) >= self.min_stem_length:
                    return stem + replacement
        return word

    def stem(self, word):
        """
        Stem a Persian word by removing suffixes.

        Args:
            word (str): The Persian word to stem

        Returns:
            str: The stemmed word
        """
        if not word:
            return word

        # Normalize the word first
        word = self.normalize(word)
        original_word = word

        # Remove suffixes in order (multiple passes for complex words)
        # 1. Remove Arabic broken plurals FIRST (before any other 'ات' removal)
        word = self.remove_broken_plural(word, self.arabic_broken_plurals)
        # Track if broken plural was applied (has special ending that shouldn't be removed)
        broken_plural_applied = word != original_word and (word.endswith('ی'))
        # Track if the word came from جات pattern (like میوهجات → میوه)
        has_jaat_pattern = word != original_word and original_word.endswith('جات') and not word.endswith('ی')

        # 2. Remove compound suffixes (e.g., هایمان, انمان)
        word = self.remove_suffix(word, self.compound_suffixes)

        # 3. Remove possessive pronouns (but not single 'م' which could be verb ending)
        possessive_no_m = [s for s in self.possessive_suffixes if s != 'م']
        word = self.remove_suffix(word, possessive_no_m)

        # 4. Remove plural suffixes
        word = self.remove_suffix(word, self.plural_suffixes)

        # 5. Remove possessive pronouns again (for cases like خانه‌ام → خانه + ام)
        word = self.remove_suffix(word, possessive_no_m)

        # 6. Remove comparative/superlative
        word = self.remove_suffix(word, self.comparative_suffixes)

        # 7. Remove verb suffixes (main patterns)
        word = self.remove_suffix(word, self.verb_suffixes)

        # 8. Remove personal endings (م، ی، ند) carefully
        # Only remove if not from broken plural and word is long enough
        if not broken_plural_applied and len(word) >= 3:
            word = self.remove_suffix(word, self.personal_endings)

        # 9. Remove adverb/adjective suffixes
        word = self.remove_suffix(word, self.adverb_suffixes)

        # 10. Remove Arabic plural patterns
        word = self.remove_suffix(word, self.arabic_plurals)

        # 12. Final cleanup - remove trailing 'ه' in specific patterns
        # Remove 'ه' if:
        # - Word ends with 'ه'
        # - After removal, stem is at least min_stem_length
        # - Original word had a suffix removed (word changed from original)
        # - The 'ه' is followed by a possessive (like خانه‌ام → خانه → خان)
        # - UNLESS it came from a جات pattern which should keep the 'ه'
        # - UNLESS the original ended with 'هها' or 'های' (means 'ه' is part of root)
        keeps_heh = has_jaat_pattern or original_word.endswith('هها') or original_word.endswith('های')

        if word != original_word and word.endswith('ه') and len(word) > 2 and not keeps_heh:
            # Only remove if there was a possessive suffix like ام, ات, اش
            had_possessive = any(original_word.endswith('ه' + s) for s in ['ام', 'ات', 'اش', 'م', 'ت', 'ش'])
            if had_possessive:
                potential_stem = word[:-1]
                if len(potential_stem) >= self.min_stem_length:
                    word = potential_stem

        return word if word else original_word

    def stem_sentence(self, sentence):
        """
        Stem all words in a sentence.

        Args:
            sentence (str): The Persian sentence to stem

        Returns:
            list: List of stemmed words
        """
        words = sentence.split()
        return [self.stem(word) for word in words]
