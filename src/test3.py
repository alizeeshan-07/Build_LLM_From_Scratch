
"""
This module contains a test function to check if given complex numbers have an imaginary part.
"""
def test_imaginary_numbers():
    # Define a list of complex numbers
    complex_numbers = [1 + 2j, 3 - 4j, 0 + 5j, -1 - 1j, 2 + 0j]
    
    # Check if each number has an imaginary part
    for num in complex_numbers:
        assert num.imag != 0, f"{num} should have an imaginary part"
    
    print("All complex numbers have an imaginary part.")