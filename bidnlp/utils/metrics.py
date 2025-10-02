"""
Persian Text Metrics and Evaluation

Provides metrics for evaluating Persian text processing results.
"""

from typing import List, Set, Tuple, Optional


class PersianTextMetrics:
    """Metrics for evaluating Persian NLP tasks."""

    @staticmethod
    def precision(predicted: Set, actual: Set) -> float:
        """
        Calculate precision: TP / (TP + FP)

        Args:
            predicted: Set of predicted items
            actual: Set of actual/ground truth items

        Returns:
            Precision score (0.0-1.0)
        """
        if not predicted:
            return 0.0

        true_positives = len(predicted & actual)
        return true_positives / len(predicted)

    @staticmethod
    def recall(predicted: Set, actual: Set) -> float:
        """
        Calculate recall: TP / (TP + FN)

        Args:
            predicted: Set of predicted items
            actual: Set of actual/ground truth items

        Returns:
            Recall score (0.0-1.0)
        """
        if not actual:
            return 0.0

        true_positives = len(predicted & actual)
        return true_positives / len(actual)

    @staticmethod
    def f1_score(predicted: Set, actual: Set) -> float:
        """
        Calculate F1 score: 2 * (precision * recall) / (precision + recall)

        Args:
            predicted: Set of predicted items
            actual: Set of actual/ground truth items

        Returns:
            F1 score (0.0-1.0)
        """
        p = PersianTextMetrics.precision(predicted, actual)
        r = PersianTextMetrics.recall(predicted, actual)

        if p + r == 0:
            return 0.0

        return 2 * (p * r) / (p + r)

    @staticmethod
    def accuracy(predicted: List, actual: List) -> float:
        """
        Calculate accuracy: correct / total

        Args:
            predicted: List of predicted items
            actual: List of actual/ground truth items

        Returns:
            Accuracy score (0.0-1.0)
        """
        if not actual or len(predicted) != len(actual):
            return 0.0

        correct = sum(1 for p, a in zip(predicted, actual) if p == a)
        return correct / len(actual)

    @staticmethod
    def edit_distance(str1: str, str2: str) -> int:
        """
        Calculate Levenshtein edit distance between two strings.

        Args:
            str1: First string
            str2: Second string

        Returns:
            Edit distance (number of operations)
        """
        m, n = len(str1), len(str2)

        # Create DP table
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Initialize base cases
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        # Fill DP table
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i-1] == str2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i-1][j],     # deletion
                        dp[i][j-1],     # insertion
                        dp[i-1][j-1]    # substitution
                    )

        return dp[m][n]

    @staticmethod
    def similarity(str1: str, str2: str) -> float:
        """
        Calculate similarity based on edit distance (0.0-1.0).

        Args:
            str1: First string
            str2: Second string

        Returns:
            Similarity score (0.0-1.0)
        """
        if not str1 and not str2:
            return 1.0
        if not str1 or not str2:
            return 0.0

        distance = PersianTextMetrics.edit_distance(str1, str2)
        max_len = max(len(str1), len(str2))

        return 1.0 - (distance / max_len)

    @staticmethod
    def jaccard_similarity(set1: Set, set2: Set) -> float:
        """
        Calculate Jaccard similarity: |A ∩ B| / |A ∪ B|

        Args:
            set1: First set
            set2: Second set

        Returns:
            Jaccard similarity (0.0-1.0)
        """
        if not set1 and not set2:
            return 1.0

        intersection = len(set1 & set2)
        union = len(set1 | set2)

        if union == 0:
            return 0.0

        return intersection / union

    @staticmethod
    def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors.

        Args:
            vec1: First vector
            vec2: Second vector

        Returns:
            Cosine similarity (-1.0 to 1.0)
        """
        if len(vec1) != len(vec2):
            raise ValueError("Vectors must have the same length")

        if not vec1:
            return 0.0

        # Calculate dot product
        dot_product = sum(a * b for a, b in zip(vec1, vec2))

        # Calculate magnitudes
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5

        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0

        return dot_product / (magnitude1 * magnitude2)

    @staticmethod
    def word_error_rate(predicted: str, actual: str) -> float:
        """
        Calculate Word Error Rate (WER).

        Args:
            predicted: Predicted text
            actual: Actual/ground truth text

        Returns:
            WER score (0.0+, lower is better)
        """
        predicted_words = predicted.split()
        actual_words = actual.split()

        distance = PersianTextMetrics.edit_distance(
            ' '.join(predicted_words),
            ' '.join(actual_words)
        )

        if not actual_words:
            return float('inf') if predicted_words else 0.0

        return distance / len(actual_words)

    @staticmethod
    def character_error_rate(predicted: str, actual: str) -> float:
        """
        Calculate Character Error Rate (CER).

        Args:
            predicted: Predicted text
            actual: Actual/ground truth text

        Returns:
            CER score (0.0+, lower is better)
        """
        distance = PersianTextMetrics.edit_distance(predicted, actual)

        if not actual:
            return float('inf') if predicted else 0.0

        return distance / len(actual)

    @staticmethod
    def bleu_score(predicted: str, actual: str, n: int = 4) -> float:
        """
        Calculate simplified BLEU score (unigram to n-gram).

        Args:
            predicted: Predicted text
            actual: Actual/ground truth text
            n: Maximum n-gram size

        Returns:
            BLEU score (0.0-1.0)
        """
        predicted_words = predicted.split()
        actual_words = actual.split()

        if not predicted_words or not actual_words:
            return 0.0

        scores = []

        for i in range(1, n + 1):
            # Get n-grams
            predicted_ngrams = [tuple(predicted_words[j:j+i])
                               for j in range(len(predicted_words) - i + 1)]
            actual_ngrams = [tuple(actual_words[j:j+i])
                            for j in range(len(actual_words) - i + 1)]

            if not predicted_ngrams or not actual_ngrams:
                continue

            # Count matches
            matches = 0
            for ngram in predicted_ngrams:
                if ngram in actual_ngrams:
                    matches += 1

            precision = matches / len(predicted_ngrams) if predicted_ngrams else 0
            scores.append(precision)

        if not scores:
            return 0.0

        # Geometric mean
        product = 1.0
        for score in scores:
            product *= (score if score > 0 else 1e-10)

        return product ** (1 / len(scores))

    @staticmethod
    def confusion_matrix(predicted: List, actual: List, labels: Optional[List] = None) -> dict:
        """
        Calculate confusion matrix.

        Args:
            predicted: List of predicted labels
            actual: List of actual labels
            labels: List of all possible labels (optional)

        Returns:
            Dictionary with confusion matrix data
        """
        if len(predicted) != len(actual):
            raise ValueError("Predicted and actual lists must have the same length")

        if labels is None:
            labels = sorted(set(predicted) | set(actual))

        # Initialize matrix
        matrix = {label: {l: 0 for l in labels} for label in labels}

        # Fill matrix
        for p, a in zip(predicted, actual):
            if p in labels and a in labels:
                matrix[a][p] += 1

        return {
            'matrix': matrix,
            'labels': labels,
            'total': len(predicted)
        }

    @staticmethod
    def classification_report(predicted: List, actual: List, labels: Optional[List] = None) -> dict:
        """
        Generate classification report with precision, recall, F1 for each label.

        Args:
            predicted: List of predicted labels
            actual: List of actual labels
            labels: List of all possible labels (optional)

        Returns:
            Dictionary with metrics for each label
        """
        if len(predicted) != len(actual):
            raise ValueError("Predicted and actual lists must have the same length")

        if labels is None:
            labels = sorted(set(predicted) | set(actual))

        report = {}

        for label in labels:
            # Get sets for this label
            pred_set = set(i for i, p in enumerate(predicted) if p == label)
            actual_set = set(i for i, a in enumerate(actual) if a == label)

            p = PersianTextMetrics.precision(pred_set, actual_set)
            r = PersianTextMetrics.recall(pred_set, actual_set)
            f1 = PersianTextMetrics.f1_score(pred_set, actual_set)

            report[label] = {
                'precision': round(p, 4),
                'recall': round(r, 4),
                'f1_score': round(f1, 4),
                'support': len(actual_set)
            }

        # Add overall metrics
        all_pred = set(range(len(predicted)))
        all_actual = set(range(len(actual)))

        report['overall'] = {
            'accuracy': round(PersianTextMetrics.accuracy(predicted, actual), 4),
            'total': len(actual)
        }

        return report
