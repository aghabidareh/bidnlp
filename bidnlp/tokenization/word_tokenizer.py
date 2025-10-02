"""
Persian Word Tokenizer

Handles the complexities of Persian word tokenization including:
- ZWNJ (zero-width non-joiner) handling
- Compound words
- Punctuation handling
- Number and date handling
- Mixed Persian-English text
"""

import re
from typing import List, Tuple


class PersianWordTokenizer:
    """
    Word tokenizer for Persian (Farsi) language.

    Handles Persian-specific challenges like ZWNJ, compound words,
    and mixed scripts.
    """

    def __init__(self, normalize_zwnj: bool = True, keep_whitespace: bool = False):
        """
        Initialize the word tokenizer.

        Args:
            normalize_zwnj: If True, normalizes ZWNJ usage
            keep_whitespace: If True, preserves whitespace tokens
        """
        self.normalize_zwnj = normalize_zwnj
        self.keep_whitespace = keep_whitespace

        # Persian character ranges
        self.persian_chars = r'[\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF]'

        # Punctuation marks
        self.persian_punctuation = '،؛؟٪×÷'
        self.latin_punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

        # Common Persian prefixes and suffixes that use ZWNJ
        self.prefix_patterns = [
            'می', 'نمی', 'بی', 'با', 'پیش', 'پس', 'هم', 'نا', 'غیر'
        ]

        self.suffix_patterns = [
            'ها', 'های', 'تر', 'ترین', 'ام', 'ات', 'اش',
            'مان', 'تان', 'شان', 'ی', 'گر', 'گری'
        ]

    def normalize(self, text: str) -> str:
        """Normalize Persian text"""
        if not text:
            return text

        # Normalize different types of spaces to regular space
        text = re.sub(r'[\u00A0\u2000-\u200F\u202F\u205F\u3000]', ' ', text)

        # Keep ZWNJ for now, we'll handle it specially
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
            text = text.replace(arabic, persian)

        # Remove Arabic diacritics
        text = re.sub(r'[\u064B-\u065F\u0670]', '', text)

        # Add space before punctuation marks for better tokenization
        # This helps separate punctuation from words
        # But be careful with periods in decimal numbers
        for punct in self.persian_punctuation + '!?':
            text = text.replace(punct, f' {punct} ')

        # Handle periods carefully - don't split decimal numbers
        # Replace period with space+period+space only if NOT between digits
        text = re.sub(r'(\D)\.(\D)', r'\1 . \2', text)  # Between non-digits
        text = re.sub(r'^\.(\D)', r' . \1', text)  # Start of text
        text = re.sub(r'(\D)\.$', r'\1 . ', text)  # End of text

        # Normalize multiple spaces
        text = re.sub(r' +', ' ', text)

        return text.strip()

    def handle_zwnj(self, text: str) -> str:
        """
        Handle ZWNJ (zero-width non-joiner) properly.

        ZWNJ is used in Persian for:
        1. Separating prefix/suffix from root (e.g., می‌رود)
        2. Compound words (e.g., دست‌کش)
        """
        if not self.normalize_zwnj:
            return text

        # Replace ZWNJ with a regular space for tokenization
        # But mark it specially so we can recognize compound words
        text = text.replace('\u200c', ' ')

        return text

    def tokenize(self, text: str, return_spans: bool = False) -> List[str]:
        """
        Tokenize Persian text into words.

        Args:
            text: Input text to tokenize
            return_spans: If True, returns (token, start, end) tuples

        Returns:
            List of tokens or list of (token, start, end) tuples
        """
        if not text:
            return []

        # Normalize the text
        original_text = text
        text = self.normalize(text)
        text = self.handle_zwnj(text)

        tokens = []
        current_pos = 0

        # Build the regex pattern
        persian_pattern = self.persian_chars + r'+'
        english_pattern = r'[a-zA-Z]+(?:[a-zA-Z0-9_\-]*[a-zA-Z0-9])?'
        number_pattern = r'\d+(?:[.,]\d+)*'
        punct_chars = re.escape(self.persian_punctuation + self.latin_punctuation)
        punct_pattern = f'[{punct_chars}]'
        whitespace_pattern = r'\s+'

        # Combine patterns with alternation
        pattern = f'({persian_pattern}|{english_pattern}|{number_pattern}|{punct_pattern}|{whitespace_pattern})'

        for match in re.finditer(pattern, text, re.UNICODE):
            token = match.group(0)
            start = match.start()
            end = match.end()

            # Skip whitespace unless keep_whitespace is True
            if token.strip() or self.keep_whitespace:
                if return_spans:
                    tokens.append((token.strip() if not self.keep_whitespace else token, start, end))
                else:
                    tokens.append(token.strip() if not self.keep_whitespace else token)

        # Filter empty tokens
        if not self.keep_whitespace:
            tokens = [t for t in tokens if t] if not return_spans else [(t, s, e) for t, s, e in tokens if t]

        return tokens

    def tokenize_with_positions(self, text: str) -> List[Tuple[str, int, int]]:
        """
        Tokenize text and return tokens with their positions.

        Returns:
            List of (token, start_pos, end_pos) tuples
        """
        return self.tokenize(text, return_spans=True)

    def detokenize(self, tokens: List[str]) -> str:
        """
        Reconstruct text from tokens.

        This is a best-effort reconstruction and may not perfectly
        match the original text.

        Args:
            tokens: List of tokens

        Returns:
            Reconstructed text
        """
        if not tokens:
            return ""

        result = []

        for i, token in enumerate(tokens):
            result.append(token)

            # Decide if we need a space after this token
            if i < len(tokens) - 1:
                next_token = tokens[i + 1]

                # Don't add space before/after punctuation
                if token in self.persian_punctuation + self.latin_punctuation:
                    continue
                if next_token in self.persian_punctuation + self.latin_punctuation:
                    continue

                # Add space between tokens
                result.append(' ')

        return ''.join(result)

    def split_compound_words(self, text: str) -> List[str]:
        """
        Split compound words that use ZWNJ.

        Example: دست‌کش -> ['دست', 'کش']

        Args:
            text: Input text

        Returns:
            List of word parts
        """
        # Split on ZWNJ
        parts = re.split(r'\u200c+', text)

        # Also split on regular spaces
        result = []
        for part in parts:
            if ' ' in part:
                result.extend(part.split())
            else:
                result.append(part)

        return [p for p in result if p.strip()]

    def get_token_type(self, token: str) -> str:
        """
        Determine the type of a token.

        Returns:
            One of: 'persian', 'english', 'number', 'punctuation', 'mixed', 'other'
        """
        if not token:
            return 'other'

        token = token.strip()

        # Check if it's punctuation
        if all(c in self.persian_punctuation + self.latin_punctuation for c in token):
            return 'punctuation'

        # Check if it's a number
        if re.match(r'^\d+(?:[.,]\d+)*$', token):
            return 'number'

        # Check if it's Persian
        if re.match(r'^' + self.persian_chars + r'+$', token, re.UNICODE):
            return 'persian'

        # Check if it's English
        if re.match(r'^[a-zA-Z]+$', token):
            return 'english'

        # Check if it's mixed
        has_persian = bool(re.search(self.persian_chars, token))
        has_latin = bool(re.search(r'[a-zA-Z]', token))

        if has_persian and has_latin:
            return 'mixed'

        return 'other'
