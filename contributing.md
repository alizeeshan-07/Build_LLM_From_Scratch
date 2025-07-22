# Contributing to Build LLM from Scratch

Thank you for your interest in contributing to this educational project! 

## 🎯 Project Goals

This repository aims to:
- Provide clear, educational implementations of LLM concepts
- Follow the book's progression chapter by chapter
- Maintain high code quality with comprehensive documentation
- Help others learn by example

## 🚀 Getting Started

1. Fork the repository
2. Create a new branch for your feature: `git checkout -b feature/chapter-X-improvement`
3. Make your changes following our guidelines below
4. Test your changes
5. Submit a pull request

## 📝 Code Guidelines

### Documentation Standards
- **Every function must have a docstring** explaining purpose, parameters, and returns
- **Add educational comments** explaining complex concepts
- **Include type hints** for better code clarity
- **Add examples** in docstrings when helpful

### Code Style
- Follow PEP 8 Python style guide
- Use Black for code formatting: `black src/`
- Maximum line length: 88 characters
- Use descriptive variable names

### Chapter Structure
When adding a new chapter:
src/chapter_XX_topic_name/
├── init.py
├── README.md          # Chapter overview and learning objectives
├── core_module.py     # Main implementation
├── utils.py          # Helper functions
└── examples.py       # Usage examples

## 🧪 Testing

- Add tests for new functionality in the `tests/` directory
- Run tests with: `pytest tests/`
- Ensure all tests pass before submitting PR

## 📚 Educational Focus

Remember this is an educational project:
- **Prioritize clarity over optimization**
- **Add comments explaining "why" not just "what"**
- **Include references to the book sections**
- **Provide working examples**

## 🐛 Bug Reports

When reporting bugs, please include:
- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Your environment (Python version, OS, etc.)

## 💡 Feature Requests

For new features:
- Explain how it helps with learning LLMs
- Reference relevant book chapters
- Provide implementation suggestions if possible

## 📊 Code Review Process

### For Contributors
- Ensure your code follows the style guidelines
- Write comprehensive tests for new functionality
- Update documentation as needed
- Keep PRs focused and reasonably sized

### For Reviewers
- Focus on educational value and clarity
- Check for proper documentation
- Verify tests are included and passing
- Ensure code follows project structure

## 🎓 Educational Standards

### Code Comments
```python
def attention(query, key, value):
    """
    Compute attention weights and values.
    
    Educational Note:
    This implements the core attention mechanism where:
    - Query: "What am I looking for?"
    - Key: "What do I have available?"
    - Value: "What do I actually return?"
    """
    # Compute similarity scores (attention weights)
    scores = torch.matmul(query, key.transpose(-2, -1))
    
    # Apply softmax to get probabilities
    weights = F.softmax(scores, dim=-1)
    
    # Apply weights to values
    output = torch.matmul(weights, value)
    return output, weights