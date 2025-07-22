# src/utils/data_utils.py (minimal version)
def load_text_data(file_path: str) -> str:
    """Load text from file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def preprocess_text(text: str) -> str:
    """Basic text preprocessing."""
    return ' '.join(text.lower().split())