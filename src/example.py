"""
This module provides mathematical utility functions for basic arithmetic operations.
It includes functions for addition, multiplication, and advanced calculations with proper type hints.
"""

from typing import List, Union, Optional

def add_numbers(a: int, b: int) -> int:
    """
    Add two integers and return the sum.
    
    This function performs basic addition of two integer values.
    
    Args:
        a: The first number to add
        b: The second number to add
    
    Returns:
        The sum of a and b as an integer
    """
    return a + b

def multiply_numbers(x: float, y: float, precision: int = 2) -> float:
    """
    Multiply two numbers with optional precision control.
    
    Args:
        x: First number to multiply
        y: Second number to multiply  
        precision: Number of decimal places to round to
        
    Returns:
        The product of x and y, rounded to specified precision
    """
    result = x * y
    return round(result, precision)

def calculate_average(numbers: List[Union[int, float]]) -> Optional[float]:
    """
    Calculate the average of a list of numbers.
    
    Args:
        numbers: List of integers or floats to average
        
    Returns:
        The arithmetic mean of the numbers, or None if list is empty
    """
    if not numbers:
        return None
    return sum(numbers) / len(numbers)

def power_calculation(base: int, exponent: int = 2, modulo: Optional[int] = None) -> int:
    """
    Calculate base raised to the power of exponent, with optional modulo operation.
    
    Args:
        base: The base number
        exponent: The power to raise the base to
        modulo: Optional modulo value for the result
        
    Returns:
        Result of base^exponent, optionally mod modulo
    """
    result = base ** exponent
    if modulo is not None:
        result = result % modulo
    return result