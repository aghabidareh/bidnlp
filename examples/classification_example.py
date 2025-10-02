"""
BidNLP Classification Module Examples

This script demonstrates text classification and sentiment analysis.
"""

from bidnlp.classification import (
    PersianSentimentAnalyzer,
    KeywordClassifier,
    BagOfWords,
    TfidfVectorizer,
    NgramExtractor
)


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"{title:^60}")
    print('='*60 + '\n')


def sentiment_analysis_examples():
    """Demonstrate sentiment analysis."""
    print_section("Sentiment Analysis")

    analyzer = PersianSentimentAnalyzer()

    # Example 1: Basic sentiment analysis
    print("1. Basic Sentiment Analysis:")
    texts = [
        "این کتاب خیلی خوب و جذاب است",
        "کیفیت بسیار ضعیف و گران است",
        "این یک کتاب است",
    ]

    for text in texts:
        sentiment = analyzer.predict(text)
        print(f"   '{text}'")
        print(f"   → Sentiment: {sentiment}\n")

    # Example 2: Detailed analysis
    print("2. Detailed Analysis:")
    text = "محصول عالی بود اما قیمت گران است"
    result = analyzer.analyze(text)

    print(f"   Text: '{text}'")
    print(f"   Sentiment: {result['sentiment']}")
    print(f"   Score: {result['score']:.2f}")
    print(f"   Positive words: {result['positive_words']}")
    print(f"   Negative words: {result['negative_words']}")

    # Example 3: Sentiment score
    print("\n3. Sentiment Score (-1 to 1):")
    texts = [
        "فوق‌العاده عالی و خوب",
        "افتضاح و بد",
    ]

    for text in texts:
        score = analyzer.get_sentiment_score(text)
        print(f"   '{text}' → Score: {score:.2f}")

    # Example 4: Probabilities
    print("\n4. Sentiment Probabilities:")
    text = "خوب بود"
    proba = analyzer.predict_proba(text)

    print(f"   Text: '{text}'")
    for sentiment, prob in proba.items():
        print(f"   {sentiment}: {prob:.2%}")

    # Example 5: Custom keywords
    print("\n5. Custom Keywords:")
    analyzer.add_positive_keyword('درخشان')
    text = "عملکرد درخشان تیم"
    sentiment = analyzer.predict(text)
    print(f"   Added custom positive keyword: 'درخشان'")
    print(f"   '{text}' → {sentiment}")


def keyword_classifier_examples():
    """Demonstrate keyword-based classification."""
    print_section("Keyword-Based Classification")

    classifier = KeywordClassifier()

    # Example 1: Manual category definition
    print("1. Manual Category Definition:")
    classifier.add_category('ورزش', {
        'فوتبال', 'بازیکن', 'تیم', 'گل', 'مسابقه', 'لیگ'
    })
    classifier.add_category('تکنولوژی', {
        'کامپیوتر', 'موبایل', 'نرم‌افزار', 'برنامه', 'اپلیکیشن'
    })
    classifier.add_category('سیاست', {
        'دولت', 'انتخابات', 'پارلمان', 'وزیر', 'مجلس'
    })

    # Classify texts
    texts = [
        "تیم فوتبال در مسابقه گل زد",
        "نرم‌افزار جدید کامپیوتر منتشر شد",
        "دولت انتخابات برگزار کرد",
    ]

    for text in texts:
        category = classifier.predict(text)
        print(f"   '{text}'")
        print(f"   → Category: {category}\n")

    # Example 2: Detailed classification
    print("2. Detailed Classification Results:")
    text = "بازیکن تیم ملی فوتبال گل زد"
    result = classifier.classify(text)

    print(f"   Text: '{text}'")
    print(f"   Category: {result['category']}")
    print(f"   Confidence: {result['confidence']:.2%}")
    print(f"   Scores: {result['scores']}")
    print(f"   Matched keywords: {result['matched_keywords']}")

    # Example 3: Training from data
    print("\n3. Training from Labeled Data:")
    train_texts = [
        "فوتبال بازی زیبایی است",
        "تیم ملی برد گرفت",
        "کامپیوتر ابزار مفیدی است",
        "نرم‌افزار جدید عرضه شد",
    ]
    train_labels = ['ورزش', 'ورزش', 'تکنولوژی', 'تکنولوژی']

    new_classifier = KeywordClassifier()
    new_classifier.train(train_texts, train_labels)

    test_text = "فوتبال"
    category = new_classifier.predict(test_text)
    print(f"   Trained on {len(train_texts)} examples")
    print(f"   Test: '{test_text}' → {category}")

    # Example 4: Top K predictions
    print("\n4. Top K Predictions:")
    text = "فوتبال"
    top_k = classifier.predict_top_k(text, k=2)

    print(f"   Text: '{text}'")
    print(f"   Top 2 categories:")
    for cat, prob in top_k:
        print(f"   {cat}: {prob:.2%}")


def feature_extraction_examples():
    """Demonstrate feature extraction."""
    print_section("Feature Extraction")

    docs = [
        "من به دانشگاه می روم",
        "دانشگاه تهران بزرگ است",
        "من کتاب می خوانم",
    ]

    # Example 1: Bag of Words
    print("1. Bag of Words:")
    bow = BagOfWords(max_features=10)
    vectors = bow.fit_transform(docs)

    print(f"   Documents: {len(docs)}")
    print(f"   Vocabulary: {bow.get_feature_names()[:5]}...")
    print(f"   First vector: {vectors[0]}")

    # Example 2: TF-IDF
    print("\n2. TF-IDF Vectorization:")
    tfidf = TfidfVectorizer(max_features=10)
    vectors = tfidf.fit_transform(docs)

    print(f"   Documents: {len(docs)}")
    print(f"   Vocabulary: {tfidf.get_feature_names()[:5]}...")
    print(f"   First vector (normalized): {dict(list(vectors[0].items())[:3])}...")

    # Example 3: N-grams
    print("\n3. N-gram Extraction:")

    # Bigrams
    bigram = NgramExtractor(n=2, max_features=10)
    bigram_vectors = bigram.fit_transform(docs)

    print(f"   Bigrams:")
    print(f"   Vocabulary: {bigram.get_feature_names()[:5]}")

    # Trigrams
    trigram = NgramExtractor(n=3, max_features=10)
    trigram_vectors = trigram.fit_transform(docs)

    print(f"\n   Trigrams:")
    print(f"   Vocabulary: {trigram.get_feature_names()[:3]}")

    # Example 4: Feature extraction pipeline
    print("\n4. Feature Extraction Pipeline:")
    text = "من به دانشگاه می روم"

    # Extract different features
    bow_vec = bow.transform([text])[0]
    tfidf_vec = tfidf.transform([text])[0]

    print(f"   Text: '{text}'")
    print(f"   BoW features: {len(bow_vec)} non-zero")
    print(f"   TF-IDF features: {len(tfidf_vec)} non-zero")


def combined_example():
    """Demonstrate combined classification workflow."""
    print_section("Combined Classification Workflow")

    # Prepare training data
    print("1. Preparing Training Data:")
    train_texts = [
        "فوتبال بازی زیبایی است",
        "تیم ملی برد گرفت",
        "گل زیبایی به ثمر رسید",
        "کامپیوتر سریع است",
        "نرم‌افزار جدید منتشر شد",
        "برنامه خوبی است",
    ]
    train_labels = ['ورزش', 'ورزش', 'ورزش', 'تکنولوژی', 'تکنولوژی', 'تکنولوژی']

    print(f"   Total samples: {len(train_texts)}")
    print(f"   Categories: {set(train_labels)}")

    # Train classifier
    print("\n2. Training Keyword Classifier:")
    classifier = KeywordClassifier(normalize=True, remove_stopwords=True)
    classifier.train(train_texts, train_labels)

    print(f"   Trained on {len(train_texts)} samples")
    print(f"   Categories: {classifier.get_categories()}")

    # Test classification
    print("\n3. Testing Classification:")
    test_texts = [
        "بازی فوتبال دیشب",
        "کامپیوتر و برنامه",
    ]

    for text in test_texts:
        prediction = classifier.predict(text)
        proba = classifier.predict_proba(text)

        print(f"\n   Text: '{text}'")
        print(f"   Prediction: {prediction}")
        print(f"   Probabilities:")
        for cat, prob in sorted(proba.items(), key=lambda x: x[1], reverse=True):
            print(f"      {cat}: {prob:.2%}")

    # Sentiment analysis
    print("\n4. Sentiment Analysis:")
    sentiment_analyzer = PersianSentimentAnalyzer()

    for text in test_texts:
        sentiment = sentiment_analyzer.predict(text)
        score = sentiment_analyzer.get_sentiment_score(text)

        print(f"\n   Text: '{text}'")
        print(f"   Sentiment: {sentiment}")
        print(f"   Score: {score:.2f}")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("BidNLP Classification Module Examples".center(60))
    print("="*60)

    # Run each section
    sentiment_analysis_examples()
    keyword_classifier_examples()
    feature_extraction_examples()
    combined_example()

    print("\n" + "="*60)
    print("Examples completed successfully!".center(60))
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
