"""
Persian POS Tag Definitions

Defines the tag set and linguistic resources for Persian POS tagging.
"""

from typing import Set, Dict, List
from enum import Enum


class PersianPOSTag(str, Enum):
    """Persian POS tag enumeration."""

    # Nouns
    N = "N"                    # Common noun
    N_PL = "N_PL"             # Plural noun
    N_PERS = "N_PERS"         # Proper noun (person)
    N_LOC = "N_LOC"           # Proper noun (location)
    N_ORG = "N_ORG"           # Proper noun (organization)

    # Verbs
    V = "V"                    # Verb (general)
    V_AUX = "V_AUX"           # Auxiliary verb
    V_PAST = "V_PAST"         # Past tense verb
    V_PRES = "V_PRES"         # Present tense verb
    V_IMP = "V_IMP"           # Imperative verb
    V_SUB = "V_SUB"           # Subjunctive verb
    V_INF = "V_INF"           # Infinitive verb

    # Adjectives
    ADJ = "ADJ"               # Adjective
    ADJ_CMPR = "ADJ_CMPR"     # Comparative adjective
    ADJ_SUP = "ADJ_SUP"       # Superlative adjective

    # Adverbs
    ADV = "ADV"               # Adverb
    ADV_TIME = "ADV_TIME"     # Time adverb
    ADV_LOC = "ADV_LOC"       # Location adverb
    ADV_NEG = "ADV_NEG"       # Negative adverb

    # Pronouns
    PRO = "PRO"               # Pronoun (general)
    PRO_DEM = "PRO_DEM"       # Demonstrative pronoun
    PRO_PERS = "PRO_PERS"     # Personal pronoun
    PRO_INT = "PRO_INT"       # Interrogative pronoun
    PRO_REF = "PRO_REF"       # Reflexive pronoun

    # Prepositions
    PREP = "PREP"             # Preposition

    # Conjunctions
    CONJ = "CONJ"             # Conjunction
    CONJ_SUBR = "CONJ_SUBR"   # Subordinating conjunction

    # Determiners
    DET = "DET"               # Determiner

    # Numerals
    NUM = "NUM"               # Numeral

    # Particles
    PART = "PART"             # Particle
    PART_NEG = "PART_NEG"     # Negative particle

    # Punctuation
    PUNC = "PUNC"             # Punctuation

    # Special
    UNKNOWN = "UNKNOWN"       # Unknown


class PersianPOSResources:
    """Linguistic resources for Persian POS tagging."""

    # Common Persian nouns
    COMMON_NOUNS: Set[str] = {
        'کتاب', 'خانه', 'مدرسه', 'دانشگاه', 'شهر', 'روز', 'شب',
        'صبح', 'عصر', 'کار', 'درس', 'آب', 'غذا', 'نان', 'میز',
        'صندلی', 'اتاق', 'آشپزخانه', 'حمام', 'باغ', 'پارک', 'خیابان',
        'ماشین', 'اتوبوس', 'قطار', 'هواپیما', 'دفتر', 'کلاس', 'کامپیوتر',
        'تلفن', 'موبایل', 'تلویزیون', 'رادیو', 'کتابخانه', 'فروشگاه',
        'بیمارستان', 'داروخانه', 'رستوران', 'کافه', 'هتل', 'فرودگاه',
    }

    # Plural markers
    PLURAL_SUFFIXES: Set[str] = {
        'ها', 'ان', 'ین', 'ات', 'گان'
    }

    # Personal pronouns
    PERSONAL_PRONOUNS: Set[str] = {
        'من', 'تو', 'او', 'ما', 'شما', 'آنها', 'ایشان', 'وی', 'ایشون'
    }

    # Demonstrative pronouns
    DEMONSTRATIVE_PRONOUNS: Set[str] = {
        'این', 'آن', 'اینها', 'آنها', 'همین', 'همان'
    }

    # Interrogative pronouns
    INTERROGATIVE_PRONOUNS: Set[str] = {
        'چه', 'چی', 'کی', 'کجا', 'کدام', 'چرا', 'چگونه', 'چطور'
    }

    # Reflexive pronouns
    REFLEXIVE_PRONOUNS: Set[str] = {
        'خود', 'خودم', 'خودت', 'خودش', 'خودمان', 'خودتان', 'خودشان'
    }

    # Prepositions
    PREPOSITIONS: Set[str] = {
        'از', 'به', 'با', 'در', 'برای', 'تا', 'بر', 'بی', 'بدون',
        'مانند', 'همچون', 'نزد', 'پیش', 'جز', 'غیر', 'علاوه', 'طبق',
        'توسط', 'بعد', 'قبل', 'پس', 'روی', 'زیر', 'کنار', 'میان'
    }

    # Conjunctions
    CONJUNCTIONS: Set[str] = {
        'و', 'یا', 'اما', 'ولی', 'که', 'تا', 'چون', 'زیرا', 'پس',
        'اگر', 'چنانچه', 'هرچند', 'اگرچه', 'بنابراین', 'همچنین', 'نیز'
    }

    # Subordinating conjunctions
    SUBORDINATING_CONJUNCTIONS: Set[str] = {
        'که', 'تا', 'چون', 'زیرا', 'اگر', 'چنانچه', 'هرچند', 'اگرچه'
    }

    # Auxiliary verbs
    AUXILIARY_VERBS: Set[str] = {
        'است', 'بود', 'شد', 'می‌شود', 'شده', 'خواهد', 'باید', 'می‌تواند',
        'هست', 'نیست', 'بوده', 'شده', 'گردید', 'می‌گردد'
    }

    # Present tense prefixes
    PRESENT_PREFIXES: Set[str] = {
        'می', 'نمی', 'بر', 'در', 'فرا', 'وا'
    }

    # Past tense suffixes
    PAST_SUFFIXES: Set[str] = {
        'م', 'ی', 'یم', 'ید', 'ند', 'ام', 'ای', 'ه', 'یم', 'اند'
    }

    # Infinitive suffixes
    INFINITIVE_SUFFIXES: Set[str] = {
        'تن', 'دن', 'ستن', 'فتن'
    }

    # Common verbs (roots)
    COMMON_VERB_ROOTS: Set[str] = {
        'رفت', 'آمد', 'خورد', 'خواب', 'نشست', 'ایستاد', 'دوید', 'خواند',
        'نوشت', 'گفت', 'دید', 'شنید', 'کرد', 'داد', 'گرفت', 'آورد',
        'برد', 'خرید', 'فروخت', 'ساخت', 'شکست', 'باخت', 'برد', 'شد'
    }

    # Adjectives
    COMMON_ADJECTIVES: Set[str] = {
        'خوب', 'بد', 'بزرگ', 'کوچک', 'قشنگ', 'زیبا', 'زشت', 'سرد', 'گرم',
        'سریع', 'کند', 'بلند', 'کوتاه', 'سنگین', 'سبک', 'تازه', 'کهنه',
        'جدید', 'قدیمی', 'مدرن', 'سنتی', 'آسان', 'سخت', 'راحت', 'مشکل',
        'شاد', 'غمگین', 'خوشحال', 'ناراحت', 'عصبانی', 'آرام', 'پرانرژی'
    }

    # Comparative adjective suffix
    COMPARATIVE_SUFFIX: str = 'تر'
    SUPERLATIVE_SUFFIX: str = 'ترین'

    # Adverbs
    COMMON_ADVERBS: Set[str] = {
        'خیلی', 'بسیار', 'کمی', 'اندکی', 'همیشه', 'هرگز', 'اکنون', 'حالا',
        'الان', 'دیروز', 'امروز', 'فردا', 'دیشب', 'امشب', 'فردا', 'پریروز',
        'پس‌فردا', 'بعد', 'قبل', 'زود', 'دیر', 'سریع', 'آهسته', 'باز', 'دوباره'
    }

    # Time adverbs
    TIME_ADVERBS: Set[str] = {
        'همیشه', 'هرگز', 'اکنون', 'حالا', 'الان', 'دیروز', 'امروز', 'فردا',
        'دیشب', 'امشب', 'پریروز', 'پس‌فردا', 'صبح', 'ظهر', 'عصر', 'شب'
    }

    # Location adverbs
    LOCATION_ADVERBS: Set[str] = {
        'اینجا', 'آنجا', 'بالا', 'پایین', 'جلو', 'عقب', 'داخل', 'بیرون',
        'نزدیک', 'دور', 'کنار', 'وسط', 'اطراف'
    }

    # Negative adverbs
    NEGATIVE_ADVERBS: Set[str] = {
        'نه', 'نمی', 'نخیر', 'هرگز', 'هیچ'
    }

    # Negative particles
    NEGATIVE_PARTICLES: Set[str] = {
        'ن', 'نه', 'نی', 'نمی'
    }

    # Determiners
    DETERMINERS: Set[str] = {
        'یک', 'هر', 'همه', 'تمام', 'بعضی', 'برخی', 'چند', 'اکثر', 'کل'
    }

    # Common proper nouns (cities)
    PERSIAN_CITIES: Set[str] = {
        'تهران', 'اصفهان', 'شیراز', 'مشهد', 'تبریز', 'کرج', 'قم', 'اهواز',
        'کرمان', 'رشت', 'یزد', 'همدان', 'اراک', 'زاهدان', 'کرمانشاه'
    }

    # Punctuation marks
    PUNCTUATION_MARKS: Set[str] = {
        '.', '،', '؛', ':', '!', '؟', '«', '»', '(', ')', '[', ']',
        '{', '}', '-', '–', '—', '/', '\\', '"', "'", '…'
    }

    @classmethod
    def is_plural_noun(cls, word: str) -> bool:
        """Check if word is a plural noun."""
        return any(word.endswith(suffix) for suffix in cls.PLURAL_SUFFIXES)

    @classmethod
    def is_comparative(cls, word: str) -> bool:
        """Check if word is a comparative adjective."""
        return word.endswith(cls.COMPARATIVE_SUFFIX) and len(word) > len(cls.COMPARATIVE_SUFFIX)

    @classmethod
    def is_superlative(cls, word: str) -> bool:
        """Check if word is a superlative adjective."""
        return word.endswith(cls.SUPERLATIVE_SUFFIX) and len(word) > len(cls.SUPERLATIVE_SUFFIX)

    @classmethod
    def is_infinitive(cls, word: str) -> bool:
        """Check if word is an infinitive verb."""
        return any(word.endswith(suffix) for suffix in cls.INFINITIVE_SUFFIXES)

    @classmethod
    def is_punctuation(cls, word: str) -> bool:
        """Check if word is punctuation."""
        return word in cls.PUNCTUATION_MARKS or all(c in cls.PUNCTUATION_MARKS for c in word)

    @classmethod
    def get_tag_description(cls, tag: str) -> str:
        """Get human-readable description of a POS tag."""
        descriptions = {
            'N': 'Common noun',
            'N_PL': 'Plural noun',
            'N_PERS': 'Proper noun (person)',
            'N_LOC': 'Proper noun (location)',
            'N_ORG': 'Proper noun (organization)',
            'V': 'Verb',
            'V_AUX': 'Auxiliary verb',
            'V_PAST': 'Past tense verb',
            'V_PRES': 'Present tense verb',
            'V_IMP': 'Imperative verb',
            'V_SUB': 'Subjunctive verb',
            'V_INF': 'Infinitive verb',
            'ADJ': 'Adjective',
            'ADJ_CMPR': 'Comparative adjective',
            'ADJ_SUP': 'Superlative adjective',
            'ADV': 'Adverb',
            'ADV_TIME': 'Time adverb',
            'ADV_LOC': 'Location adverb',
            'ADV_NEG': 'Negative adverb',
            'PRO': 'Pronoun',
            'PRO_DEM': 'Demonstrative pronoun',
            'PRO_PERS': 'Personal pronoun',
            'PRO_INT': 'Interrogative pronoun',
            'PRO_REF': 'Reflexive pronoun',
            'PREP': 'Preposition',
            'CONJ': 'Conjunction',
            'CONJ_SUBR': 'Subordinating conjunction',
            'DET': 'Determiner',
            'NUM': 'Numeral',
            'PART': 'Particle',
            'PART_NEG': 'Negative particle',
            'PUNC': 'Punctuation',
            'UNKNOWN': 'Unknown'
        }
        return descriptions.get(tag, 'Unknown tag')
