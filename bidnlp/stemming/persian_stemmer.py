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

        # Plural and noun suffixes
        self.plural_suffixes = [
            'ها', 'ان', 'ات', 'ین'
        ]

        # Possessive pronouns
        self.possessive_suffixes = [
            'هایم', 'هایت', 'هایش', 'هایمان', 'هایتان', 'هایشان',
            'ام', 'ات', 'اش', 'مان', 'تان', 'شان',
            'ایم', 'اید', 'اند',
            'یم', 'ید', 'ند',
            'م', 'ت', 'ش'
        ]

        # Verb suffixes (present and past tense)
        # Note: Single letter suffixes like 'ی', 'د', 'م' are very aggressive
        # and should be used carefully
        self.verb_suffixes = [
            'یدیم', 'یدید', 'یدند', 'ندگان', 'اندگان',
            'یده', 'نده', 'انده',
            'یدم', 'یدی', 'ید',
            'ندم', 'ندی', 'ند',
            'یم', 'ید', 'ند',
            'ده', 'نده',
            'د', 'م'
        ]

        # Very short verb suffixes (only remove in specific contexts)
        self.short_verb_suffixes = ['ی']

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

        # Remove suffixes in order
        # 1. Remove Arabic broken plurals FIRST (before any other 'ات' removal)
        word = self.remove_broken_plural(word, self.arabic_broken_plurals)

        # 2. Remove possessive pronouns
        word = self.remove_suffix(word, self.possessive_suffixes)

        # 3. Remove plural suffixes
        word = self.remove_suffix(word, self.plural_suffixes)

        # 4. Remove comparative/superlative
        word = self.remove_suffix(word, self.comparative_suffixes)

        # 5. Remove verb suffixes
        word = self.remove_suffix(word, self.verb_suffixes)

        # 6. Remove adverb/adjective suffixes
        word = self.remove_suffix(word, self.adverb_suffixes)

        # 7. Remove Arabic plural patterns
        word = self.remove_suffix(word, self.arabic_plurals)

        # 8. Final cleanup - remove trailing 'ه' in specific patterns
        # Only remove if word is long enough and 'ه' looks like a suffix
        # Be conservative - only remove for words > 4 chars
        if len(word) > 4 and word.endswith('ه'):
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
