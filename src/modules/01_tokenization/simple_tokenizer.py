## 🔤 **`simple_tokenizer.py`**

"""
Simple tokenizer implementation using regex-based splitting.

This module implements a basic tokenizer that splits text using regular expressions
and handles unknown tokens with a fallback strategy.
"""

import re
from typing import Dict, List


class TextTokenizer:
    """
    A simple regex-based tokenizer for text preprocessing.
    
    This tokenizer splits text using punctuation and whitespace patterns,
    maps tokens to integers, and handles out-of-vocabulary words.
    
    Args:
        vocab: Dictionary mapping tokens (str) to IDs (int)
        
    Example:
        >>> vocab = {"hello": 0, "world": 1, ",": 2, "!": 3, "unknown": 4}
        >>> tokenizer = TextTokenizer(vocab)
        >>> ids = tokenizer.encode("hello, world!")
        >>> text = tokenizer.decode(ids)
        >>> print(f"IDs: {ids}, Text: {text}")
    """
    
    def __init__(self, vocab: Dict[str, int]):
        """Initialize tokenizer with vocabulary."""
        self.str_to_int = vocab
        self.int_to_str = {i: s for s, i in vocab.items()}

    def encode(self, text: str) -> List[int]:
        """
        Encode text into token IDs.
        
        Args:
            text: Input text to tokenize
            
        Returns:
            List of token IDs
        """
        # Split using regex pattern for punctuation and whitespace
        preprocessed = re.split(r'([,.:;?_!"()\']|--|\\s)', text)
        
        # Remove empty strings and strip whitespace
        preprocessed = [
            item.strip() for item in preprocessed if item.strip()
        ]
        
        # Replace unknown tokens
        preprocessed = [
            item if item in self.str_to_int else "<|unk|>"
            for item in preprocessed
        ]

        # Convert to IDs
        ids = [self.str_to_int[s] for s in preprocessed]
        return ids

    def decode(self, ids: List[int]) -> str:
        """
        Decode token IDs back to text.
        
        Args:
            ids: List of token IDs
            
        Returns:
            Decoded text string
        """
        # Convert IDs back to tokens
        text = " ".join([self.int_to_str[i] for i in ids])
        
        # Fix spacing around punctuation
        text = re.sub(r"\s+([,.:;?!\"()\\'])", r"\1", text)
        return text # type: ignore


if __name__ == "__main__":
    # Example usage with simple vocabulary
    sample_vocab = {
        "hello": 0, "world": 1, ",": 2, "!": 3, 
        "this": 4, "is": 5, "a": 6, "test": 7, "unknown": 8
    }
    
    tokenizer = TextTokenizer(sample_vocab)
    
    # Test with sample text
    test_texts = [
        "hello, world!",
        "this is a test",
        "unknown words here"
    ]
    
    for text in test_texts:
        ids = tokenizer.encode(text)
        decoded = tokenizer.decode(ids)
        
        print(f"Original: {text}")
        print(f"Token IDs: {ids}")
        print(f"Decoded: {decoded}")
        print(f"Match: {text == decoded}")
        print("-" * 40)