"""
BidNLP Utils Module Examples

This script demonstrates the usage of various utility functions in BidNLP.
"""

from bidnlp.utils import (
    PersianCharacters,
    PersianTextStatistics,
    PersianStopWords,
    PersianTextValidator,
    PersianTextMetrics
)


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"{title:^60}")
    print('='*60 + '\n')


def character_utilities_examples():
    """Demonstrate character utility functions."""
    print_section("Character Utilities")

    # Check character types
    print("1. Character Type Detection:")
    chars = ['س', 'ك', '۵', '٥', '5', '،', '\u200c']
    for char in chars:
        char_type = PersianCharacters.get_character_type(char)
        print(f"   '{char}' -> {char_type}")

    # Check if text is Persian
    print("\n2. Persian Text Detection:")
    texts = [
        "سلام دنیا",
        "hello world",
        "سلام hello",
    ]
    for text in texts:
        is_persian = PersianCharacters.is_persian_text(text, threshold=0.5)
        print(f"   '{text}' -> Persian: {is_persian}")

    # Count character types
    print("\n3. Character Type Counts:")
    text = "سلام دنیا ۱۲۳ hello"
    counts = PersianCharacters.count_character_types(text)
    print(f"   Text: '{text}'")
    for char_type, count in counts.items():
        if count > 0:
            print(f"   {char_type}: {count}")

    # Get Persian alphabet
    print("\n4. Persian Alphabet:")
    alphabet = PersianCharacters.get_persian_alphabet()
    print(f"   Total letters: {len(alphabet)}")
    print(f"   Sample: {list(alphabet)[:10]}")

    # Check for diacritics
    print("\n5. Diacritic Detection:")
    text_with_diacritics = "سَلامٌ"
    text_clean = PersianCharacters.remove_diacritics(text_with_diacritics)
    print(f"   Original: '{text_with_diacritics}'")
    print(f"   Cleaned: '{text_clean}'")


def statistics_examples():
    """Demonstrate text statistics functions."""
    print_section("Text Statistics")

    stats = PersianTextStatistics()

    text = """سلام دنیا. من به دانشگاه می‌روم. چطوری هستید؟

این یک پاراگراف دوم است. خیلی خوب است."""

    # Get comprehensive statistics
    print("1. Comprehensive Statistics:")
    statistics = stats.get_statistics(text)
    print(f"   Text preview: '{text[:30]}...'")
    print(f"\n   Statistics:")
    for key, value in statistics.items():
        print(f"   {key}: {value}")

    # Word frequency
    print("\n2. Word Frequency:")
    word_text = "سلام سلام دنیا سلام چطوری دنیا"
    freq = stats.word_frequency(word_text, top_n=3)
    print(f"   Text: '{word_text}'")
    print(f"   Top 3 words:")
    for word, count in freq:
        print(f"   '{word}': {count}")

    # N-grams
    print("\n3. Bigrams:")
    ngram_text = "من به دانشگاه می روم"
    bigrams = stats.get_ngrams(ngram_text, n=2)
    print(f"   Text: '{ngram_text}'")
    print(f"   Bigrams: {bigrams[:3]}")

    # Longest/shortest word
    print("\n4. Longest and Shortest Words:")
    word_text = "من دانشگاه به کتاب می‌روم"
    longest = stats.longest_word(word_text)
    shortest = stats.shortest_word(word_text)
    print(f"   Text: '{word_text}'")
    print(f"   Longest: '{longest}' ({len(longest)} chars)")
    print(f"   Shortest: '{shortest}' ({len(shortest)} chars)")


def stopwords_examples():
    """Demonstrate stop words functions."""
    print_section("Stop Words")

    stopwords = PersianStopWords()

    # Check stop words
    print("1. Stop Word Detection:")
    words = ['من', 'از', 'دانشگاه', 'به', 'کتاب']
    for word in words:
        is_stop = stopwords.is_stopword(word)
        print(f"   '{word}' -> Stop word: {is_stop}")

    # Remove stop words
    print("\n2. Remove Stop Words:")
    text = "من از دانشگاه به خانه می روم"
    filtered = stopwords.remove_stopwords(text)
    print(f"   Original: '{text}'")
    print(f"   Filtered: '{filtered}'")

    # Stop word statistics
    print("\n3. Stop Word Statistics:")
    count = stopwords.count_stopwords(text)
    ratio = stopwords.stopword_ratio(text)
    print(f"   Text: '{text}'")
    print(f"   Stop word count: {count}")
    print(f"   Stop word ratio: {ratio:.2%}")

    # Custom stop words
    print("\n4. Custom Stop Words:")
    custom_stops = PersianStopWords(custom_stopwords={'دانشگاه'}, include_defaults=True)
    text = "من به دانشگاه می روم"
    filtered = custom_stops.remove_stopwords(text)
    print(f"   Added 'دانشگاه' as stop word")
    print(f"   Original: '{text}'")
    print(f"   Filtered: '{filtered}'")

    # Get stop words list
    print("\n5. Stop Words List (first 10):")
    stop_list = stopwords.get_stopwords_list()[:10]
    print(f"   {stop_list}")


def validator_examples():
    """Demonstrate text validation functions."""
    print_section("Text Validation")

    validator = PersianTextValidator()

    # Validate Persian text
    print("1. Persian Text Validation:")
    texts = [
        "سلام دنیا",
        "hello world",
        "سلام كتاب",  # Arabic kaf
    ]
    for text in texts:
        is_valid = validator.is_valid_persian_text(text)
        print(f"   '{text}' -> Valid Persian: {is_valid}")

    # Check normalization
    print("\n2. Normalization Check:")
    texts = [
        "سلام دنیا ۱۲۳",
        "سلام كتاب",  # Arabic kaf
        "سلام ۱۲ 34",  # Mixed digits
    ]
    for text in texts:
        is_normalized = validator.is_normalized(text)
        print(f"   '{text}' -> Normalized: {is_normalized}")

    # Comprehensive validation
    print("\n3. Comprehensive Validation:")
    text = "سلام دنیا. چطوری هستید؟"
    result = validator.validate_text(text)
    print(f"   Text: '{text}'")
    print(f"   Valid: {result['is_valid']}")
    print(f"   Persian: {result['is_valid_persian']}")
    print(f"   Normalized: {result['is_normalized']}")
    print(f"   Proper spacing: {result['has_proper_spacing']}")
    if result['issues']:
        print(f"   Issues: {result['issues']}")

    # Quality score
    print("\n4. Quality Score:")
    texts = [
        "سلام دنیا چطوری",
        "سلام كتاب",  # Arabic kaf
        "hello world",
    ]
    for text in texts:
        score = validator.get_quality_score(text)
        print(f"   '{text}' -> Score: {score:.2f}")

    # Check for special content
    print("\n5. Special Content Detection:")
    text = "سلام https://test.com @user #hashtag"
    print(f"   Text: '{text}'")
    print(f"   Has URL: {validator.has_url(text)}")
    print(f"   Has mention: {validator.has_mention(text)}")
    print(f"   Has hashtag: {validator.has_hashtag(text)}")
    print(f"   Is clean: {validator.is_clean_text(text)}")


def metrics_examples():
    """Demonstrate evaluation metrics."""
    print_section("Evaluation Metrics")

    # Precision, Recall, F1
    print("1. Classification Metrics:")
    predicted = {'a', 'b', 'c', 'd'}
    actual = {'a', 'b', 'e', 'f'}

    precision = PersianTextMetrics.precision(predicted, actual)
    recall = PersianTextMetrics.recall(predicted, actual)
    f1 = PersianTextMetrics.f1_score(predicted, actual)

    print(f"   Predicted: {predicted}")
    print(f"   Actual: {actual}")
    print(f"   Precision: {precision:.4f}")
    print(f"   Recall: {recall:.4f}")
    print(f"   F1 Score: {f1:.4f}")

    # Edit distance
    print("\n2. Edit Distance:")
    pairs = [
        ("سلام", "سلام"),
        ("سلام", "سلاف"),
        ("سلام", "سلامم"),
    ]
    for str1, str2 in pairs:
        distance = PersianTextMetrics.edit_distance(str1, str2)
        similarity = PersianTextMetrics.similarity(str1, str2)
        print(f"   '{str1}' <-> '{str2}'")
        print(f"   Distance: {distance}, Similarity: {similarity:.4f}")

    # Jaccard similarity
    print("\n3. Jaccard Similarity:")
    set1 = {'کتاب', 'مداد', 'خودکار'}
    set2 = {'کتاب', 'دفتر', 'خودکار'}
    jaccard = PersianTextMetrics.jaccard_similarity(set1, set2)
    print(f"   Set 1: {set1}")
    print(f"   Set 2: {set2}")
    print(f"   Jaccard: {jaccard:.4f}")

    # Word/Character Error Rate
    print("\n4. Error Rates:")
    predicted = "من به دانشگاه می روم"
    actual = "من به دانشگاه می رفتم"

    wer = PersianTextMetrics.word_error_rate(predicted, actual)
    cer = PersianTextMetrics.character_error_rate(predicted, actual)

    print(f"   Predicted: '{predicted}'")
    print(f"   Actual: '{actual}'")
    print(f"   WER: {wer:.4f}")
    print(f"   CER: {cer:.4f}")

    # BLEU score
    print("\n5. BLEU Score:")
    predicted = "من به دانشگاه می روم"
    actual = "من به دانشگاه می رفتم"
    bleu = PersianTextMetrics.bleu_score(predicted, actual)
    print(f"   Predicted: '{predicted}'")
    print(f"   Actual: '{actual}'")
    print(f"   BLEU: {bleu:.4f}")

    # Classification report
    print("\n6. Classification Report:")
    predicted = ['pos', 'neg', 'pos', 'neu', 'pos']
    actual = ['pos', 'neg', 'neg', 'neu', 'pos']

    report = PersianTextMetrics.classification_report(predicted, actual)
    print(f"   Predicted: {predicted}")
    print(f"   Actual: {actual}")
    print(f"\n   Report:")
    for label, metrics in report.items():
        if label != 'overall':
            print(f"   {label}: P={metrics['precision']:.2f}, "
                  f"R={metrics['recall']:.2f}, F1={metrics['f1_score']:.2f}")
    print(f"   Overall Accuracy: {report['overall']['accuracy']:.2f}")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("BidNLP Utils Module Examples".center(60))
    print("="*60)

    # Run each section
    character_utilities_examples()
    statistics_examples()
    stopwords_examples()
    validator_examples()
    metrics_examples()

    print("\n" + "="*60)
    print("Examples completed successfully!".center(60))
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
