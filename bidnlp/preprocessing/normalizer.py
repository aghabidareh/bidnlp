"""
Persian Text Normalizer

Comprehensive normalization for Persian text including:
- Character normalization (Arabic to Persian)
- ZWNJ and whitespace normalization
- Diacritic handling
- Direction marks removal
- Unicode normalization
"""

import re
import unicodedata
from typing import Optional


class PersianNormalizer:
    """
    Comprehensive normalizer for Persian (Farsi) text.

    Handles various normalization tasks to standardize Persian text.
    """

    def __init__(
        self,
        normalize_arabic: bool = True,
        normalize_zwnj: bool = True,
        remove_diacritics: bool = True,
        normalize_spacing: bool = True,
        fix_arabic_numbers: bool = True,
        remove_kashida: bool = True,
        unicode_form: str = 'NFKC'
    ):
        """
        Initialize the normalizer.

        Args:
            normalize_arabic: Convert Arabic characters to Persian
            normalize_zwnj: Normalize ZWNJ usage
            remove_diacritics: Remove Arabic diacritics
            normalize_spacing: Fix spacing issues
            fix_arabic_numbers: Convert Arabic-Indic digits to Persian
            remove_kashida: Remove kashida (ـ) character
            unicode_form: Unicode normalization form (NFC, NFKC, NFD, NFKD)
        """
        self.normalize_arabic = normalize_arabic
        self.normalize_zwnj = normalize_zwnj
        self.remove_diacritics = remove_diacritics
        self.normalize_spacing = normalize_spacing
        self.fix_arabic_numbers = fix_arabic_numbers
        self.remove_kashida = remove_kashida
        self.unicode_form = unicode_form

        # Arabic to Persian character mappings
        self.arabic_to_persian = {
            'ي': 'ی',      # Arabic yeh to Persian yeh
            'ك': 'ک',      # Arabic kaf to Persian kaf
            'ؤ': 'و',      # Arabic waw with hamza above
            'ۀ': 'ه',      # Persian heh with hamza above
            'ة': 'ه',      # Arabic teh marbuta
            'إ': 'ا',      # Arabic alef with hamza below
            'أ': 'ا',      # Arabic alef with hamza above
            'ٱ': 'ا',      # Arabic alef wasla
            'ٳ': 'ا',      # Arabic alef with hamza below
            'ٲ': 'ا',      # Arabic alef with madda above
            'ٵ': 'ا',      # Arabic alef
        }

        # Arabic-Indic to Persian digit mappings
        self.arabic_numbers = {
            '٠': '۰', '١': '۱', '٢': '۲', '٣': '۳', '٤': '۴',
            '٥': '۵', '٦': '۶', '٧': '۷', '٨': '۸', '٩': '۹'
        }

        # Diacritics (Tashkil) - Arabic vowel marks
        self.diacritics = (
            '\u064B'  # Fathatan
            '\u064C'  # Dammatan
            '\u064D'  # Kasratan
            '\u064E'  # Fatha
            '\u064F'  # Damma
            '\u0650'  # Kasra
            '\u0651'  # Shadda
            '\u0652'  # Sukun
            '\u0653'  # Maddah
            '\u0654'  # Hamza above
            '\u0655'  # Hamza below
            '\u0656'  # Subscript alef
            '\u0657'  # Inverted damma
            '\u0658'  # Mark noon ghunna
            '\u0670'  # Superscript alef
        )

        # Direction marks and other invisible characters
        self.invisible_chars = (
            '\u200B'  # Zero-width space
            '\u200D'  # Zero-width joiner
            '\u200E'  # Left-to-right mark
            '\u200F'  # Right-to-left mark
            '\u202A'  # Left-to-right embedding
            '\u202B'  # Right-to-left embedding
            '\u202C'  # Pop directional formatting
            '\u202D'  # Left-to-right override
            '\u202E'  # Right-to-left override
            '\uFEFF'  # Zero-width no-break space (BOM)
        )

        # Various space characters
        self.space_chars = {
            '\u00A0': ' ',  # Non-breaking space
            '\u2000': ' ',  # En quad
            '\u2001': ' ',  # Em quad
            '\u2002': ' ',  # En space
            '\u2003': ' ',  # Em space
            '\u2004': ' ',  # Three-per-em space
            '\u2005': ' ',  # Four-per-em space
            '\u2006': ' ',  # Six-per-em space
            '\u2007': ' ',  # Figure space
            '\u2008': ' ',  # Punctuation space
            '\u2009': ' ',  # Thin space
            '\u200A': ' ',  # Hair space
            '\u202F': ' ',  # Narrow no-break space
            '\u205F': ' ',  # Medium mathematical space
            '\u3000': ' ',  # Ideographic space
        }

        # Kashida character (Arabic tatweel)
        self.kashida = '\u0640'

    def normalize_characters(self, text: str) -> str:
        """Normalize Arabic characters to Persian equivalents"""
        if not self.normalize_arabic:
            return text

        for arabic, persian in self.arabic_to_persian.items():
            text = text.replace(arabic, persian)

        return text

    def normalize_numbers(self, text: str) -> str:
        """Convert Arabic-Indic numerals to Persian numerals"""
        if not self.fix_arabic_numbers:
            return text

        for arabic, persian in self.arabic_numbers.items():
            text = text.replace(arabic, persian)

        return text

    def remove_diacritic_marks(self, text: str) -> str:
        """Remove Arabic diacritical marks (Tashkil)"""
        if not self.remove_diacritics:
            return text

        return ''.join(c for c in text if c not in self.diacritics)

    def remove_kashida_char(self, text: str) -> str:
        """Remove kashida (tatweel) characters"""
        if not self.remove_kashida:
            return text

        return text.replace(self.kashida, '')

    def normalize_whitespace(self, text: str) -> str:
        """Normalize various whitespace characters"""
        if not self.normalize_spacing:
            return text

        # Replace various space characters with regular space
        for space_char, replacement in self.space_chars.items():
            text = text.replace(space_char, replacement)

        # Normalize multiple spaces to single space
        text = re.sub(r' +', ' ', text)

        # Normalize newlines
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Max 2 consecutive newlines

        # Remove spaces before punctuation
        text = re.sub(r'\s+([،؛؟!.,:;?!])', r'\1', text)

        # Add space after punctuation if missing
        text = re.sub(r'([،؛؟!.,:;?!])([^\s\d])', r'\1 \2', text)

        return text

    def normalize_zwnj_usage(self, text: str) -> str:
        """Normalize ZWNJ (zero-width non-joiner) usage"""
        if not self.normalize_zwnj:
            return text

        # Common patterns where ZWNJ should be used in Persian
        # Prefix + verb: می‌خورم، نمی‌دانم
        zwnj = '\u200c'
        text = re.sub(r'(می|نمی|بی|ن)(\S)', r'\1' + zwnj + r'\2', text)

        # Remove excessive ZWNJs
        text = re.sub(zwnj + '+', zwnj, text)

        # Remove ZWNJ at start/end of text
        text = text.strip(zwnj)

        return text

    def remove_invisible_characters(self, text: str) -> str:
        """Remove invisible Unicode characters except ZWNJ if needed"""
        # Keep ZWNJ if we're normalizing it
        if self.normalize_zwnj:
            invisible = ''.join(c for c in self.invisible_chars if c != '\u200c')
        else:
            invisible = self.invisible_chars

        return ''.join(c for c in text if c not in invisible)

    def apply_unicode_normalization(self, text: str) -> str:
        """Apply Unicode normalization"""
        if self.unicode_form:
            try:
                text = unicodedata.normalize(self.unicode_form, text)
            except Exception:
                # If normalization fails, continue without it
                pass

        return text

    def normalize(self, text: str) -> str:
        """
        Apply all normalization steps.

        Args:
            text: Input text to normalize

        Returns:
            Normalized text
        """
        if not text:
            return text

        # Apply Unicode normalization first
        text = self.apply_unicode_normalization(text)

        # Character normalization
        text = self.normalize_characters(text)

        # Number normalization
        text = self.normalize_numbers(text)

        # Remove diacritics
        text = self.remove_diacritic_marks(text)

        # Remove kashida
        text = self.remove_kashida_char(text)

        # Remove invisible characters
        text = self.remove_invisible_characters(text)

        # ZWNJ normalization
        text = self.normalize_zwnj_usage(text)

        # Whitespace normalization
        text = self.normalize_whitespace(text)

        # Final cleanup
        text = text.strip()

        return text

    def batch_normalize(self, texts: list) -> list:
        """
        Normalize multiple texts.

        Args:
            texts: List of texts to normalize

        Returns:
            List of normalized texts
        """
        return [self.normalize(text) for text in texts]
