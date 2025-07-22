"""
Visualization utilities for plotting attention weights, training curves, etc.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import List, Optional

def plot_attention_weights(attention_weights: np.ndarray, 
                         tokens: List[str],
                         figsize: tuple = (10, 8),
                         save_path: Optional[str] = None):
    """
    Plot attention weights as a heatmap.
    
    Args:
        attention_weights: 2D array of attention weights
        tokens: List of token strings
        figsize: Figure size tuple
        save_path: Optional path to save the plot
    """
    plt.figure(figsize=figsize)
    
    sns.heatmap(attention_weights,
                xticklabels=tokens,
                yticklabels=tokens,
                cmap='Blues',
                annot=True,
                fmt='.2f')
    
    plt.title('Attention Weights Visualization')
    plt.xlabel('Keys')
    plt.ylabel('Queries')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()

def plot_training_curves(train_losses: List[float], 
                        val_losses: List[float],
                        save_path: Optional[str] = None):
    """
    Plot training and validation loss curves.
    
    Args:
        train_losses: List of training losses
        val_losses: List of validation losses  
        save_path: Optional path to save the plot
    """
    plt.figure(figsize=(10, 6))
    
    epochs = range(1, len(train_losses) + 1)
    
    plt.plot(epochs, train_losses, 'b-', label='Training Loss')
    plt.plot(epochs, val_losses, 'r-', label='Validation Loss')
    
    plt.title('Training Progress')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()

def plot_token_embeddings(embeddings: np.ndarray,
                         tokens: List[str],
                         method: str = 'pca'):
    """
    Plot token embeddings in 2D using dimensionality reduction.
    
    Args:
        embeddings: Token embedding matrix
        tokens: List of token strings
        method: Dimensionality reduction method ('pca' or 'tsne')
    """
    from sklearn.decomposition import PCA
    from sklearn.manifold import TSNE
    
    if method == 'pca':
        reducer = PCA(n_components=2)
    else:
        reducer = TSNE(n_components=2, random_state=42)
    
    embeddings_2d = reducer.fit_transform(embeddings)
    
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], alpha=0.7)
    
    # Add labels for a subset of points
    for i, token in enumerate(tokens[:20]):  # Show first 20 tokens
        plt.annotate(token, (embeddings_2d[i, 0], embeddings_2d[i, 1]),
                    xytext=(5, 5), textcoords='offset points',
                    fontsize=8, alpha=0.8)
    
    plt.title(f'Token Embeddings Visualization ({method.upper()})')
    plt.xlabel('Component 1')
    plt.ylabel('Component 2')
    plt.grid(True, alpha=0.3)
    plt.show()