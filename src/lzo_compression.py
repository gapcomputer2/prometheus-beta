"""
Simplified LZO-like Compression Implementation

This module provides a basic compression algorithm focusing on run-length encoding.
"""

def lzo_compress(data):
    """
    Compress input data using a simplified run-length encoding approach.
    
    Args:
        data (bytes or bytearray): Input data to be compressed
    
    Returns:
        bytearray: Compressed data
    
    Raises:
        TypeError: If input is not bytes or bytearray
        ValueError: If input data is empty
    """
    # Input validation
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("Input must be bytes or bytearray")
    
    if not data:
        raise ValueError("Input data cannot be empty")
    
    compressed = bytearray()
    i = 0
    
    while i < len(data):
        # Count repeated bytes
        repeat_count = 1
        while i + repeat_count < len(data) and data[i] == data[i + repeat_count] and repeat_count < 255:
            repeat_count += 1
        
        if repeat_count > 2:
            # Encode repeated bytes
            compressed.extend([
                0xFF,  # Flag for run-length encoding
                repeat_count,  # Number of repeats
                data[i]  # The repeated byte
            ])
            i += repeat_count
        else:
            # Literal byte
            compressed.append(data[i])
            i += 1
    
    return compressed

def lzo_decompress(compressed_data):
    """
    Decompress data that was compressed using the simplified algorithm.
    
    Args:
        compressed_data (bytes or bytearray): Compressed input data
    
    Returns:
        bytearray: Decompressed data
    
    Raises:
        TypeError: If input is not bytes or bytearray
        ValueError: If input data is empty or invalid
    """
    # Input validation
    if not isinstance(compressed_data, (bytes, bytearray)):
        raise TypeError("Input must be bytes or bytearray")
    
    if not compressed_data:
        raise ValueError("Input data cannot be empty")
    
    decompressed = bytearray()
    i = 0
    
    while i < len(compressed_data):
        if i + 2 < len(compressed_data) and compressed_data[i] == 0xFF:
            # Run-length encoded sequence
            repeat_count = compressed_data[i + 1]
            byte_to_repeat = compressed_data[i + 2]
            decompressed.extend([byte_to_repeat] * repeat_count)
            i += 3
        else:
            # Literal byte
            decompressed.append(compressed_data[i])
            i += 1
    
    return decompressed