"""
Evaluation metrics for language models.
"""

import torch
import numpy as np
from typing import List, Dict

def calculate_perplexity(loss: float) -> float:
    """
    Calculate perplexity from cross-entropy loss.
    
    Args:
        loss: Cross-entropy loss value
        
    Returns:
        Perplexity score
    """
    return torch.exp(torch.tensor(loss)).item()

def calculate_accuracy(predictions: torch.Tensor, targets: torch.Tensor) -> float:
    """
    Calculate token-level accuracy.
    
    Args:
        predictions: Model predictions (logits)
        targets: True target tokens
        
    Returns:
        Accuracy percentage
    """
    pred_tokens = torch.argmax(predictions, dim=-1)
    correct = (pred_tokens == targets).float()
    return correct.mean().item() * 100

def evaluate_model(model, data_loader, device: str = 'cpu') -> Dict[str, float]:
    """
    Evaluate model on a dataset.
    
    Args:
        model: PyTorch model to evaluate
        data_loader: DataLoader with evaluation data
        device: Device to run evaluation on
        
    Returns:
        Dictionary of evaluation metrics
    """
    model.eval()
    total_loss = 0
    total_accuracy = 0
    num_batches = 0
    
    with torch.no_grad():
        for batch in data_loader:
            inputs, targets = batch
            inputs, targets = inputs.to(device), targets.to(device)
            
            outputs = model(inputs)
            loss = torch.nn.functional.cross_entropy(
                outputs.view(-1, outputs.size(-1)), 
                targets.view(-1)
            )
            
            total_loss += loss.item()
            total_accuracy += calculate_accuracy(outputs, targets)
            num_batches += 1
    
    avg_loss = total_loss / num_batches
    avg_accuracy = total_accuracy / num_batches
    perplexity = calculate_perplexity(avg_loss)
    
    return {
        'loss': avg_loss,
        'accuracy': avg_accuracy,
        'perplexity': perplexity
    }