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
    
    # DEBUG: Check if special tokens are in vocabulary
    print(f"\nDEBUG: Checking special tokens...")
    print(f"<|unk|> in vocab: {'<|unk|>' in vocab}")
    print(f"<|endoftext|> in vocab: {'<|endoftext|>' in vocab}")
    
    # Show some vocab entries
    print(f"\nFirst 10 vocab entries:")
    for i, (token, idx) in enumerate(list(vocab.items())[:10]):
        print(f"  '{token}' -> {idx}")
    
    print(f"\nLast 10 vocab entries:")
    for token, idx in list(vocab.items())[-10:]:
        print(f"  '{token}' -> {idx}")
    
    # Create tokenizer
    print("\nCreating tokenizer...")
    tokenizer = TextTokenizer(vocab)
    
    # Test with simple text first
    simple_test = "Hello, world!"
    print(f"\nTesting simple text: {simple_test}")
    
    try:
        ids = tokenizer.encode(simple_test)
        decoded = tokenizer.decode(ids)
        print(f"Success! IDs: {ids}")
        print(f"Decoded: {decoded}")
    except Exception as e:
        print(f"Error with simple text: {e}")
        return


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