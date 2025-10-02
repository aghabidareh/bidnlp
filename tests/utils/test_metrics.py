"""
Tests for Persian text metrics
"""

import pytest
from bidnlp.utils import PersianTextMetrics


class TestPersianTextMetrics:
    """Test cases for PersianTextMetrics class."""

    def test_precision(self):
        """Test precision calculation."""
        predicted = {'a', 'b', 'c'}
        actual = {'a', 'b', 'd'}

        precision = PersianTextMetrics.precision(predicted, actual)
        assert abs(precision - 0.6667) < 0.01  # 2/3

    def test_recall(self):
        """Test recall calculation."""
        predicted = {'a', 'b', 'c'}
        actual = {'a', 'b', 'd'}

        recall = PersianTextMetrics.recall(predicted, actual)
        assert abs(recall - 0.6667) < 0.01  # 2/3

    def test_f1_score(self):
        """Test F1 score calculation."""
        predicted = {'a', 'b', 'c'}
        actual = {'a', 'b', 'd'}

        f1 = PersianTextMetrics.f1_score(predicted, actual)
        assert abs(f1 - 0.6667) < 0.01

    def test_accuracy(self):
        """Test accuracy calculation."""
        predicted = ['a', 'b', 'c', 'd']
        actual = ['a', 'b', 'c', 'e']

        accuracy = PersianTextMetrics.accuracy(predicted, actual)
        assert accuracy == 0.75  # 3/4

    def test_edit_distance(self):
        """Test edit distance calculation."""
        # No changes
        assert PersianTextMetrics.edit_distance("سلام", "سلام") == 0

        # One substitution
        assert PersianTextMetrics.edit_distance("سلام", "سلاف") == 1

        # One insertion
        assert PersianTextMetrics.edit_distance("سلام", "سلامم") == 1

        # One deletion
        assert PersianTextMetrics.edit_distance("سلام", "سلا") == 1

    def test_similarity(self):
        """Test similarity calculation."""
        # Identical strings
        assert PersianTextMetrics.similarity("سلام", "سلام") == 1.0

        # Completely different
        sim = PersianTextMetrics.similarity("سلام", "خداحافظ")
        assert sim < 1.0

        # Similar strings
        sim = PersianTextMetrics.similarity("سلام", "سلامم")
        assert 0.5 < sim < 1.0

    def test_jaccard_similarity(self):
        """Test Jaccard similarity."""
        set1 = {'a', 'b', 'c'}
        set2 = {'b', 'c', 'd'}

        jaccard = PersianTextMetrics.jaccard_similarity(set1, set2)
        assert jaccard == 0.5  # 2 intersection / 4 union

    def test_cosine_similarity(self):
        """Test cosine similarity."""
        vec1 = [1.0, 2.0, 3.0]
        vec2 = [1.0, 2.0, 3.0]

        # Identical vectors
        cosine = PersianTextMetrics.cosine_similarity(vec1, vec2)
        assert abs(cosine - 1.0) < 0.01

        # Orthogonal vectors
        vec3 = [1.0, 0.0, 0.0]
        vec4 = [0.0, 1.0, 0.0]
        cosine = PersianTextMetrics.cosine_similarity(vec3, vec4)
        assert abs(cosine) < 0.01

    def test_word_error_rate(self):
        """Test Word Error Rate calculation."""
        predicted = "سلام دنیا"
        actual = "سلام دنیا"

        # Perfect match
        wer = PersianTextMetrics.word_error_rate(predicted, actual)
        assert wer == 0.0

        predicted = "سلام جهان"
        actual = "سلام دنیا"

        # One word different
        wer = PersianTextMetrics.word_error_rate(predicted, actual)
        assert wer > 0.0

    def test_character_error_rate(self):
        """Test Character Error Rate calculation."""
        predicted = "سلام"
        actual = "سلام"

        # Perfect match
        cer = PersianTextMetrics.character_error_rate(predicted, actual)
        assert cer == 0.0

        predicted = "سلاف"
        actual = "سلام"

        # One character different
        cer = PersianTextMetrics.character_error_rate(predicted, actual)
        assert cer > 0.0

    def test_bleu_score(self):
        """Test BLEU score calculation."""
        predicted = "سلام دنیا"
        actual = "سلام دنیا"

        # Perfect match
        bleu = PersianTextMetrics.bleu_score(predicted, actual)
        assert bleu == 1.0

        predicted = "سلام جهان"
        actual = "سلام دنیا"

        # Partial match
        bleu = PersianTextMetrics.bleu_score(predicted, actual)
        assert 0.0 < bleu < 1.0

    def test_confusion_matrix(self):
        """Test confusion matrix calculation."""
        predicted = ['a', 'b', 'a', 'c']
        actual = ['a', 'b', 'b', 'c']

        cm = PersianTextMetrics.confusion_matrix(predicted, actual)

        assert cm['total'] == 4
        assert 'a' in cm['labels']
        assert 'b' in cm['labels']
        assert 'c' in cm['labels']

    def test_classification_report(self):
        """Test classification report generation."""
        predicted = ['a', 'b', 'a', 'c']
        actual = ['a', 'b', 'b', 'c']

        report = PersianTextMetrics.classification_report(predicted, actual)

        assert 'a' in report
        assert 'b' in report
        assert 'c' in report
        assert 'overall' in report

        # Check that metrics are present
        assert 'precision' in report['a']
        assert 'recall' in report['a']
        assert 'f1_score' in report['a']
        assert 'support' in report['a']

    def test_empty_sets(self):
        """Test metrics with empty sets."""
        empty = set()
        non_empty = {'a', 'b'}

        assert PersianTextMetrics.precision(empty, non_empty) == 0.0
        assert PersianTextMetrics.recall(empty, non_empty) == 0.0
        assert PersianTextMetrics.f1_score(empty, non_empty) == 0.0

    def test_identical_sets(self):
        """Test metrics with identical sets."""
        set1 = {'a', 'b', 'c'}
        set2 = {'a', 'b', 'c'}

        assert PersianTextMetrics.precision(set1, set2) == 1.0
        assert PersianTextMetrics.recall(set1, set2) == 1.0
        assert PersianTextMetrics.f1_score(set1, set2) == 1.0
        assert PersianTextMetrics.jaccard_similarity(set1, set2) == 1.0

    def test_empty_strings_similarity(self):
        """Test similarity with empty strings."""
        assert PersianTextMetrics.similarity("", "") == 1.0
        assert PersianTextMetrics.similarity("", "test") == 0.0
        assert PersianTextMetrics.similarity("test", "") == 0.0

    def test_persian_text_metrics(self):
        """Test metrics on Persian text."""
        predicted = "من به دانشگاه می روم"
        actual = "من به دانشگاه می رفتم"

        # Calculate various metrics
        wer = PersianTextMetrics.word_error_rate(predicted, actual)
        cer = PersianTextMetrics.character_error_rate(predicted, actual)
        similarity = PersianTextMetrics.similarity(predicted, actual)

        assert 0.0 <= wer
        assert 0.0 <= cer <= 1.0
        assert 0.0 <= similarity <= 1.0

    def test_cosine_similarity_edge_cases(self):
        """Test cosine similarity edge cases."""
        # Zero vectors
        zero_vec = [0.0, 0.0, 0.0]
        vec = [1.0, 2.0, 3.0]

        cosine = PersianTextMetrics.cosine_similarity(zero_vec, vec)
        assert cosine == 0.0

    def test_cosine_similarity_different_lengths(self):
        """Test cosine similarity with different length vectors."""
        vec1 = [1.0, 2.0]
        vec2 = [1.0, 2.0, 3.0]

        with pytest.raises(ValueError):
            PersianTextMetrics.cosine_similarity(vec1, vec2)

    def test_accuracy_different_lengths(self):
        """Test accuracy with different length lists."""
        predicted = ['a', 'b']
        actual = ['a', 'b', 'c']

        accuracy = PersianTextMetrics.accuracy(predicted, actual)
        assert accuracy == 0.0  # Different lengths

    def test_bleu_score_edge_cases(self):
        """Test BLEU score edge cases."""
        # Empty strings
        assert PersianTextMetrics.bleu_score("", "") == 0.0
        assert PersianTextMetrics.bleu_score("test", "") == 0.0
        assert PersianTextMetrics.bleu_score("", "test") == 0.0

    def test_confusion_matrix_different_lengths(self):
        """Test confusion matrix with different length lists."""
        predicted = ['a', 'b']
        actual = ['a', 'b', 'c']

        with pytest.raises(ValueError):
            PersianTextMetrics.confusion_matrix(predicted, actual)

    def test_classification_report_different_lengths(self):
        """Test classification report with different length lists."""
        predicted = ['a', 'b']
        actual = ['a', 'b', 'c']

        with pytest.raises(ValueError):
            PersianTextMetrics.classification_report(predicted, actual)

    def test_perfect_scores(self):
        """Test that perfect predictions give perfect scores."""
        predicted = {'a', 'b', 'c'}
        actual = {'a', 'b', 'c'}

        assert PersianTextMetrics.precision(predicted, actual) == 1.0
        assert PersianTextMetrics.recall(predicted, actual) == 1.0
        assert PersianTextMetrics.f1_score(predicted, actual) == 1.0

    def test_no_overlap_scores(self):
        """Test scores with no overlap between predictions and actual."""
        predicted = {'a', 'b', 'c'}
        actual = {'x', 'y', 'z'}

        assert PersianTextMetrics.precision(predicted, actual) == 0.0
        assert PersianTextMetrics.recall(predicted, actual) == 0.0
        assert PersianTextMetrics.f1_score(predicted, actual) == 0.0
        assert PersianTextMetrics.jaccard_similarity(predicted, actual) == 0.0
