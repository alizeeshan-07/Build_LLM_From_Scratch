"""
Vocabulary building utilities for tokenization.

This module downloads sample text and creates vocabularies for tokenizer training.
Based on "The Verdict" text from the LLMs-from-scratch repository.
"""

import re
import urllib.request
from typing import Dict, List
from pathlib import Path


def download_sample_text(save_path: str = "the-verdict.txt") -> str:
    """
    Download sample text file for vocabulary building.
    
    Args:
        save_path: Path to save the downloaded file
        
    Returns:
        Path to the downloaded file
    """
    url = ("https://raw.githubusercontent.com/rasbt/"
           "LLMs-from-scratch/main/ch02/01_main-chapter-code/"
           "the-verdict.txt")
    
    print(f"Downloading text from: {url}")
    urllib.request.urlretrieve(url, save_path)
    print(f"Text saved to: {save_path}")
    
    return save_path


def load_and_analyze_text(file_path: str) -> str:
    """
    Load text file and display basic statistics.
    
    Args:
        file_path: Path to the text file
        
    Returns:
        Raw text content
    """
    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()
    
    print(f"Total number of characters: {len(raw_text)}")
    print(f"First 99 characters:\n{raw_text[:99]}")
    
    return raw_text


def preprocess_text(raw_text: str) -> List[str]:
    """
    Preprocess text using regex splitting.
    
    Args:
        raw_text: Raw input text
        
    Returns:
        List of preprocessed tokens
    """
    # Split using regex pattern for punctuation and whitespace
    preprocessed = re.split(r'([,.:;?_!"()\']|--|\\s)', raw_text)
    
    # Remove empty strings and strip whitespace
    preprocessed = [item.strip() for item in preprocessed if item.strip()]
    
    print(f"Number of tokens after preprocessing: {len(preprocessed)}")
    
    return preprocessed


def build_vocabulary(tokens: List[str]) -> Dict[str, int]:
    """
    Build vocabulary dictionary from tokens.
    
    Args:
        tokens: List of preprocessed tokens
        
    Returns:
        Dictionary mapping tokens to integer IDs
    """
    # Get unique tokens and sort them
    all_words = sorted(set(tokens))
    vocab_size = len(all_words)
    
    print(f"Vocabulary size: {vocab_size}")
    print(f"First 10 tokens: {all_words[:10]}")
    print(f"Last 10 tokens: {all_words[-10:]}")
    
    # Create vocabulary mapping
    vocab = {token: integer for integer, token in enumerate(all_words)}
    
    return vocab


def create_full_vocabulary(download_fresh: bool = True) -> Dict[str, int]:
    """
    Complete pipeline to create vocabulary from sample text.
    
    Args:
        download_fresh: Whether to download text again or use existing file
        
    Returns:
        Complete vocabulary dictionary
    """
    file_path = "the-verdict.txt"
    
    # Download text if needed
    if download_fresh or not Path(file_path).exists():
        download_sample_text(file_path)
    
    # Load and analyze text
    raw_text = load_and_analyze_text(file_path)
    
    # Preprocess text
    tokens = preprocess_text(raw_text)
    
    # Build vocabulary
    vocab = build_vocabulary(tokens)
    
    return vocab


def save_vocabulary(vocab: Dict[str, int], save_path: str = "vocabulary.txt") -> None:
    """
    Save vocabulary to file for later use.
    
    Args:
        vocab: Vocabulary dictionary
        save_path: Path to save vocabulary file
    """
    with open(save_path, "w", encoding="utf-8") as f:
        for token, idx in vocab.items():
            f.write(f"{token}\t{idx}\n")
    
    print(f"Vocabulary saved to: {save_path}")


def load_vocabulary(file_path: str = "vocabulary.txt") -> Dict[str, int]:
    """
    Load vocabulary from file.
    
    Args:
        file_path: Path to vocabulary file
        
    Returns:
        Vocabulary dictionary
    """
    vocab = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            token, idx = line.strip().split("\t")
            vocab[token] = int(idx)
    
    print(f"Loaded vocabulary with {len(vocab)} tokens from: {file_path}")
    return vocab


if __name__ == "__main__":
    # Create vocabulary from scratch
    print("=== Building Vocabulary ===")
    vocab = create_full_vocabulary(download_fresh=True)
    
    # Save vocabulary
    save_vocabulary(vocab, "vocabulary.txt")
    
    # Show some examples
    print(f"\n=== Vocabulary Examples ===")
    print(f"Total vocabulary size: {len(vocab)}")
    
    # Show some token mappings
    sample_tokens = list(vocab.items())[:10]
    for token, idx in sample_tokens:
        print(f"'{token}' -> {idx}")
    
    print(f"\n=== Special Characters ===")
    special_chars = [token for token in vocab.keys() if not token.isalnum()][:10]
    for token in special_chars:
        print(f"'{token}' -> {vocab[token]}")