"""
Simple test script for TextTokenizer.

This script tests the complete tokenization pipeline:
1. Download and build vocabulary
2. Create tokenizer
3. Test encoding/decoding on various texts
"""

from build_vocabulary import create_full_vocabulary
from simple_tokenizer import TextTokenizer
from utils import analyze_vocabulary, plot_token_frequencies


def test_basic_functionality():
    """Test basic tokenizer encode/decode functionality."""
    print("=== Testing Basic Functionality ===")
    
    # Build vocabulary
    print("Building vocabulary...")
    vocab = create_full_vocabulary(download_fresh=False)
    print(f"Vocabulary size: {len(vocab)}")
    
    # Create tokenizer
    print("\nCreating tokenizer...")
    tokenizer = TextTokenizer(vocab)
    
    # Test texts
    test_texts = [
        "Hello, world!",
        "This is a test sentence.",
        "What about punctuation? And numbers!",
        "Unknown words will be handled.",
        "The quick brown fox jumps over the lazy dog."
    ]
    
    print("\n=== Testing Tokenization ===")
    for i, text in enumerate(test_texts, 1):
        print(f"\nTest {i}:")
        print(f"Original: {text}")
        
        # Encode
        ids = tokenizer.encode(text)
        print(f"Token IDs: {ids}")
        print(f"Number of tokens: {len(ids)}")
        
        # Decode
        decoded = tokenizer.decode(ids)
        print(f"Decoded: {decoded}")
        
        # Check if round-trip works
        match = text == decoded
        print(f"Perfect match: {match}")
        
        if not match:
            print(f"Difference detected!")


def test_vocabulary_analysis():
    """Test vocabulary analysis utilities."""
    print("\n=== Testing Vocabulary Analysis ===")
    
    vocab = create_full_vocabulary(download_fresh=False)
    analyze_vocabulary(vocab)


def test_tokenization_analysis():
    """Test tokenization frequency analysis."""
    print("\n=== Testing Token Frequency Analysis ===")
    
    # Build vocab and get tokens for analysis
    vocab = create_full_vocabulary(download_fresh=False) 
    
    # Sample text for frequency analysis
    sample_texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Hello world! This is a test.",
        "Machine learning and artificial intelligence.",
        "Natural language processing with transformers."
    ]
    
    # Tokenize all texts
    tokenizer = TextTokenizer(vocab)
    all_tokens = []
    
    for text in sample_texts:
        ids = tokenizer.encode(text)
        tokens = [tokenizer.int_to_str[id] for id in ids]
        all_tokens.extend(tokens)
    
    print(f"Total tokens for analysis: {len(all_tokens)}")
    print(f"Unique tokens: {len(set(all_tokens))}")
    
    # Plot frequencies (if matplotlib available)
    try:
        plot_token_frequencies(all_tokens, top_n=15)
    except ImportError:
        print("Matplotlib not available for plotting")


def main():
    """Run all tests."""
    print("🧪 Starting Tokenization Tests")
    print("=" * 50)
    
    try:
        test_basic_functionality()
        test_vocabulary_analysis()
        test_tokenization_analysis()
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        raise


if __name__ == "__main__":
    main()