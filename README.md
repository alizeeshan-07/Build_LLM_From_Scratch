# 🤖 Build Large Language Model from Scratch

A comprehensive implementation following a modular, educational approach to understanding and building Large Language Models (LLMs) from the ground up.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Auto-Update Docs](https://img.shields.io/badge/docs-auto--updated-green.svg)](.github/workflows/update-readme.yml)

## 🎯 About This Project

This repository provides a **complete, educational implementation** of Large Language Models, designed for:

- 🎓 **Students and researchers** learning about transformer architectures
- 💻 **Developers** wanting to understand LLMs from first principles  
- 🔬 **Practitioners** looking for clean, well-documented reference implementations
- 🤝 **Contributors** interested in advancing open-source ML education

### ✨ **Key Features**
- **Progressive complexity**: Each module builds naturally on previous concepts
- **Production-quality code**: Clean, typed, tested, and documented
- **Educational focus**: Extensive explanations, visualizations, and examples
- **Auto-updating documentation**: README stays synchronized with code changes
- **Interactive learning**: Jupyter notebooks for experimentation
- **Comprehensive testing**: Unit tests ensure code correctness

## 📚 Documentation & Learning Resources

This repository includes comprehensive documentation to support your learning journey:

### 📖 **Core Documentation**
- **[🎯 Learning Path](docs/learning_path.md)** - Step-by-step guide through all modules with time estimates, prerequisites, and study tips
- **[📚 Resources](docs/resources.md)** - Curated collection of papers, books, videos, and online resources
- **[🔧 Troubleshooting](docs/troubleshooting.md)** - Solutions to common implementation, training, and setup issues

### 🎯 **Module-Specific Guides**
Each module includes its own README with:
- Learning objectives and key concepts
- Implementation details and explanations
- Usage examples and best practices
- Common issues and debugging tips

## 🎯 Learning Path

This repository is organized into progressive modules. Here's the recommended learning sequence:

1. **Module 01: Tokenization** (`src/modules/01_tokenization/`)
2. **Module 02: Embeddings** (`src/modules/02_embeddings/`)
3. **Module 03: Attention** (`src/modules/03_attention/`)
4. **Module 04: Transformer Blocks** (`src/modules/04_transformer_blocks/`)
5. **Module 05: Gpt Model** (`src/modules/05_gpt_model/`)
6. **Module 06: Training** (`src/modules/06_training/`)
7. **Module 07: Inference** (`src/modules/07_inference/`)
8. **Module 08: Fine Tuning** (`src/modules/08_fine_tuning/`)

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8+ installed
- Basic familiarity with PyTorch and neural networks
- 8GB+ RAM recommended (16GB+ for larger experiments)

### **Installation**
```bash
# Clone the repository
git clone https://github.com/alizeeshan-07/Build_LLM_From_Scratch.git
cd Build_LLM_From_Scratch

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the project in development mode
pip install -e .

# Verify installation
python examples/quick_start.py
```

### **First Steps**
1. 📖 **Read the [Learning Path](docs/learning_path.md)** to understand the progression
2. 🏃‍♂️ **Start with Module 1**: `src/modules/01_tokenization/`
3. 📚 **Follow along** with the module README and examples
4. 🧪 **Experiment** with the Jupyter notebooks in `notebooks/`
5. ❓ **Get help** from our [Troubleshooting Guide](docs/troubleshooting.md)

## 📖 Module Overview

## Module 01: Tokenization

📁 **Location**: `src/modules/01_tokenization/`

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

### 📋 Files in this Module:

#### `simple_tokenizer.py`
Simple tokenizer implementation using regex-based splitting.

This module implements a basic tokenizer that splits text using regular expressions
and handles unknown tokens with a fallback strategy.

**Key Classes:**
- `TextTokenizer`: A simple regex-based tokenizer for text preprocessing

---

#### `test.py`
Simple test script for TextTokenizer.

This script tests the complete tokenization pipeline:
1. Download and build vocabulary
2. Create tokenizer
3. Test encoding/decoding on various texts

**Key Functions:**
- `test_basic_functionality()`: Test basic tokenizer encode/decode functionality
- `test_vocabulary_analysis()`: Test vocabulary analysis utilities
- `test_tokenization_analysis()`: Test tokenization frequency analysis
- `main()`: Run all tests

---

#### `utils.py`
Utilities specific to tokenization module.

This module provides analysis and visualization tools for understanding
tokenization behavior and vocabulary characteristics.

**Key Functions:**
- `analyze_vocabulary()`: Analyze and display vocabulary statistics
- `plot_token_frequencies()`: Plot most frequent tokens
- `compare_tokenizations()`: Compare two tokenizers side by side
- `tokenization_statistics()`: Calculate comprehensive tokenization statistics

---

#### `build_vocabulary.py`
Vocabulary building utilities for tokenization.

This module downloads sample text and creates vocabularies for tokenizer training.
Based on "The Verdict" text from the LLMs-from-scratch repository.

**Key Functions:**
- `download_sample_text()`: Download sample text file for vocabulary building
- `load_and_analyze_text()`: Load text file and display basic statistics
- `preprocess_text()`: Preprocess text using regex splitting
- `build_vocabulary()`: Build vocabulary dictionary from tokens
- `create_full_vocabulary()`: Complete pipeline to create vocabulary from sample text
- `save_vocabulary()`: Save vocabulary to file for later use
- `load_vocabulary()`: Load vocabulary from file

---

## Module 02: Embeddings

📁 **Location**: `src/modules/02_embeddings/`

*Module files will appear here as you implement them.*

## Module 03: Attention

📁 **Location**: `src/modules/03_attention/`

*Module files will appear here as you implement them.*

## Module 04: Transformer Blocks

📁 **Location**: `src/modules/04_transformer_blocks/`

*Module files will appear here as you implement them.*

## Module 05: Gpt Model

📁 **Location**: `src/modules/05_gpt_model/`

*Module files will appear here as you implement them.*

## Module 06: Training

📁 **Location**: `src/modules/06_training/`

*Module files will appear here as you implement them.*

## Module 07: Inference

📁 **Location**: `src/modules/07_inference/`

*Module files will appear here as you implement them.*

## Module 08: Fine Tuning

📁 **Location**: `src/modules/08_fine_tuning/`

*Module files will appear here as you implement them.*

## 🛠️ Utilities & Tools

Common utilities and tools used across all modules:

### `cli.py`
Command-line interface for the Build LLM project.
Provides easy access to common operations.

### `data_utils.py`
**Key Functions:**
- `load_text_data()`: Load text from file
- `preprocess_text()`: Basic text preprocessing

### `metrics.py`
Evaluation metrics for language models.

### `visualization.py`
Visualization utilities for plotting attention weights, training curves, etc.

**Key Functions:**
- `plot_attention_weights()`: Plot attention weights as a heatmap
- `plot_training_curves()`: Plot training and validation loss curves
- `plot_token_embeddings()`: Plot token embeddings in 2D using dimensionality reduction

## 📁 Project Structure

```
Build_LLM_From_Scratch/
├── 📁 src/
│   ├── 📁 modules/                    # Core LLM implementation modules
│   │   ├── 📁 01_tokenization/        # Text tokenization methods
│   │   ├── 📁 02_embeddings/          # Word and positional embeddings
│   │   ├── 📁 03_attention/           # Attention mechanisms
│   │   ├── 📁 04_transformer_blocks/  # Transformer architecture
│   │   ├── 📁 05_gpt_model/           # Complete GPT model
│   │   ├── 📁 06_training/            # Training procedures
│   │   ├── 📁 07_inference/           # Text generation
│   │   └── 📁 08_fine_tuning/         # Model fine-tuning
│   └── 📁 utils/                      # Common utilities
├── 📁 examples/                       # Usage examples and demos
├── 📁 notebooks/                      # Interactive Jupyter notebooks
├── 📁 tests/                          # Unit tests
├── 📁 docs/                           # Comprehensive documentation
└── 📁 data/                           # Sample datasets (git-ignored)
```

## 💡 Usage Examples

### **Command Line Interface**
```bash
# Quick start demo
python examples/quick_start.py

# Train a small model
python examples/train_small_model.py

# Generate text
python examples/generate_text.py --prompt "The future of AI is"

# Use the CLI tool
build-llm train --config configs/small_model.yaml
build-llm generate --prompt "Hello, world!" --max-length 50
```

### **Python API**
```python
from src.modules.tokenization import SimpleTokenizer
from src.modules.gpt_model import GPTModel
from src.utils import plot_attention_weights

# Tokenize text
tokenizer = SimpleTokenizer()
tokens = tokenizer.encode("Hello, world!")

# Create and use model
model = GPTModel(vocab_size=10000, d_model=512)
output = model(tokens)

# Visualize attention
plot_attention_weights(attention_weights, tokens)
```

## 🤝 Contributing

We welcome contributions! This project is designed to be educational and collaborative.

### **Ways to Contribute**
- 🐛 **Bug reports** - Found an issue? Let us know!
- 💡 **Feature requests** - Ideas for improvements?
- 📝 **Documentation** - Help make explanations clearer
- 🧪 **Testing** - Add tests for better reliability
- 🎓 **Educational content** - Notebooks, examples, tutorials
- 🔧 **Code improvements** - Optimizations and clean-ups

### **Getting Started with Contributing**
1. Read our [Contributing Guidelines](CONTRIBUTING.md)
2. Check out [Good First Issues](https://github.com/alizeeshan-07/Build_LLM_From_Scratch/labels/good%20first%20issue)
3. Fork the repository and create a feature branch
4. Make your changes and add tests if applicable
5. Submit a pull request with a clear description

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📊 Project Stats

- 🐍 **Language**: Python 3.8+
- 🔥 **Framework**: PyTorch 2.0+
- 📦 **Modules**: 8 core learning modules
- 🧪 **Tests**: Comprehensive test coverage
- 📚 **Documentation**: Auto-generated and maintained
- 🤖 **CI/CD**: Automated testing and documentation updates

## 🙏 Acknowledgments

This project is inspired by:
- 📖 "Build a Large Language Model (From Scratch)" book
- 🎓 Stanford CS224N course materials
- 💻 Andrej Karpathy's educational content
- 🤗 Hugging Face's transformer implementations
- 🌟 The broader open-source ML community

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support & Contact

- 💬 **Discussions**: [GitHub Discussions](https://github.com/alizeeshan-07/Build_LLM_From_Scratch/discussions)
- 🐛 **Issues**: [GitHub Issues](https://github.com/alizeeshan-07/Build_LLM_From_Scratch/issues)
- 📧 **Email**: Open an issue for questions
- 📚 **Documentation**: Check our [docs folder](docs/) for detailed guides

---

**⭐ Star this repository if it helps you learn!**

*📝 This README is automatically updated when Python files are modified. Last updated: Auto-generated by GitHub Actions.*
