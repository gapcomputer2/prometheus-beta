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
        max_repeat = 0
        repeat_byte = None
        
        # Check for repeated sequences
        for j in range(1, min(256, len(data) - i + 1)):
            current_window = data[i:i+j]
            if len(set(current_window)) == 1:
                max_repeat = j
                repeat_byte = current_window[0]
        
        if max_repeat > 2:
            # Encode repeated bytes
            compressed.extend([
                0xFF,  # Flag for run-length encoding
                max_repeat - 1,  # Number of additional repeats
                repeat_byte  # The repeated byte
            ])
            i += max_repeat
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
            repeat_count = compressed_data[i + 1] + 1
            byte_to_repeat = compressed_data[i + 2]
            decompressed.extend([byte_to_repeat] * repeat_count)
            i += 3
        else:
            # Literal byte
            decompressed.append(compressed_data[i])
            i += 1
    
    return decompressed