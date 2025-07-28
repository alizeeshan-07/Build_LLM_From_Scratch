"""
Utilities specific to tokenization module.

This module provides analysis and visualization tools for understanding
tokenization behavior and vocabulary characteristics.
"""

from collections import Counter
from typing import List, Dict, Tuple, Any


def analyze_vocabulary(vocab: Dict[str, int]) -> None:
    """
    Analyze and display vocabulary statistics.
    
    Args:
        vocab: Vocabulary dictionary mapping tokens to IDs
    """
    print(f"📊 Vocabulary Analysis")
    print(f"{'='*30}")
    print(f"Vocabulary size: {len(vocab)}")
    
    # Character analysis
    all_chars = set()
    for token in vocab.keys():
        all_chars.update(token)
    print(f"Unique characters: {len(all_chars)}")
    
    # Token length analysis
    token_lengths = [len(token) for token in vocab.keys()]
    avg_length = sum(token_lengths) / len(token_lengths)
    max_length = max(token_lengths)
    min_length = min(token_lengths)
    
    print(f"Average token length: {avg_length:.2f}")
    print(f"Longest token: '{max(vocab.keys(), key=len)}' (length: {max_length})")
    print(f"Shortest token: '{min(vocab.keys(), key=len)}' (length: {min_length})")
    
    # Token type analysis
    alphabetic = sum(1 for token in vocab.keys() if token.isalpha())
    numeric = sum(1 for token in vocab.keys() if token.isnumeric())
    punctuation = sum(1 for token in vocab.keys() if not token.isalnum())
    
    print(f"\n📝 Token Types:")
    print(f"Alphabetic tokens: {alphabetic} ({alphabetic/len(vocab)*100:.1f}%)")
    print(f"Numeric tokens: {numeric} ({numeric/len(vocab)*100:.1f}%)")
    print(f"Punctuation/Other: {punctuation} ({punctuation/len(vocab)*100:.1f}%)")
    
    # Show some examples
    print(f"\n🔤 Sample Tokens:")
    sample_tokens = list(vocab.items())[:10]
    for token, idx in sample_tokens:
        print(f"  '{token}' -> {idx}")


def plot_token_frequencies(tokens: List[str], top_n: int = 20) -> None:
    """
    Plot most frequent tokens.
    
    Args:
        tokens: List of tokens to analyze
        top_n: Number of top tokens to display
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("❌ matplotlib not available. Install with: pip install matplotlib")
        return
    
    if not tokens:
        print("❌ No tokens to plot!")
        return
    
    # Count token frequencies
    token_counts = Counter(tokens)
    top_tokens = token_counts.most_common(top_n)
    
    if not top_tokens:
        print("❌ No tokens found!")
        return
    
    tokens_list, counts = zip(*top_tokens)
    
    # Create plot
    plt.figure(figsize=(12, 6))
    bars = plt.bar(range(len(tokens_list)), counts, color='skyblue', alpha=0.7)
    
    # Customize plot
    plt.xticks(range(len(tokens_list)), tokens_list, rotation=45, ha='right')
    plt.xlabel('Tokens')
    plt.ylabel('Frequency')
    plt.title(f'Top {top_n} Most Frequent Tokens')
    plt.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{count}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.show()
    
    # Print statistics
    total_tokens = len(tokens)
    top_frequency = sum(counts)
    coverage = (top_frequency / total_tokens) * 100
    
    print(f"📈 Frequency Analysis:")
    print(f"Total tokens analyzed: {total_tokens}")
    print(f"Top {top_n} tokens represent {coverage:.1f}% of all tokens")
    print(f"Most frequent token: '{tokens_list[0]}' ({counts[0]} times)")


def compare_tokenizations(text: str, tokenizer1: Any, tokenizer2: Any, 
                         name1: str = "Tokenizer 1", name2: str = "Tokenizer 2") -> None:
    """
    Compare two tokenizers side by side.
    
    Args:
        text: Input text to tokenize
        tokenizer1: First tokenizer (must have .encode() method)
        tokenizer2: Second tokenizer (must have .encode() method)
        name1: Name for first tokenizer
        name2: Name for second tokenizer
    """
    print(f"🔄 Tokenizer Comparison")
    print(f"{'='*50}")
    print(f"Input text: {text}")
    print(f"Text length: {len(text)} characters")
    
    try:
        # Tokenize with both tokenizers
        tokens1 = tokenizer1.encode(text)
        tokens2 = tokenizer2.encode(text)
        
        print(f"\n{name1}:")
        print(f"  Token count: {len(tokens1)}")
        print(f"  Token IDs: {tokens1}")
        print(f"  Compression ratio: {len(text)/len(tokens1):.2f} chars/token")
        
        print(f"\n{name2}:")
        print(f"  Token count: {len(tokens2)}")
        print(f"  Token IDs: {tokens2}")
        print(f"  Compression ratio: {len(text)/len(tokens2):.2f} chars/token")
        
        # Comparison
        efficiency_1 = len(text) / len(tokens1)
        efficiency_2 = len(text) / len(tokens2)
        
        if efficiency_1 > efficiency_2:
            winner = name1
            difference = ((efficiency_1 - efficiency_2) / efficiency_2) * 100
        elif efficiency_2 > efficiency_1:
            winner = name2
            difference = ((efficiency_2 - efficiency_1) / efficiency_1) * 100
        else:
            winner = "Tie"
            difference = 0
        
        print(f"\n🏆 Comparison Result:")
        if winner != "Tie":
            print(f"  More efficient: {winner}")
            print(f"  Efficiency gain: {difference:.1f}%")
        else:
            print(f"  Both tokenizers have equal efficiency")
            
    except Exception as e:
        print(f"❌ Error during comparison: {e}")


def tokenization_statistics(tokenizer: Any, texts: List[str]) -> Dict[str, float]:
    """
    Calculate comprehensive tokenization statistics.
    
    Args:
        tokenizer: Tokenizer with .encode() method
        texts: List of texts to analyze
        
    Returns:
        Dictionary with statistics
    """
    if not texts:
        return {}
    
    total_chars = sum(len(text) for text in texts)
    total_tokens = 0
    token_lengths = []
    
    for text in texts:
        tokens = tokenizer.encode(text)
        total_tokens += len(tokens)
        token_lengths.extend([len(tokenizer.int_to_str[tid]) for tid in tokens])
    
    stats = {
        'total_texts': len(texts),
        'total_characters': total_chars,
        'total_tokens': total_tokens,
        'avg_chars_per_text': total_chars / len(texts),
        'avg_tokens_per_text': total_tokens / len(texts),
        'compression_ratio': total_chars / total_tokens,
        'avg_token_length': sum(token_lengths) / len(token_lengths),
        'vocabulary_size': len(tokenizer.str_to_int)
    }
    
    return stats


if __name__ == "__main__":
    # Example usage
    print("🛠️ Tokenization Utils Demo")
    
    # This would normally use real tokenizer
    sample_vocab = {"hello": 0, "world": 1, ",": 2, "!": 3, "test": 4}
    
    print("✅ Utils module loaded successfully!")
    print("Import this module to use tokenization analysis tools.")