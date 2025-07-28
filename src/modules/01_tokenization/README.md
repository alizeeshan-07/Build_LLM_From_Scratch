# Module 1: Tokenization

## 🎯 Learning Objectives

By completing this module, you will understand:
- How to convert raw text into numerical tokens
- Different tokenization strategies (word-level, regex-based)
- Vocabulary building from text corpora
- Handling unknown words and special tokens
- Evaluating tokenization quality

## 🔑 Key Concepts

### **Tokenization**
The process of breaking down text into smaller units (tokens) that can be processed by machine learning models.

### **Vocabulary**
A mapping between tokens (strings) and unique integer IDs. Forms the foundation for converting text to numbers.

### **Unknown Token Handling**
Strategy for dealing with words not seen during vocabulary building.

## 📁 Files in This Module

### **Core Implementation**
- `simple_tokenizer.py` - Main TextTokenizer class with encode/decode methods
- `build_vocabulary.py` - Tools for downloading text and building vocabularies

### **Testing & Examples**
- `test.py` - Simple test script to verify tokenizer functionality
- `utils.py` - Analysis and visualization tools for tokenization

## 🚀 Quick Start

```python
# Build vocabulary from sample text
from build_vocabulary import create_full_vocabulary
vocab = create_full_vocabulary()

# Create tokenizer
from simple_tokenizer import TextTokenizer
tokenizer = TextTokenizer(vocab)

# Tokenize text
text = "Hello, world!"
token_ids = tokenizer.encode(text)
decoded_text = tokenizer.decode(token_ids)

print(f"Original: {text}")
print(f"Token IDs: {token_ids}")
print(f"Decoded: {decoded_text}")