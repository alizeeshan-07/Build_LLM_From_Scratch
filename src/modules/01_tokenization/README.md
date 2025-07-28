# Module 1: Tokenization

## 🎯 Overview

Tokenization is the foundational step in natural language processing where we convert raw text into numerical tokens that machine learning models can understand. This module implements a regex-based tokenizer that splits text using punctuation and whitespace patterns, creating a vocabulary mapping between tokens and unique integer IDs.

## 🧠 Core Concepts Explained

### **What is Tokenization?**

Tokenization is the process of breaking down text into smaller, meaningful units called "tokens." Think of it as converting sentences into a list of words and punctuation marks that a computer can work with.

**Example:**
```
Input:  "Hello, world!"
Tokens: ["Hello", ",", "world", "!"]
IDs:    [45, 2, 123, 8]
```

### **Why Do We Need Tokenization?**

1. **Neural networks work with numbers**: Models can't process raw text directly
2. **Consistent input format**: All text gets converted to the same numerical format
3. **Vocabulary management**: We can control which words the model knows
4. **Efficiency**: Numbers are faster to process than strings

### **Vocabulary Creation**

A vocabulary is a dictionary that maps each unique token to a unique integer ID:

```python
vocab = {
    "hello": 0,
    "world": 1, 
    ",": 2,
    "!": 3,
    "<|unk|>": 4,        # Unknown token
    "<|endoftext|>": 5   # End of text marker
}
```

**Key Features:**
- **Bidirectional mapping**: token ↔ ID conversion
- **Special tokens**: Handle unknown words and text boundaries
- **Sorted tokens**: Consistent vocabulary across runs

### **Handling Unknown Words**

When the tokenizer encounters a word not in its vocabulary, it uses the special `<|unk|>` token:

```python
# If "python" is not in vocabulary:
"I love python" → ["I", "love", "<|unk|>"] → [12, 34, 4]
```

### **Regex-Based Splitting**

Our tokenizer uses regular expressions to split text intelligently:

```python
# Pattern: r'([,.:;?_!"()\']|--|\\s)'
"Hello, world!" → ["Hello", ",", "world", "!"]
"It's great--really?" → ["It", "'", "s", "great", "--", "really", "?"]
```

**What the regex does:**
- `[,.:;?_!"()\']`: Captures punctuation marks as separate tokens
- `--`: Captures double dashes (common in literature)
- `\\s`: Captures whitespace characters

## 📁 File Structure & Purpose

```
src/modules/01_tokenization/
├── __init__.py              # Module exports and imports
├── README.md               # This comprehensive guide
├── simple_tokenizer.py     # Core TextTokenizer implementation
├── build_vocabulary.py     # Vocabulary creation from text
├── test.py                 # Testing and demonstration script
└── utils.py                # Analysis and visualization tools
```

## 📄 Detailed File Explanations

### **`simple_tokenizer.py` - Core Implementation**

**Purpose**: Contains the main `TextTokenizer` class that performs encoding and decoding.

**Key Components:**

#### **`TextTokenizer` Class**

```python
class TextTokenizer:
    def __init__(self, vocab: Dict[str, int])
    def encode(self, text: str) → List[int]
    def decode(self, ids: List[int]) → str
```

**What happens in `encode()`:**
1. **Regex splitting**: Breaks text using punctuation patterns
2. **Cleanup**: Removes empty strings and strips whitespace
3. **Unknown handling**: Replaces unfamiliar tokens with `<|unk|>`
4. **ID conversion**: Maps tokens to integer IDs using vocabulary

**What happens in `decode()`:**
1. **ID to token**: Converts integer IDs back to token strings
2. **Rejoin**: Combines tokens with spaces
3. **Spacing fix**: Removes extra spaces around punctuation using regex

**Example Usage:**
```python
vocab = {"hello": 0, "world": 1, ",": 2, "<|unk|>": 3}
tokenizer = TextTokenizer(vocab)

# Encoding
ids = tokenizer.encode("hello, world")  # → [0, 2, 1]

# Decoding  
text = tokenizer.decode([0, 2, 1])      # → "hello, world"
```

### **`build_vocabulary.py` - Vocabulary Creation**

**Purpose**: Downloads sample text and builds comprehensive vocabularies for training tokenizers.

**Key Functions:**

#### **`download_sample_text()`**
- Downloads "The Verdict" text from the LLMs-from-scratch repository
- Saves locally for vocabulary building
- Uses urllib for reliable downloading

#### **`load_and_analyze_text()`**
- Loads text file with UTF-8 encoding
- Displays character count and preview
- Returns raw text for processing

#### **`preprocess_text()`**
- Applies same regex splitting as tokenizer
- Removes empty tokens and strips whitespace
- Returns list of clean tokens

#### **`build_vocabulary()`**
- Creates sorted list of unique tokens
- Adds special tokens: `<|endoftext|>`, `<|unk|>`
- Maps tokens to consecutive integer IDs
- Returns complete vocabulary dictionary

#### **`create_full_vocabulary()` - Main Pipeline**
The complete workflow:
```python
def create_full_vocabulary():
    # 1. Download text (if needed)
    download_sample_text("the-verdict.txt")
    
    # 2. Load and analyze
    raw_text = load_and_analyze_text("the-verdict.txt")
    
    # 3. Preprocess into tokens
    tokens = preprocess_text(raw_text)
    
    # 4. Build vocabulary mapping
    vocab = build_vocabulary(tokens)
    
    return vocab
```

### **`test.py` - Testing & Demonstration**

**Purpose**: Comprehensive testing suite that validates tokenizer functionality and demonstrates usage patterns.

**Test Functions:**

#### **`test_basic_functionality()`**
- Builds vocabulary from sample text
- Creates tokenizer instance
- Tests encoding/decoding on various texts
- Validates round-trip consistency (encode → decode = original)

#### **`test_vocabulary_analysis()`**
- Analyzes vocabulary statistics
- Shows token distribution and characteristics
- Demonstrates vocabulary utility functions

#### **`test_tokenization_analysis()`**
- Tests token frequency analysis
- Creates visualizations (if matplotlib available)
- Demonstrates tokenization patterns

**Test Cases Covered:**
```python
test_texts = [
    "Hello, world!",                    # Basic punctuation
    "This is a test sentence.",         # Standard sentence
    "What about punctuation? And numbers!", # Complex punctuation
    "Unknown words will be handled.",   # Unknown token handling
    "The quick brown fox jumps over the lazy dog." # Longer text
]
```

### **`utils.py` - Analysis Tools**

**Purpose**: Provides specialized utilities for analyzing and visualizing tokenization behavior.

**Key Functions:**

#### **`analyze_vocabulary(vocab)`**
Comprehensive vocabulary analysis:
- **Size metrics**: Total tokens, character counts
- **Token statistics**: Average length, longest/shortest tokens
- **Type analysis**: Alphabetic vs numeric vs punctuation breakdown
- **Sample display**: Shows example token mappings

#### **`plot_token_frequencies(tokens, top_n=20)`**
Visual frequency analysis:
- Creates bar chart of most frequent tokens
- Shows frequency counts and percentages
- Calculates coverage statistics
- Requires matplotlib for visualization

#### **`compare_tokenizations(text, tokenizer1, tokenizer2)`**
Side-by-side tokenizer comparison:
- Tokenizes same text with different tokenizers
- Compares token counts and compression ratios
- Identifies more efficient tokenization strategies
- Useful for evaluating different approaches

#### **`tokenization_statistics(tokenizer, texts)`**
Comprehensive statistical analysis:
- Calculates compression ratios
- Analyzes token length distributions
- Computes efficiency metrics
- Returns detailed statistics dictionary

### **`__init__.py` - Module Interface**

**Purpose**: Defines the public API of the tokenization module.

**Exports:**
```python
from .simple_tokenizer import TextTokenizer
from .build_vocabulary import create_full_vocabulary, build_vocabulary
from .utils import analyze_vocabulary, plot_token_frequencies, compare_tokenizations
```

This allows clean imports:
```python
from src.modules.tokenization import TextTokenizer, create_full_vocabulary
```

## 🧪 How to Test Everything

### **Quick Test - Run the Main Test Suite**

```bash
cd src/modules/01_tokenization/
python test.py
```

**What this does:**
1. **Downloads sample text** ("The Verdict" by Edith Wharton)
2. **Builds vocabulary** from ~20,000 characters of text
3. **Creates tokenizer** with ~700 unique tokens
4. **Tests encoding/decoding** on various text samples
5. **Validates consistency** (round-trip testing)
6. **Shows vocabulary analysis** and statistics
7. **Creates visualizations** (if matplotlib installed)

### **Individual Component Testing**

#### **Test Vocabulary Building**
```bash
cd src/modules/01_tokenization/
python build_vocabulary.py
```

**Expected Output:**
```
Downloading text from: https://raw.githubusercontent.com/rasbt/...
Text saved to: the-verdict.txt
Total number of characters: 20479
First 99 characters:
I HAD always thought Jack Gisburn rather a cheap soul...
Number of tokens after preprocessing: 4649
Vocabulary size: 1159
```

#### **Test Tokenizer Directly**
```python
# In Python REPL or separate script:
from build_vocabulary import create_full_vocabulary
from simple_tokenizer import TextTokenizer

# Build vocab
vocab = create_full_vocabulary(download_fresh=False)

# Create tokenizer
tokenizer = TextTokenizer(vocab)

# Test specific text
text = "Hello, world! This is amazing."
ids = tokenizer.encode(text)
decoded = tokenizer.decode(ids)

print(f"Original: {text}")
print(f"IDs: {ids}")
print(f"Decoded: {decoded}")
print(f"Match: {text == decoded}")
```

#### **Test Analysis Tools**
```python
from utils import analyze_vocabulary, plot_token_frequencies
from build_vocabulary import create_full_vocabulary

# Build vocabulary
vocab = create_full_vocabulary(download_fresh=False)

# Analyze vocabulary
analyze_vocabulary(vocab)

# Test with sample tokens
sample_tokens = ["the", "and", "is", "a", "to", "the", "and", "is"]
plot_token_frequencies(sample_tokens, top_n=5)
```

### **Expected Test Results**

**Successful test output should show:**

```
🧪 Starting Tokenization Tests
=== Building Vocabulary ===
Downloading text from: https://raw.githubusercontent.com/rasbt/...
Total number of characters: 20479
Vocabulary size: 1159

=== Testing Basic Functionality ===
Creating tokenizer...

=== Testing Tokenization ===
Test 1:
Original: Hello, world!
Token IDs: [789, 2, 456]
Decoded: Hello, world!
Perfect match: True

✅ All tests completed successfully!
```

## 🔍 Understanding the Output

### **Vocabulary Statistics**
- **Size**: ~1,159 tokens (varies with text)
- **Special tokens**: `<|endoftext|>`, `<|unk|>`
- **Token types**: Mix of words, punctuation, numbers

### **Token ID Mapping**
```python
# Example mappings (actual IDs will vary):
"Hello" → 789
","     → 2
"world" → 456
"<|unk|>" → 1158
```

### **Round-trip Testing**
The most important test: `original_text == decoded_text`
- **Pass**: Tokenization is working correctly
- **Fail**: There's an issue with encoding/decoding logic

## 🚨 Common Issues & Solutions

### **Issue 1: `KeyError: '<|unk|>'`**
**Cause**: Unknown token not in vocabulary
**Solution**: Ensure `build_vocabulary()` adds special tokens:
```python
all_tokens.extend(["<|endoftext|>", "<|unk|>"])
```

### **Issue 2: `ModuleNotFoundError`**
**Cause**: Missing imports or wrong directory
**Solution**: Run from correct directory and check imports:
```bash
cd src/modules/01_tokenization/
python test.py
```

### **Issue 3: Download Fails**
**Cause**: Network issues or URL changes
**Solution**: Check internet connection or manually download text file

### **Issue 4: Matplotlib Errors**
**Cause**: Visualization library not installed
**Solution**: Install matplotlib or skip visualization:
```bash
pip install matplotlib
```

## 🎯 Learning Outcomes

After completing this module, you should understand:

✅ **Tokenization fundamentals**: How text becomes numbers
✅ **Vocabulary creation**: Building token-to-ID mappings
✅ **Regex patterns**: How text splitting works
✅ **Unknown token handling**: Dealing with out-of-vocabulary words
✅ **Round-trip consistency**: Ensuring reversible transformations
✅ **Analysis techniques**: Evaluating tokenization quality

## 🚀 Next Steps

1. **Master this module**: Run all tests successfully
2. **Experiment**: Try different texts and analyze patterns
3. **Optimize**: Consider different regex patterns
4. **Extend**: Think about subword tokenization (BPE)
5. **Move on**: Ready for Module 2 (Embeddings)

## 💡 Key Takeaways

- **Tokenization is foundational** to all NLP tasks
- **Vocabulary size affects model capacity** and training
- **Regex patterns determine** how text gets split
- **Special tokens handle edge cases** like unknown words
- **Testing ensures correctness** of implementations
- **Analysis tools help understand** tokenization behavior

Ready to build the foundation of your LLM! 🏗️🤖