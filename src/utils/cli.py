"""
Command-line interface for the Build LLM project.
Provides easy access to common operations.
"""

import argparse
import sys
from pathlib import Path

def train_model(args):
    """Train a model with specified configuration."""
    print(f"Training model with config: {args.config}")
    # Import and run training logic
    
def generate_text(args):
    """Generate text using a trained model."""
    print(f"Generating text with prompt: '{args.prompt}'")
    # Import and run generation logic

def tokenize_text(args):
    """Tokenize input text and display results."""
    print(f"Tokenizing: '{args.text}'")
    # Import and run tokenization logic

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Build LLM from Scratch - Command Line Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  build-llm train --config configs/small_model.yaml
  build-llm generate --prompt "The future of AI is"
  build-llm tokenize --text "Hello, world!"
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Train command
    train_parser = subparsers.add_parser('train', help='Train a model')
    train_parser.add_argument('--config', required=True, help='Training configuration file')
    train_parser.set_defaults(func=train_model)
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate text')
    gen_parser.add_argument('--prompt', required=True, help='Text prompt for generation')
    gen_parser.add_argument('--model', default='gpt2-small', help='Model to use')
    gen_parser.add_argument('--max-length', type=int, default=100, help='Maximum generation length')
    gen_parser.set_defaults(func=generate_text)
    
    # Tokenize command
    token_parser = subparsers.add_parser('tokenize', help='Tokenize text')
    token_parser.add_argument('--text', required=True, help='Text to tokenize')
    token_parser.add_argument('--tokenizer', default='simple', help='Tokenizer type')
    token_parser.set_defaults(func=tokenize_text)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)

if __name__ == '__main__':
    main()