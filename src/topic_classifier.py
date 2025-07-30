# topic_classifier.py
from transformers import pipeline
from functools import lru_cache
import numpy as np  # For float conversion


class TopicClassifier:
    """
    Performs zero-shot topic classification on text using a pre-trained NLI model.
    """

    def __init__(self, model_name: str = "facebook/bart-large-mnli"):
        """
        Initializes the TopicClassifier with a specified pre-trained model.
        Args:
            model_name (str): The name of the Hugging Face model for zero-shot classification.
                              "facebook/bart-large-mnli" is a common choice.
        """
        try:
            self.classifier = pipeline("zero-shot-classification", model=model_name)
            print(f"TopicClassifier using model: {model_name}")
        except Exception as e:
            print(f"Error loading TopicClassifier model '{model_name}': {e}")
            print("Please ensure you have 'transformers' and 'torch' installed correctly and internet access.")
            self.classifier = None  # Set to None to indicate failure

    @lru_cache(maxsize=1000)  # Cache to avoid re-running for same text/labels combinations
    def classify_zero_shot(self, text: str, candidate_labels: list[str], confidence_threshold: float = 0.6) -> list[
        dict]:
        """
        Classifies text into given candidate labels using zero-shot learning.

        Args:
            text (str): The text to classify.
            candidate_labels (list[str]): A list of possible labels for the text.
            confidence_threshold (float): Minimum confidence score to include a label.

        Returns:
            list[dict]: A list of dictionaries, each with 'label' and 'score' for classified topics.
        """
        if not text or not candidate_labels or self.classifier is None:
            return []

        # Zero-shot classification handles multiple labels and scores them
        try:
            result = self.classifier(text, candidate_labels, multi_label=True)
            # result example: {'sequence': '...', 'labels': ['music', 'art'], 'scores': [0.9, 0.1]}

            classified_topics = []
            for label, score in zip(result['labels'], result['scores']):
                if score > confidence_threshold:
                    classified_topics.append({"label": label, "score": float(score)})
            return sorted(classified_topics, key=lambda x: x['score'], reverse=True)  # Sort by score
        except Exception as e:
            print(f"Error during zero-shot classification: {e}")
            return []