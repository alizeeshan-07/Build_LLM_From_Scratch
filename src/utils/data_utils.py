"""
Data processing utilities for loading and preprocessing text data.
"""

import os
import re
from typing import List, Dict, Tuple
from pathlib import Path

def load_text_data(file_path: str) -> str:
    """
    Load text data from a file.
    
    Args:
        file_path: Path to the text file
        
    Returns:
        String containing the file contents
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as f:
            return f.read()

def preprocess_text(text: str, lowercase: bool = True, remove_punctuation: bool = False) -> str:
    """
    Basic text preprocessing.
    
    Args:
        text: Input text to preprocess
        lowercase: Whether to convert to lowercase
        remove_punctuation: Whether to remove punctuation
        
    Returns:
        Preprocessed text string
    """
    if lowercase:
        text = text.lower()
    
    if remove_punctuation:
        text = re.sub(r'[^\w\s]', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def create_vocab(texts: List[str], min_freq: int = 2) -> Dict[str, int]:
    """
    Create vocabulary from list of texts.
    
    Args:
        texts: List of text strings
        min_freq: Minimum frequency for word inclusion
        
    Returns:
        Dictionary mapping words to indices
    """
    word_counts = {}
    
    for text in texts:
        words = text.split()
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
    
    # Filter by minimum frequency
    vocab = {'<pad>': 0, '<unk>': 1}
    idx = 2
    
    for word, count in word_counts.items():
        if count >= min_freq:
            vocab[word] = idx
            idx += 1
    
    return vocab