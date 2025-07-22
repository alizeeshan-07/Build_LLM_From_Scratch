# 🤖 Build Large Language Model from Scratch

A comprehensive implementation following the book's methodology, with clear chapter-by-chapter progression.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📚 About This Repository

This repository contains a complete implementation of a Large Language Model (LLM) built from scratch, following best practices for educational purposes. Each chapter builds upon the previous one, creating a fully functional GPT-style model.

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

```bash
# Clone the repository
git clone https://github.com/alizeeshan-07/Build_LLM_From_Scratch.git
cd Build_LLM_From_Scratch

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run a quick demo
python examples/quick_start.py
```

## 📖 Module Details

## Module 01: Tokenization

📁 **Location**: `src/modules/01_tokenization/`

## Module 02: Embeddings

📁 **Location**: `src/modules/02_embeddings/`

## Module 03: Attention

📁 **Location**: `src/modules/03_attention/`

## Module 04: Transformer Blocks

📁 **Location**: `src/modules/04_transformer_blocks/`

## Module 05: Gpt Model

📁 **Location**: `src/modules/05_gpt_model/`

## Module 06: Training

📁 **Location**: `src/modules/06_training/`

## Module 07: Inference

📁 **Location**: `src/modules/07_inference/`

## Module 08: Fine Tuning

📁 **Location**: `src/modules/08_fine_tuning/`

## 🛠️ Utilities

Common utilities used across all chapters:

### `visualization.py`
Visualization utilities for plotting attention weights, training curves, etc.

- `plot_attention_weights()`: Plot attention weights as a heatmap
- `plot_training_curves()`: Plot training and validation loss curves
- `plot_token_embeddings()`: Plot token embeddings in 2D using dimensionality reduction

### `cli.py`
Command-line interface for the Build LLM project.
Provides easy access to common operations.

- `train_model()`: Train a model with specified configuration
- `generate_text()`: Generate text using a trained model
- `tokenize_text()`: Tokenize input text and display results
- `main()`: Main CLI entry point

### `data_utils.py`
Data processing utilities for loading and preprocessing text data.

- `load_text_data()`: Load text data from a file
- `preprocess_text()`: Basic text preprocessing
- `create_vocab()`: Create vocabulary from list of texts

### `metrics.py`
Evaluation metrics for language models.

- `calculate_perplexity()`: Calculate perplexity from cross-entropy loss
- `calculate_accuracy()`: Calculate token-level accuracy
- `evaluate_model()`: Evaluate model on a dataset

### `init.py`
Utility functions and helpers for the Build LLM project.

## 📄 Project Structure

```
src/
├── modules/
│   ├── 01_tokenization/           # Text tokenization methods
│   ├── 02_embeddings/             # Word and positional embeddings
│   ├── 03_attention/              # Attention mechanisms
│   ├── 04_transformer_blocks/     # Transformer architecture
│   ├── 05_gpt_model/              # Complete GPT model
│   ├── 06_training/               # Training procedures
│   ├── 07_inference/              # Text generation
│   └── 08_fine_tuning/            # Model fine-tuning
└── utils/                         # Common utilities
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Make sure to follow the existing code structure and add appropriate documentation.

## 📧 Contact

Feel free to reach out if you have questions about the implementation or want to discuss LLM concepts!

---
*📝 This README is automatically updated when Python files are modified.*
