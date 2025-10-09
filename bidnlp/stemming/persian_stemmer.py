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
        # Note: 'ین' and 'ون' are handled separately in arabic_plurals
        self.plural_suffixes = [
            'های', 'ها', 'یان', 'ان', 'ات'
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
        # Note: For 'تند', we only want to remove 'ند', leaving 'ت'
        self.verb_suffixes = [
            'یدیم', 'یدید', 'یدند', 'ندگان', 'اندگان',
            'ستند', 'ستیم', 'ستید',
            'یده', 'نده', 'انده',
            'یدم', 'یدی', 'ید',
            'ندم', 'ندی',
            'ستم', 'ستی',
            'تیم', 'تید',
            'یم', 'ید',
            'ده', 'نده',
        ]

        # Personal endings for verbs (to be removed carefully)
        # These are applied after verb suffixes
        self.personal_endings = ['م', 'ی']

        # Special pattern: 'تند' -> remove only 'ند', keep 'ت'
        # This is for past tense verbs like رفتند -> رفت, خوردند -> خورد
        self.past_tense_plural = 'ند'

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
        # Note: 'ات' is handled carefully - only removed if it results in valid stem
        self.arabic_plurals = [
            'ین', 'ون'
        ]

        # Special Arabic plurals that need stem adjustment
        # These are applied before regular plural removal
        self.arabic_plural_patterns = [
            ('سلمین', 'سلم'),  # مسلمین -> مسلم, مؤمنین -> not affected
            ('لمون', 'لم'),     # معلمون -> معلم
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

        # 1b. Handle special Arabic plural patterns (e.g., مسلمین -> مسلم)
        # This must be done BEFORE step 4 removes 'ین'
        word_before_arabic = word
        word = self.remove_broken_plural(word, self.arabic_plural_patterns)
        arabic_plural_applied = word != word_before_arabic

        # 2. Remove compound suffixes (e.g., هایمان, انمان)
        word = self.remove_suffix(word, self.compound_suffixes)

        # 3. Remove possessive pronouns (but not single 'م' or 'ند' which could be verb endings)
        # 'ند' should not be removed here as it's part of past tense verb forms (رفتند, خوردند)
        # For 'ت', be more careful - check if removing it might leave a valid verb stem
        possessive_safe = [s for s in self.possessive_suffixes if s not in ['م', 'ند']]
        # Don't include 'ت' for now - handle it specially in step 3b
        possessive_safe = [s for s in possessive_safe if s != 'ت']
        word = self.remove_suffix(word, possessive_safe)

        # 3b. Handle 'ت' possessive carefully
        # Only remove if NOT preceded by common past tense patterns (شت، فت، دت، رد، خت، ست)
        # This preserves verb stems like نوشت، رفت، دید while removing possessive from کتابت
        if word.endswith('ت') and len(word) > 3:
            # Check what's before the 'ت'
            before_t = word[-2]
            # If it's a verb-like pattern, don't remove
            if before_t not in ['ش', 'ف', 'س']:  # Common verb stem endings before 'ت'
                # Try removing 'ت'
                potential = word[:-1]
                if len(potential) >= self.min_stem_length:
                    word = potential

        # 4. Remove plural suffixes
        word_before_plural = word
        word = self.remove_suffix(word, self.plural_suffixes)
        # Track if 'ات' was removed (Arabic plural pattern) - the remaining 'م' should be kept
        at_suffix_removed = word_before_plural.endswith('ات') and word != word_before_plural

        # 5. Remove possessive pronouns again (for cases like خانه‌ام → خانه + ام)
        word = self.remove_suffix(word, possessive_safe)

        # 6. Remove comparative/superlative
        word = self.remove_suffix(word, self.comparative_suffixes)

        # 7. Remove verb suffixes (main patterns)
        word = self.remove_suffix(word, self.verb_suffixes)

        # 7b. Special handling for past tense plural 'ند'
        # Only remove 'ند' if word ends with 'تند', 'دند', leaving the 'ت' or 'د'
        # This handles: رفتند -> رفت, خوردند -> خورد
        if word.endswith(self.past_tense_plural) and len(word) > 3:
            # Check if preceded by ت or د
            before_nd = word[-3]
            if before_nd in ['ت', 'د']:
                word = word[:-2]  # Remove only 'ند', keep the ت or د

        # 8. Remove personal endings (م، ی) carefully
        # Only remove if not from broken plural, not from Arabic plural, not from 'ات' suffix, and word is long enough
        # Don't remove if word ends with 'م' from Arabic plural (e.g., مسلم from مسلمین, کلم from کلمات)
        if not broken_plural_applied and not arabic_plural_applied and not at_suffix_removed and len(word) >= 3:
            word = self.remove_suffix(word, self.personal_endings)

        # 9. Remove adverb/adjective suffixes
        # But skip if word ends with 'خانه' (compound word, we'll handle 'ه' removal later)
        is_khaneh_compound = word.endswith('خانه') and len(word) > 4
        if not is_khaneh_compound:
            word = self.remove_suffix(word, self.adverb_suffixes)

        # 10. Remove Arabic plural patterns
        word = self.remove_suffix(word, self.arabic_plurals)

        # 11. Final cleanup - remove trailing 'ه' in specific patterns
        # Remove 'ه' if:
        # - Word ends with 'ه'
        # - After removal, stem is at least min_stem_length
        # - Original word had a suffix removed (word changed from original)
        # - The 'ه' is followed by a possessive (like خانه‌ام → خانه → خان)
        #   OR if it's part of a compound that had an adverb suffix (like خانواده‌وار)
        #   OR if it's a compound word ending in خانه (like کتابخانه -> کتابخان)
        # - UNLESS it came from a جات pattern which should keep the 'ه'
        # - UNLESS the original ended with 'هها' or 'های' (means 'ه' is part of root)
        keeps_heh = has_jaat_pattern or original_word.endswith('هها') or original_word.endswith('های')

        if word.endswith('ه') and len(word) > 2 and not keeps_heh:
            # Remove if there was a possessive suffix like ام, ات, اش
            # OR if there was an adverb suffix like وار, انه
            # OR if it's a compound ending in خانه
            had_possessive = any(original_word.endswith('ه' + s) for s in ['ام', 'ات', 'اش', 'م', 'ت', 'ش'])
            had_adverb = any(original_word.endswith('ه' + s) for s in ['وار', 'انه'])
            had_simple_suffix = original_word.endswith('انه') or original_word.endswith('وار')
            is_compound_khaneh = word.endswith('خانه') and len(word) > 4

            # Only apply if word changed from original OR it's a خانه compound
            if (word != original_word and (had_possessive or had_adverb or had_simple_suffix)) or is_compound_khaneh:
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
