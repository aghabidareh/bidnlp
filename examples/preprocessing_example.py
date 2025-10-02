"""
Example usage of BidNLP preprocessing modules
"""

from bidnlp.preprocessing import (
    PersianNormalizer,
    PersianTextCleaner,
    PersianNumberNormalizer,
    PersianDateNormalizer,
    PersianPunctuationNormalizer
)


def normalization_example():
    """Demonstrate text normalization"""
    print("=" * 60)
    print("TEXT NORMALIZATION")
    print("=" * 60)

    normalizer = PersianNormalizer()

    # Example 1: Arabic to Persian conversion
    text1 = "كتاب يک مدرسة"
    print(f"\n1. Arabic to Persian:")
    print(f"   Before: {text1}")
    print(f"   After:  {normalizer.normalize(text1)}")

    # Example 2: Diacritic removal
    text2 = "كِتَابٌ مُفِيدٌ"
    print(f"\n2. Diacritic removal:")
    print(f"   Before: {text2}")
    print(f"   After:  {normalizer.normalize(text2)}")

    # Example 3: Whitespace normalization
    text3 = "این    متن     دارای    فاصله‌های     زیاد  است"
    print(f"\n3. Whitespace normalization:")
    print(f"   Before: '{text3}'")
    print(f"   After:  '{normalizer.normalize(text3)}'")

    # Example 4: ZWNJ normalization
    text4 = "من میروم و میخوانم"
    print(f"\n4. ZWNJ normalization:")
    print(f"   Before: {text4}")
    print(f"   After:  {normalizer.normalize(text4)}")


def cleaning_example():
    """Demonstrate text cleaning"""
    print("\n" + "=" * 60)
    print("TEXT CLEANING")
    print("=" * 60)

    # Example 1: URL and email cleaning
    cleaner1 = PersianTextCleaner(
        replace_urls_with='<URL>',
        replace_emails_with='<EMAIL>'
    )

    text1 = "برای اطلاعات بیشتر به https://example.com مراجعه کنید یا به info@example.com ایمیل بزنید"
    print(f"\n1. URL & Email handling:")
    print(f"   Before: {text1}")
    print(f"   After:  {cleaner1.clean(text1)}")

    # Example 2: HTML removal
    text2 = "<p>این یک <strong>متن</strong> با <em>تگ‌های</em> HTML است</p>"
    cleaner2 = PersianTextCleaner(remove_html=True)
    print(f"\n2. HTML tag removal:")
    print(f"   Before: {text2}")
    print(f"   After:  {cleaner2.clean(text2)}")

    # Example 3: Social media cleanup
    text3 = "سلام @کاربر! این #ایران است 😊"
    cleaner3 = PersianTextCleaner(
        replace_mentions_with='<USER>',
        replace_hashtags_with='<TAG>',
        remove_emojis=True
    )
    print(f"\n3. Social media cleanup:")
    print(f"   Before: {text3}")
    print(f"   After:  {cleaner3.clean(text3)}")

    # Example 4: Keep only Persian text
    text4 = "Persian فارسی with English 123 and numbers"
    cleaner4 = PersianTextCleaner()
    result4 = cleaner4.remove_non_persian(text4, keep_numbers=True)
    print(f"\n4. Keep only Persian (+ numbers):")
    print(f"   Before: {text4}")
    print(f"   After:  {result4}")


def number_normalization_example():
    """Demonstrate number normalization"""
    print("\n" + "=" * 60)
    print("NUMBER NORMALIZATION")
    print("=" * 60)

    normalizer = PersianNumberNormalizer()

    # Example 1: Digit normalization
    text1 = "شماره من ۰۹۱۲۳۴۵۶۷۸۹ و کد پستی ٤٥٦٧٨ است"
    print(f"\n1. Normalize to English digits:")
    print(f"   Before: {text1}")
    print(f"   After:  {normalizer.normalize_digits(text1, 'english')}")

    text2 = "My number is 123456789"
    print(f"\n2. Normalize to Persian digits:")
    print(f"   Before: {text2}")
    print(f"   After:  {normalizer.normalize_digits(text2, 'persian')}")

    # Example 3: Word to number conversion
    text3 = "من یک کتاب دارم و دو قلم"
    print(f"\n3. Convert number words to digits:")
    print(f"   Before: {text3}")
    print(f"   After:  {normalizer.convert_words_to_numbers(text3)}")

    # Example 4: Number to word conversion
    numbers = [1, 10, 25, 100, 250]
    print(f"\n4. Convert digits to Persian words:")
    for num in numbers:
        word = normalizer.number_to_word(num)
        print(f"   {num} -> {word}")

    # Example 5: Phone number formatting
    text5 = "تماس بگیرید: ۰۹۱۲۳۴۵۶۷۸۹"
    print(f"\n5. Phone number formatting:")
    print(f"   Before: {text5}")
    print(f"   After:  {normalizer.normalize_phone_numbers(text5)}")


def date_normalization_example():
    """Demonstrate date normalization"""
    print("\n" + "=" * 60)
    print("DATE NORMALIZATION")
    print("=" * 60)

    normalizer = PersianDateNormalizer()

    # Example: Date format normalization
    text = "تاریخ‌های مهم: 1400/1/1 و 99-12-29 و 1398/5/7"
    print(f"\nDate format standardization:")
    print(f"   Before: {text}")
    print(f"   After:  {normalizer.normalize_date_format(text)}")

    # Extract dates
    dates = normalizer.extract_dates(text)
    print(f"   Extracted dates: {dates}")


def punctuation_normalization_example():
    """Demonstrate punctuation normalization"""
    print("\n" + "=" * 60)
    print("PUNCTUATION NORMALIZATION")
    print("=" * 60)

    # Example 1: Convert to Persian punctuation
    normalizer1 = PersianPunctuationNormalizer(target_style='persian')
    text1 = "سلام, حال شما چطور است?"
    print(f"\n1. Normalize to Persian punctuation:")
    print(f"   Before: {text1}")
    print(f"   After:  {normalizer1.normalize(text1)}")

    # Example 2: Quotation marks
    text2 = 'او گفت "سلام" و رفت'
    print(f"\n2. Normalize quotation marks:")
    print(f"   Before: {text2}")
    print(f"   After:  {normalizer1.normalize(text2)}")

    # Example 3: Fix spacing
    text3 = "سلام،حال شما چطور است ؟من خوبم !"
    print(f"\n3. Fix spacing around punctuation:")
    print(f"   Before: {text3}")
    print(f"   After:  {normalizer1.normalize(text3)}")


def complete_pipeline_example():
    """Demonstrate a complete preprocessing pipeline"""
    print("\n" + "=" * 60)
    print("COMPLETE PREPROCESSING PIPELINE")
    print("=" * 60)

    # Raw input text with various issues
    raw_text = """
    <p>كتاب   «فارسي» را  ميخوانم .</p>
    شماره  من  ۰۹۱۲۳۴۵۶۷۸۹   است  .
    ببینید https://example.com
    @کاربر سلام! #test
    """

    print(f"\nOriginal text:{raw_text}")

    # Step 1: Clean HTML and social media content
    cleaner = PersianTextCleaner(
        remove_html=True,
        replace_urls_with='<URL>',
        replace_mentions_with='<USER>',
        replace_hashtags_with='<TAG>'
    )
    text = cleaner.clean(raw_text)
    print(f"\nAfter cleaning:\n{text}")

    # Step 2: Normalize text
    normalizer = PersianNormalizer()
    text = normalizer.normalize(text)
    print(f"\nAfter normalization:\n{text}")

    # Step 3: Normalize numbers
    num_normalizer = PersianNumberNormalizer()
    text = num_normalizer.normalize_digits(text, 'persian')
    print(f"\nAfter number normalization:\n{text}")

    # Step 4: Normalize punctuation
    punct_normalizer = PersianPunctuationNormalizer(target_style='persian')
    text = punct_normalizer.normalize(text)
    print(f"\nFinal result:\n{text}")


if __name__ == "__main__":
    normalization_example()
    cleaning_example()
    number_normalization_example()
    date_normalization_example()
    punctuation_normalization_example()
    complete_pipeline_example()

    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)
