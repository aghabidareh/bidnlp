"""
HMM-Based Persian POS Tagger

Implements a Hidden Markov Model-based POS tagger for Persian.
"""

from typing import List, Tuple, Dict, Optional
from collections import defaultdict
import math
from .base_tagger import BasePOSTagger
from .pos_tags import PersianPOSTag


class HMMPOSTagger(BasePOSTagger):
    """HMM-based POS tagger for Persian."""

    def __init__(self, normalize: bool = True, smoothing: float = 1e-10):
        """
        Initialize the HMM POS tagger.

        Args:
            normalize: Whether to normalize text before tagging
            smoothing: Smoothing factor for unknown words (Laplace smoothing)
        """
        super().__init__(normalize=normalize)
        self.smoothing = smoothing

        # Model parameters
        self.transition_probs: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        self.emission_probs: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        self.tag_counts: Dict[str, int] = defaultdict(int)
        self.word_counts: Dict[str, int] = defaultdict(int)
        self.vocabulary: set = set()
        self.tagset: set = set()

        # Special tags
        self.start_tag = '<START>'
        self.end_tag = '<END>'

    def train(self, tagged_sentences: List[List[Tuple[str, str]]]) -> None:
        """
        Train the HMM model on tagged sentences.

        Args:
            tagged_sentences: List of sentences, each is a list of (word, tag) tuples
        """
        # Count transitions and emissions
        transition_counts: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        emission_counts: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        tag_counts: Dict[str, int] = defaultdict(int)

        for sentence in tagged_sentences:
            if not sentence:
                continue

            # Add start transition
            prev_tag = self.start_tag
            tag_counts[self.start_tag] += 1

            for word, tag in sentence:
                # Count emission
                emission_counts[tag][word] += 1
                self.vocabulary.add(word)
                self.tagset.add(tag)

                # Count transition
                transition_counts[prev_tag][tag] += 1

                # Update tag count
                tag_counts[tag] += 1

                prev_tag = tag

            # Add end transition
            transition_counts[prev_tag][self.end_tag] += 1
            tag_counts[self.end_tag] += 1

        # Calculate probabilities
        self._calculate_transition_probs(transition_counts, tag_counts)
        self._calculate_emission_probs(emission_counts, tag_counts)
        self.tag_counts = tag_counts

        self._is_trained = True

    def _calculate_transition_probs(self, transition_counts: Dict[str, Dict[str, int]],
                                    tag_counts: Dict[str, int]) -> None:
        """Calculate transition probabilities."""
        for prev_tag, next_tags in transition_counts.items():
            total = tag_counts[prev_tag]
            for next_tag, count in next_tags.items():
                # Add-one smoothing
                self.transition_probs[prev_tag][next_tag] = (
                    (count + self.smoothing) / (total + self.smoothing * len(self.tagset))
                )

    def _calculate_emission_probs(self, emission_counts: Dict[str, Dict[str, int]],
                                  tag_counts: Dict[str, int]) -> None:
        """Calculate emission probabilities."""
        for tag, words in emission_counts.items():
            total = tag_counts[tag]
            for word, count in words.items():
                self.emission_probs[tag][word] = count / total

    def tag(self, text: str) -> List[Tuple[str, str]]:
        """
        Tag a text using Viterbi algorithm.

        Args:
            text: Input text

        Returns:
            List of (word, tag) tuples
        """
        if not self._is_trained:
            raise ValueError("Tagger must be trained before tagging")

        if not text:
            return []

        # Preprocess
        processed_text = self.preprocess(text)

        # Tokenize
        words = self.tokenize(processed_text)

        if not words:
            return []

        # Use Viterbi algorithm
        tags = self._viterbi(words)

        return list(zip(words, tags))

    def _viterbi(self, words: List[str]) -> List[str]:
        """
        Viterbi algorithm for finding most likely tag sequence.

        Args:
            words: List of words

        Returns:
            List of tags
        """
        if not words:
            return []

        # Initialize
        n_words = len(words)
        taglist = list(self.tagset) if self.tagset else [PersianPOSTag.N.value]

        # Viterbi matrix: viterbi[time][tag] = (probability, backpointer)
        viterbi: List[Dict[str, Tuple[float, Optional[str]]]] = [
            {} for _ in range(n_words)
        ]

        # Initialize first word
        word = words[0]
        for tag in taglist:
            trans_prob = self.transition_probs[self.start_tag].get(tag, self.smoothing)
            emit_prob = self._get_emission_prob(tag, word)
            viterbi[0][tag] = (math.log(trans_prob) + math.log(emit_prob), None)

        # Forward pass
        for t in range(1, n_words):
            word = words[t]
            for tag in taglist:
                max_prob = float('-inf')
                best_prev_tag = None

                for prev_tag in taglist:
                    prev_prob = viterbi[t - 1][prev_tag][0]
                    trans_prob = self.transition_probs[prev_tag].get(tag, self.smoothing)
                    prob = prev_prob + math.log(trans_prob)

                    if prob > max_prob:
                        max_prob = prob
                        best_prev_tag = prev_tag

                emit_prob = self._get_emission_prob(tag, word)
                viterbi[t][tag] = (max_prob + math.log(emit_prob), best_prev_tag)

        # Backward pass - find best path
        # Find best final tag
        max_prob = float('-inf')
        best_final_tag = taglist[0]
        for tag in taglist:
            prob = viterbi[n_words - 1][tag][0]
            if prob > max_prob:
                max_prob = prob
                best_final_tag = tag

        # Reconstruct path
        tags = [best_final_tag]
        for t in range(n_words - 1, 0, -1):
            prev_tag = viterbi[t][tags[0]][1]
            if prev_tag is None:
                prev_tag = taglist[0]
            tags.insert(0, prev_tag)

        return tags

    def _get_emission_prob(self, tag: str, word: str) -> float:
        """
        Get emission probability for word given tag.

        Args:
            tag: POS tag
            word: Word

        Returns:
            Emission probability
        """
        if word in self.emission_probs[tag]:
            return self.emission_probs[tag][word]
        else:
            # Unknown word - use smoothing
            # Simple smoothing: uniform distribution over all tags
            return self.smoothing

    def get_transition_prob(self, prev_tag: str, tag: str) -> float:
        """
        Get transition probability.

        Args:
            prev_tag: Previous tag
            tag: Current tag

        Returns:
            Transition probability
        """
        return self.transition_probs[prev_tag].get(tag, self.smoothing)

    def get_emission_prob(self, tag: str, word: str) -> float:
        """
        Get emission probability.

        Args:
            tag: POS tag
            word: Word

        Returns:
            Emission probability
        """
        return self._get_emission_prob(tag, word)

    def get_most_likely_tag(self, word: str) -> str:
        """
        Get most likely tag for a word based on emission probabilities.

        Args:
            word: Input word

        Returns:
            Most likely POS tag
        """
        if not self._is_trained:
            raise ValueError("Tagger must be trained before prediction")

        max_prob = 0.0
        best_tag = PersianPOSTag.N.value

        for tag in self.tagset:
            prob = self._get_emission_prob(tag, word)
            if prob > max_prob:
                max_prob = prob
                best_tag = tag

        return best_tag

    def save_model(self) -> Dict:
        """
        Save model parameters.

        Returns:
            Dictionary containing model parameters
        """
        return {
            'transition_probs': dict(self.transition_probs),
            'emission_probs': dict(self.emission_probs),
            'tag_counts': dict(self.tag_counts),
            'vocabulary': list(self.vocabulary),
            'tagset': list(self.tagset),
            'smoothing': self.smoothing,
            'is_trained': self._is_trained
        }

    def load_model(self, model_data: Dict) -> None:
        """
        Load model parameters.

        Args:
            model_data: Dictionary containing model parameters
        """
        self.transition_probs = defaultdict(lambda: defaultdict(float), model_data['transition_probs'])
        self.emission_probs = defaultdict(lambda: defaultdict(float), model_data['emission_probs'])
        self.tag_counts = defaultdict(int, model_data['tag_counts'])
        self.vocabulary = set(model_data['vocabulary'])
        self.tagset = set(model_data['tagset'])
        self.smoothing = model_data.get('smoothing', self.smoothing)
        self._is_trained = model_data.get('is_trained', False)
