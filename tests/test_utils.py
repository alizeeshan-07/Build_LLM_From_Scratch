"""
Tests for utility functions.
"""

import pytest
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.data_utils import preprocess_text, create_vocab

def test_preprocess_text():
    """Test text preprocessing function."""
    text = "Hello, World! This is a TEST."
    
    # Test lowercase
    result = preprocess_text(text, lowercase=True)
    assert "hello, world!" in result
    
    # Test punctuation removal
    result = preprocess_text(text, remove_punctuation=True)
    assert "," not in result
    assert "!" not in result

def test_create_vocab():
    """Test vocabulary creation."""
    texts = ["hello world", "world peace", "hello there"]
    vocab = create_vocab(texts, min_freq=1)
    
    assert "<pad>" in vocab
    assert "<unk>" in vocab
    assert "hello" in vocab
    assert "world" in vocab
    assert vocab["<pad>"] == 0
    assert vocab["<unk>"] == 1