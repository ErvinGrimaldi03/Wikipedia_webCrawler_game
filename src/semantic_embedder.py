# semantic_embedder.py
from transformers import AutoModel, AutoTokenizer
import torch
import numpy as np


class SemanticEmbedder:
    """
    Generates semantic embeddings for text using a pre-trained Sentence Transformer model.
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initializes the SemanticEmbedder with a specified pre-trained model.
        Args:
            model_name (str): The name of the Hugging Face Sentence Transformer model to use.
                              "all-MiniLM-L6-v2" is a good balance of size/performance.
        """
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModel.from_pretrained(model_name)
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model.to(self.device)
            print(f"SemanticEmbedder using model: {model_name} on device: {self.device}")
        except Exception as e:
            print(f"Error loading SemanticEmbedder model '{model_name}': {e}")
            print("Please ensure you have 'transformers' and 'torch' installed correctly and internet access.")
            # Fallback to a dummy model or raise an error depending on desired behavior
            self.tokenizer = None
            self.model = None
            self.device = "cpu"

    def _mean_pooling(self, model_output: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
        """
        Performs mean pooling on token embeddings to get a single vector for the sentence.
        """
        if self.model is None:  # Handle case where model failed to load
            return torch.zeros(1, 384)  # Return a dummy tensor, assuming MiniLM's size

        token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        return sum_embeddings / sum_mask

    def get_embedding(self, text: str) -> list[float]:
        """
        Generates a semantic embedding for a given text.

        Args:
            text (str): The input text to embed.

        Returns:
            list[float]: A list of floats representing the dense semantic embedding.
                         Returns a zero vector if text is empty or model not loaded.
        """
        if not text or self.model is None:
            # Return a zero vector of the model's expected dimension (e.g., 384 for MiniLM)
            return np.zeros(self.model.config.hidden_size if self.model else 384).tolist()

            # Tokenize the text
        encoded_input = self.tokenizer(
            text,
            padding=True,
            truncation=True,
            max_length=512,  # Max length for most transformer models
            return_tensors='pt'
        ).to(self.device)

        # Compute embeddings
        with torch.no_grad():  # Disable gradient calculation for inference
            model_output = self.model(**encoded_input)

        # Perform pooling (mean pooling in this case)
        sentence_embedding = self._mean_pooling(model_output, encoded_input['attention_mask'])

        # Normalize embeddings to unit length (important for cosine similarity)
        sentence_embedding = torch.nn.functional.normalize(sentence_embedding, p=2, dim=1)

        return sentence_embedding.cpu().numpy()[0].tolist()  # Convert to list for JSON serialization