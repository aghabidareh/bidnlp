"""
Persian Stop Words

Provides Persian stop words list and utilities.
"""

from typing import Set, List, Optional


class PersianStopWords:
    """Persian stop words management."""

    # Common Persian stop words
    DEFAULT_STOPWORDS = {
        # Pronouns
        'من', 'تو', 'او', 'ما', 'شما', 'آنها', 'این', 'آن', 'آنان',
        'خود', 'خویش', 'خویشتن',

        # Verbs (to be)
        'است', 'هست', 'بود', 'بودن', 'بودند', 'بودم', 'بودی', 'بوده',
        'باشد', 'باشم', 'باشی', 'باشیم', 'باشید', 'باشند',
        'نیست', 'نبود', 'نباشد',

        # Prepositions
        'از', 'به', 'با', 'در', 'بر', 'برای', 'تا', 'بی', 'مثل', 'مانند',
        'همچون', 'چون', 'مگر', 'جز', 'غیر', 'بدون',

        # Conjunctions
        'و', 'یا', 'اما', 'ولی', 'که', 'چه', 'اگر', 'پس',
        'زیرا', 'چونکه', 'چنانچه', 'هرچند', 'لیکن',

        # Determiners
        'یک', 'یکی', 'همه', 'تمام', 'بعضی', 'چند', 'هر', 'هیچ',
        'دیگر', 'بیش', 'کم', 'خیلی', 'بسیار',

        # Question words
        'چی', 'چه', 'کی', 'کجا', 'کدام', 'چرا', 'چگونه', 'چطور',
        'کدامین', 'چند',

        # Adverbs
        'خیلی', 'بسیار', 'بیش', 'کم', 'همیشه', 'هرگز', 'گاهی',
        'اکنون', 'حالا', 'امروز', 'دیروز', 'فردا', 'باز', 'بازهم',
        'دوباره', 'تنها', 'فقط', 'حتی', 'نیز', 'هم', 'آنجا', 'اینجا',

        # Common verbs
        'شد', 'شده', 'شود', 'شوند', 'شدند', 'شدم', 'شدی', 'شویم', 'شوید',
        'کرد', 'کرده', 'کنم', 'کنی', 'کند', 'کنید', 'کنند', 'می\u200cکند',
        'داشت', 'دارد', 'داشته', 'دارم', 'داری', 'داریم', 'دارید', 'دارند',
        'گفت', 'گوید', 'گفته', 'گویم', 'گویی', 'گوییم', 'گویید', 'گویند',

        # Negation
        'نه', 'نی', 'نمی', 'ن',

        # Possessive markers
        'ام', 'ات', 'اش', 'مان', 'تان', 'شان',

        # Others
        'را', 'رو', 'ای', 'هان', 'آری', 'بله', 'خیر',
        'البته', 'مثلا', 'یعنی', 'خب', 'آخه', 'الان',
        'وقتی', 'زمانی', 'هنگامی', 'آنگاه', 'سپس', 'آنگه',
        'نزد', 'پیش', 'کنار', 'نیمه', 'تر', 'ترین',
    }

    def __init__(self, custom_stopwords: Optional[Set[str]] = None,
                 include_defaults: bool = True):
        """
        Initialize stop words manager.

        Args:
            custom_stopwords: Additional custom stop words
            include_defaults: Whether to include default stop words
        """
        self.stopwords = set()

        if include_defaults:
            self.stopwords.update(self.DEFAULT_STOPWORDS)

        if custom_stopwords:
            self.stopwords.update(custom_stopwords)

    def is_stopword(self, word: str) -> bool:
        """
        Check if a word is a stop word.

        Args:
            word: Word to check

        Returns:
            True if word is a stop word
        """
        return word.strip() in self.stopwords

    def remove_stopwords(self, text: str) -> str:
        """
        Remove stop words from text.

        Args:
            text: Input text

        Returns:
            Text with stop words removed
        """
        words = text.split()
        filtered_words = [word for word in words if not self.is_stopword(word)]
        return ' '.join(filtered_words)

    def filter_stopwords(self, words: List[str]) -> List[str]:
        """
        Filter stop words from a list of words.

        Args:
            words: List of words

        Returns:
            List with stop words removed
        """
        return [word for word in words if not self.is_stopword(word)]

    def add_stopword(self, word: str) -> None:
        """
        Add a custom stop word.

        Args:
            word: Stop word to add
        """
        self.stopwords.add(word.strip())

    def add_stopwords(self, words: List[str]) -> None:
        """
        Add multiple custom stop words.

        Args:
            words: List of stop words to add
        """
        self.stopwords.update(word.strip() for word in words)

    def remove_stopword(self, word: str) -> None:
        """
        Remove a word from stop words list.

        Args:
            word: Word to remove
        """
        self.stopwords.discard(word.strip())

    def remove_stopwords_from_list(self, words: List[str]) -> None:
        """
        Remove multiple words from stop words list.

        Args:
            words: List of words to remove
        """
        for word in words:
            self.stopwords.discard(word.strip())

    def get_stopwords(self) -> Set[str]:
        """
        Get the current stop words set.

        Returns:
            Set of stop words
        """
        return self.stopwords.copy()

    def get_stopwords_list(self) -> List[str]:
        """
        Get the current stop words as a sorted list.

        Returns:
            Sorted list of stop words
        """
        return sorted(self.stopwords)

    def count_stopwords(self, text: str) -> int:
        """
        Count stop words in text.

        Args:
            text: Input text

        Returns:
            Number of stop words
        """
        words = text.split()
        return sum(1 for word in words if self.is_stopword(word))

    def stopword_ratio(self, text: str) -> float:
        """
        Calculate ratio of stop words to total words.

        Args:
            text: Input text

        Returns:
            Stop word ratio (0.0-1.0)
        """
        words = text.split()
        if not words:
            return 0.0

        stopword_count = self.count_stopwords(text)
        return stopword_count / len(words)

    def reset_to_defaults(self) -> None:
        """Reset stop words to default list."""
        self.stopwords = self.DEFAULT_STOPWORDS.copy()

    def clear(self) -> None:
        """Clear all stop words."""
        self.stopwords.clear()

    @staticmethod
    def get_default_stopwords() -> Set[str]:
        """
        Get the default Persian stop words.

        Returns:
            Set of default stop words
        """
        return PersianStopWords.DEFAULT_STOPWORDS.copy()

    @staticmethod
    def get_default_stopwords_list() -> List[str]:
        """
        Get the default Persian stop words as a sorted list.

        Returns:
            Sorted list of default stop words
        """
        return sorted(PersianStopWords.DEFAULT_STOPWORDS)
