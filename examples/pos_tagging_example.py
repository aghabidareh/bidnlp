"""
BidNLP POS Tagging Module Examples

This script demonstrates Persian Part-of-Speech tagging.
"""

from bidnlp.pos import (
    RuleBasedPOSTagger,
    HMMPOSTagger,
    PersianPOSTag,
    PersianPOSResources
)


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"{title:^60}")
    print('='*60 + '\n')


def rule_based_tagging_examples():
    """Demonstrate rule-based POS tagging."""
    print_section("Rule-Based POS Tagging")

    tagger = RuleBasedPOSTagger()

    # Example 1: Basic tagging
    print("1. Basic POS Tagging:")
    text = "من به دانشگاه می‌روم"
    tagged = tagger.tag(text)

    print(f"   Text: '{text}'")
    for word, tag in tagged:
        tag_desc = PersianPOSResources.get_tag_description(tag)
        print(f"   {word:15} → {tag:12} ({tag_desc})")

    # Example 2: Tagging sentences with different word types
    print("\n2. Tagging Different Word Types:")
    texts = [
        "این کتاب خیلی خوب است",
        "من و تو به خانه می‌رویم",
        "امروز هوا خیلی سرد است",
    ]

    for text in texts:
        tagged = tagger.tag(text)
        print(f"\n   Text: '{text}'")
        print(f"   Tags: {' | '.join([f'{w}({t})' for w, t in tagged])}")

    # Example 3: Get only specific POS tags
    print("\n3. Extract Words by POS Tag:")
    text = "من و دوستم به دانشگاه تهران رفتیم"
    tagged = tagger.tag(text)

    print(f"   Text: '{text}'")

    # Get pronouns
    pronouns = tagger.get_words_by_tag(text, PersianPOSTag.PRO_PERS.value)
    print(f"   Pronouns: {pronouns}")

    # Get prepositions
    preps = tagger.get_words_by_tag(text, PersianPOSTag.PREP.value)
    print(f"   Prepositions: {preps}")

    # Get nouns
    nouns = tagger.get_words_by_tag(text, PersianPOSTag.N.value)
    print(f"   Nouns: {nouns}")

    # Example 4: Tag distribution
    print("\n4. POS Tag Distribution:")
    text = "این کتاب خیلی خوب است و من آن را دوست دارم"
    distribution = tagger.get_tag_distribution(text)

    print(f"   Text: '{text}'")
    print(f"   Tag Distribution:")
    for tag, proportion in sorted(distribution.items(), key=lambda x: x[1], reverse=True):
        tag_desc = PersianPOSResources.get_tag_description(tag)
        print(f"   {tag:12} ({tag_desc:25}): {proportion:.1%}")

    # Example 5: Custom words
    print("\n5. Adding Custom Words:")
    tagger.add_noun("فناوری")
    tagger.add_adjective("نوآورانه")
    tagger.add_verb("پرواز")

    text = "فناوری نوآورانه"
    tagged = tagger.tag(text)

    print(f"   Added custom words: فناوری (noun), نوآورانه (adjective)")
    print(f"   Text: '{text}'")
    for word, tag in tagged:
        print(f"   {word:15} → {tag}")

    # Example 6: Handling different sentence types
    print("\n6. Different Sentence Types:")

    sentences = [
        ("این کتاب است.", "Declarative with punctuation"),
        ("آیا تو می‌آیی؟", "Interrogative"),
        ("چه زیبا است!", "Exclamatory"),
        ("برو آنجا.", "Imperative"),
    ]

    for text, sentence_type in sentences:
        tagged = tagger.tag(text)
        print(f"\n   {sentence_type}: '{text}'")
        for word, tag in tagged:
            print(f"   {word:15} → {tag}")


def hmm_tagging_examples():
    """Demonstrate HMM-based POS tagging."""
    print_section("HMM-Based POS Tagging")

    # Example 1: Training the tagger
    print("1. Training HMM Tagger:")

    # Prepare training data
    training_data = [
        [("من", "PRO_PERS"), ("به", "PREP"), ("خانه", "N"), ("می‌روم", "V_PRES")],
        [("او", "PRO_PERS"), ("کتاب", "N"), ("می‌خواند", "V_PRES")],
        [("ما", "PRO_PERS"), ("در", "PREP"), ("دانشگاه", "N"), ("هستیم", "V_AUX")],
        [("این", "PRO_DEM"), ("خوب", "ADJ"), ("است", "V_AUX")],
        [("آنها", "PRO_PERS"), ("امروز", "ADV_TIME"), ("آمدند", "V_PAST")],
        [("من", "PRO_PERS"), ("کتاب", "N"), ("خوب", "ADJ"), ("می‌خوانم", "V_PRES")],
        [("تو", "PRO_PERS"), ("به", "PREP"), ("مدرسه", "N"), ("می‌روی", "V_PRES")],
        [("او", "PRO_PERS"), ("از", "PREP"), ("شهر", "N"), ("آمد", "V_PAST")],
        [("ما", "PRO_PERS"), ("کار", "N"), ("می‌کنیم", "V_PRES")],
        [("شما", "PRO_PERS"), ("کجا", "PRO_INT"), ("هستید", "V_AUX")],
    ]

    tagger = HMMPOSTagger()
    tagger.train(training_data)

    print(f"   Trained on {len(training_data)} sentences")
    print(f"   Vocabulary size: {len(tagger.vocabulary)}")
    print(f"   Number of tags: {len(tagger.tagset)}")
    print(f"   Tags: {sorted(tagger.tagset)}")

    # Example 2: Tagging with trained model
    print("\n2. Tagging with Trained Model:")

    test_sentences = [
        "من به خانه می‌روم",
        "او کتاب می‌خواند",
        "ما در دانشگاه هستیم",
    ]

    for text in test_sentences:
        tagged = tagger.tag(text)
        print(f"\n   Text: '{text}'")
        for word, tag in tagged:
            tag_desc = PersianPOSResources.get_tag_description(tag)
            print(f"   {word:15} → {tag:12} ({tag_desc})")

    # Example 3: Handling unknown words
    print("\n3. Handling Unknown Words:")

    text = "من ناشناخته می‌بینم"  # 'ناشناخته' is unknown
    tagged = tagger.tag(text)

    print(f"   Text: '{text}' (contains unknown word)")
    for word, tag in tagged:
        known = "known" if word in tagger.vocabulary else "unknown"
        print(f"   {word:15} → {tag:12} ({known})")

    # Example 4: Transition probabilities
    print("\n4. Transition Probabilities:")

    transitions = [
        ("PRO_PERS", "PREP"),
        ("PRO_PERS", "N"),
        ("PREP", "N"),
        ("N", "V_PRES"),
    ]

    print(f"   Sample transition probabilities:")
    for prev_tag, next_tag in transitions:
        prob = tagger.get_transition_prob(prev_tag, next_tag)
        print(f"   {prev_tag:12} → {next_tag:12}: {prob:.4f}")

    # Example 5: Emission probabilities
    print("\n5. Emission Probabilities:")

    word_tag_pairs = [
        ("من", "PRO_PERS"),
        ("به", "PREP"),
        ("خانه", "N"),
        ("است", "V_AUX"),
    ]

    print(f"   Word emission probabilities:")
    for word, tag in word_tag_pairs:
        prob = tagger.get_emission_prob(tag, word)
        print(f"   P({word:10} | {tag:12}): {prob:.4f}")

    # Example 6: Most likely tag for a word
    print("\n6. Most Likely Tags for Words:")

    words = ["من", "به", "خانه", "کتاب"]
    for word in words:
        tag = tagger.get_most_likely_tag(word)
        tag_desc = PersianPOSResources.get_tag_description(tag)
        print(f"   {word:10} → {tag:12} ({tag_desc})")

    # Example 7: Save and load model
    print("\n7. Save and Load Model:")

    # Save model
    model_data = tagger.save_model()
    print(f"   Model saved")
    print(f"   Model contains: {list(model_data.keys())}")

    # Load into new tagger
    new_tagger = HMMPOSTagger()
    new_tagger.load_model(model_data)
    print(f"   Model loaded into new tagger")

    # Test loaded tagger
    text = "من به خانه می‌روم"
    tagged = new_tagger.tag(text)
    print(f"   Test with loaded model: '{text}'")
    print(f"   Result: {[(w, t) for w, t in tagged]}")


def comparison_examples():
    """Compare rule-based and HMM taggers."""
    print_section("Rule-Based vs HMM Comparison")

    # Prepare HMM tagger
    training_data = [
        [("من", "PRO_PERS"), ("به", "PREP"), ("خانه", "N"), ("می‌روم", "V_PRES")],
        [("او", "PRO_PERS"), ("کتاب", "N"), ("می‌خواند", "V_PRES")],
        [("ما", "PRO_PERS"), ("در", "PREP"), ("دانشگاه", "N"), ("هستیم", "V_AUX")],
        [("این", "PRO_DEM"), ("خوب", "ADJ"), ("است", "V_AUX")],
        [("من", "PRO_PERS"), ("کتاب", "N"), ("خوب", "ADJ"), ("می‌خوانم", "V_PRES")],
    ]

    rule_tagger = RuleBasedPOSTagger()
    hmm_tagger = HMMPOSTagger()
    hmm_tagger.train(training_data)

    # Example 1: Compare tagging results
    print("1. Comparing Tagging Results:")

    test_texts = [
        "من به دانشگاه می‌روم",
        "این کتاب خوب است",
    ]

    for text in test_texts:
        rule_tagged = rule_tagger.tag(text)
        hmm_tagged = hmm_tagger.tag(text)

        print(f"\n   Text: '{text}'")
        print(f"\n   Rule-based:")
        for word, tag in rule_tagged:
            print(f"   {word:15} → {tag}")

        print(f"\n   HMM-based:")
        for word, tag in hmm_tagged:
            print(f"   {word:15} → {tag}")

    # Example 2: Tag distribution comparison
    print("\n2. Tag Distribution Comparison:")

    text = "من و دوستم به دانشگاه می‌رویم"

    rule_dist = rule_tagger.get_tag_distribution(text)
    hmm_dist = hmm_tagger.get_tag_distribution(text)

    print(f"   Text: '{text}'")
    print(f"\n   Rule-based distribution:")
    for tag, prop in sorted(rule_dist.items(), key=lambda x: x[1], reverse=True):
        print(f"   {tag:12}: {prop:.2%}")

    print(f"\n   HMM-based distribution:")
    for tag, prop in sorted(hmm_dist.items(), key=lambda x: x[1], reverse=True):
        print(f"   {tag:12}: {prop:.2%}")


def advanced_examples():
    """Advanced POS tagging examples."""
    print_section("Advanced POS Tagging")

    tagger = RuleBasedPOSTagger()

    # Example 1: Analyzing text complexity
    print("1. Text Complexity Analysis:")

    texts = [
        ("من به خانه می‌روم", "Simple"),
        ("این کتاب خیلی جالب و آموزنده است", "Medium"),
        ("دانشمندان با استفاده از تکنولوژی‌های نوین به کشفیات مهمی دست یافتند", "Complex"),
    ]

    for text, complexity in texts:
        tagged = tagger.tag(text)
        counts = tagger.get_tag_counts(text)

        print(f"\n   {complexity} sentence: '{text}'")
        print(f"   Total words: {len(tagged)}")
        print(f"   Unique POS tags: {len(counts)}")
        print(f"   Tag variety: {counts}")

    # Example 2: Batch processing
    print("\n2. Batch Processing:")

    texts = [
        "من به مدرسه می‌روم",
        "او کتاب می‌خواند",
        "ما در خانه هستیم",
    ]

    results = tagger.tag_batch(texts)

    print(f"   Processed {len(texts)} texts:")
    for i, (text, tagged) in enumerate(zip(texts, results), 1):
        tags = [tag for word, tag in tagged]
        print(f"   {i}. '{text}'")
        print(f"      Tags: {tags}")

    # Example 3: Filtering by multiple tags
    print("\n3. Filtering by Multiple POS Tags:")

    text = "من و دوستم امروز به دانشگاه تهران رفتیم"
    tagged = tagger.tag(text)

    print(f"   Text: '{text}'")

    # Get all pronouns
    pronouns = [word for word, tag in tagged if tag.startswith("PRO")]
    print(f"   All pronouns: {pronouns}")

    # Get all verbs
    verbs = [word for word, tag in tagged if tag.startswith("V")]
    print(f"   All verbs: {verbs}")

    # Get all nouns
    nouns = [word for word, tag in tagged if tag.startswith("N")]
    print(f"   All nouns: {nouns}")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("BidNLP POS Tagging Module Examples".center(60))
    print("="*60)

    # Run each section
    rule_based_tagging_examples()
    hmm_tagging_examples()
    comparison_examples()
    advanced_examples()

    print("\n" + "="*60)
    print("Examples completed successfully!".center(60))
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
