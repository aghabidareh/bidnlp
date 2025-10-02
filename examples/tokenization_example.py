"""
Example usage of BidNLP tokenization modules
"""

from bidnlp.tokenization import (
    PersianWordTokenizer,
    PersianSentenceTokenizer,
    PersianCharacterTokenizer,
    PersianMorphemeTokenizer,
    PersianSyllableTokenizer
)


def word_tokenization_example():
    """Demonstrate word tokenization"""
    print("=" * 60)
    print("WORD TOKENIZATION")
    print("=" * 60)

    tokenizer = PersianWordTokenizer()

    # Simple example
    text1 = "سلام، حال شما چطور است؟"
    print(f"\nText: {text1}")
    print(f"Tokens: {tokenizer.tokenize(text1)}")

    # Mixed Persian-English
    text2 = "من Python را دوست دارم."
    print(f"\nText: {text2}")
    print(f"Tokens: {tokenizer.tokenize(text2)}")

    # With ZWNJ (compound words)
    text3 = "کتاب‌خانه بزرگی است."
    print(f"\nText: {text3}")
    print(f"Tokens: {tokenizer.tokenize(text3)}")

    # With positions
    text4 = "این یک آزمایش است"
    print(f"\nText: {text4}")
    print("Tokens with positions:")
    for token, start, end in tokenizer.tokenize_with_positions(text4):
        print(f"  '{token}' at position {start}-{end}")


def sentence_tokenization_example():
    """Demonstrate sentence tokenization"""
    print("\n" + "=" * 60)
    print("SENTENCE TOKENIZATION")
    print("=" * 60)

    tokenizer = PersianSentenceTokenizer()

    text = """
    فارسی یکی از زبان‌های هند و اروپایی است.
    این زبان در ایران رسمی است.
    آیا شما فارسی صحبت می‌کنید؟
    بله، من فارسی بلدم!
    """

    print(f"\nOriginal text:{text}")
    print("\nSentences:")
    sentences = tokenizer.tokenize(text.strip())
    for i, sent in enumerate(sentences, 1):
        print(f"{i}. {sent}")

    print(f"\nTotal sentences: {tokenizer.count_sentences(text)}")


def character_tokenization_example():
    """Demonstrate character tokenization"""
    print("\n" + "=" * 60)
    print("CHARACTER TOKENIZATION")
    print("=" * 60)

    tokenizer = PersianCharacterTokenizer()

    word = "سلام"
    print(f"\nWord: {word}")
    chars = tokenizer.tokenize(word)
    print(f"Characters: {chars}")

    # Reconstruct
    reconstructed = tokenizer.detokenize(chars)
    print(f"Reconstructed: {reconstructed}")


def morpheme_tokenization_example():
    """Demonstrate morpheme tokenization"""
    print("\n" + "=" * 60)
    print("MORPHEME TOKENIZATION")
    print("=" * 60)

    tokenizer = PersianMorphemeTokenizer()

    words = [
        "میروم",       # می + رو + م (present tense "I go")
        "کتابها",      # کتاب + ها (books)
        "بزرگتر",      # بزرگ + تر (bigger)
        "بزرگترین",    # بزرگ + ترین (biggest)
        "دانشجویان",   # دانشجو + ان (students)
        "نمیدانم",     # نمی + دان + م (I don't know)
        "بیکار",       # بی + کار (unemployed)
        "مهربانانه",   # مهربان + انه (kindly)
    ]

    print("\nMorpheme analysis:")
    for word in words:
        morphemes = tokenizer.tokenize(word)
        tagged = tokenizer.tokenize_with_tags(word)

        print(f"\n  {word}")
        print(f"    Morphemes: {' + '.join(morphemes)}")
        print(f"    Tagged: {tagged}")


def syllable_tokenization_example():
    """Demonstrate syllable tokenization"""
    print("\n" + "=" * 60)
    print("SYLLABLE TOKENIZATION")
    print("=" * 60)

    tokenizer = PersianSyllableTokenizer()

    words = ["سلام", "کتاب", "دانشگاه", "فارسی"]

    print("\nSyllable breakdown:")
    for word in words:
        syllables = tokenizer.tokenize(word)
        count = tokenizer.count_syllables(word)
        print(f"  {word}: {syllables} ({count} syllables)")


def complete_pipeline_example():
    """Demonstrate a complete NLP pipeline"""
    print("\n" + "=" * 60)
    print("COMPLETE TOKENIZATION PIPELINE")
    print("=" * 60)

    text = "من کتاب می‌خوانم. او هم کتاب می‌خواند!"

    # Step 1: Sentence tokenization
    sent_tokenizer = PersianSentenceTokenizer()
    sentences = sent_tokenizer.tokenize(text)

    print(f"\nOriginal text: {text}\n")
    print("Pipeline:")

    # Step 2: Word tokenization for each sentence
    word_tokenizer = PersianWordTokenizer()
    morpheme_tokenizer = PersianMorphemeTokenizer()

    for i, sentence in enumerate(sentences, 1):
        print(f"\n{i}. Sentence: {sentence}")

        words = word_tokenizer.tokenize(sentence)
        print(f"   Words: {words}")

        # Step 3: Morpheme analysis for verbs
        for word in words:
            if 'می' in word or word.endswith('م') or word.endswith('د'):
                morphemes = morpheme_tokenizer.tokenize(word)
                print(f"   {word} → morphemes: {morphemes}")


if __name__ == "__main__":
    word_tokenization_example()
    sentence_tokenization_example()
    character_tokenization_example()
    morpheme_tokenization_example()
    syllable_tokenization_example()
    complete_pipeline_example()

    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)
