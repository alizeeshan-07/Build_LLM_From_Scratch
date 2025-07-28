# Module 1: Tokenization

## 🎯 Overview

Tokenization is the foundational step in natural language processing where we convert raw text into numerical tokens that machine learning models can understand. This module implements a regex-based tokenizer that splits text using punctuation and whitespace patterns.

## 🧠 Core Concepts

### **What is Tokenization?**
Breaking down text into smaller units called "tokens" that computers can process:

```
Input:  "Hello, world!"
Tokens: ["Hello", ",", "world", "!"]  
IDs:    [45, 2, 123, 8]
```

### **Vocabulary**
A dictionary mapping tokens to unique integer IDs:

```python
vocab = {
    "hello": 0,
    "world": 1,
    ",": 2,
    "<|unk|>": 3,        # Unknown token
    "<|endoftext|>": 4   # End marker
}
```

### **Regex Pattern**
Our tokenizer uses `([,.:;?_!"()\']|--|\\s)` to split text:
- Captures punctuation as separate tokens
- Handles double dashes and whitespace
- Preserves important text structure

## 📁 File Structure

```
src/modules/01_tokenization/
├── simple_tokenizer.py     # Core TextTokenizer class
├── build_vocabulary.py     # Vocabulary creation
├── test.py                 # Testing script  
├── utils.py                # Analysis tools
└── README.md              # This guide
```

## 📄 Core Files Explained

### **`simple_tokenizer.py` - Main Implementation**

Contains the `TextTokenizer` class with two key methods:

#### **`encode(text)` - Text to Numbers**
1. **Split text** using regex pattern
2. **Clean tokens** (remove empty, strip whitespace)  
3. **Handle unknowns** (replace with `<|unk|>`)
4. **Convert to IDs** using vocabulary

```python
tokenizer = TextTokenizer(vocab)
ids = tokenizer.encode("Hello, world!")  # → [45, 2, 123, 8]
```

#### **`decode(ids)` - Numbers to Text**
1. **Map IDs to tokens** using reverse vocabulary
2. **Join with spaces**
3. **Fix punctuation spacing** with regex

```python
text = tokenizer.decode([45, 2, 123, 8])  # → "Hello, world!"
```

### **`build_vocabulary.py` - Vocabulary Creation**

Creates vocabularies from real text data:

#### **Main Pipeline: `create_full_vocabulary()`**
1. **Download text**: Gets "The Verdict" sample text
2. **Load and analyze**: Reads file, shows statistics
3. **Preprocess**: Splits text using same regex as tokenizer
4. **Build vocab**: Creates sorted token-to-ID mapping

```python
vocab = create_full_vocabulary()  # Downloads text and builds vocab
```

#### **Key Functions:**
- `download_sample_text()`: Downloads sample text file
- `preprocess_text()`: Splits text into tokens
- `build_vocabulary()`: Creates final vocab with special tokens

**Special tokens added:**
```python
all_tokens.extend(["<|endoftext|>", "<|unk|>"])
```

## 🧪 How to Test

### **Run Complete Test Suite**
```bash
cd src/modules/01_tokenization/
python test.py
```

**What happens:**
1. Downloads sample text (~20K characters)
2. Builds vocabulary (~1,159 tokens)  
3. Creates tokenizer
4. Tests encoding/decoding on sample texts
5. Validates round-trip consistency
6. Shows vocabulary analysis

### **Manual Testing**
```python
from build_vocabulary import create_full_vocabulary
from simple_tokenizer import TextTokenizer

# Build vocabulary
vocab = create_full_vocabulary()

# Create tokenizer  
tokenizer = TextTokenizer(vocab)

# Test
text = "Hello, world!"
ids = tokenizer.encode(text)
decoded = tokenizer.decode(ids)

print(f"Original: {text}")
print(f"Token IDs: {ids}")  
print(f"Decoded: {decoded}")
print(f"Perfect match: {text == decoded}")
```

## ✅ Expected Results

**Successful test shows:**
```
Building vocabulary...
Vocabulary size: 1159
Creating tokenizer...

Test 1:
Original: Hello, world!
Token IDs: [789, 2, 456]
Decoded: Hello, world!
Perfect match: True

✅ All tests completed successfully!
```

## 🎯 Learning Outcomes

After this module, you should understand:
- ✅ How text becomes numerical tokens
- ✅ Vocabulary creation and management
- ✅ Handling unknown words with special tokens
- ✅ Round-trip encoding/decoding validation

## 🚀 Next Steps

1. **Test successfully**: Run `python test.py` without errors
2. **Experiment**: Try different texts and analyze results  
3. **Ready for Module 2**: Understanding embeddings

The foundation of your LLM is ready! 🏗️