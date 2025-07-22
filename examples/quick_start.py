"""
Quick start example demonstrating the complete LLM pipeline.
"""

import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def main():
    """Demonstrate basic LLM functionality."""
    print("🤖 Build LLM from Scratch - Quick Start Demo")
    print("=" * 50)
    
    # Example text
    sample_text = "The quick brown fox jumps over the lazy dog."
    
    print(f"Sample text: {sample_text}")
    print("\n1. Tokenization Demo:")
    print("   (Will be implemented in Chapter 1)")
    
    print("\n2. Embedding Demo:")
    print("   (Will be implemented in Chapter 2)")
    
    print("\n3. Attention Demo:")
    print("   (Will be implemented in Chapter 3)")
    
    print("\n4. Full Model Demo:")
    print("   (Will be implemented in Chapter 5)")
    
    print("\n✅ Quick start completed!")
    print("📚 Check individual chapters for detailed implementations.")

if __name__ == "__main__":
    main()