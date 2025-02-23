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
        # Look for repeated patterns
        max_match_length = 0
        max_match_offset = 0
        
        # Search back in previously processed data
        search_start = max(0, i - 4096)
        for j in range(search_start, i):
            # Try to find the longest matching sequence
            match_length = 0
            while (i + match_length < len(data) and 
                   j + match_length < i and 
                   data[j + match_length] == data[i + match_length] and 
                   match_length < 255):
                match_length += 1
            
            # Update best match
            if match_length > max_match_length:
                max_match_length = match_length
                max_match_offset = i - j
        
        # Encode based on match length
        if max_match_length > 2:
            # Encode as a match (offset, length)
            compressed.extend([
                0xFF,  # Flag for match encoding
                max_match_offset & 0xFF,  # Offset (low byte)
                max_match_length  # Match length
            ])
            i += max_match_length
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
            # Encoded match
            offset = compressed_data[i + 1]
            length = compressed_data[i + 2]
            
            # Reconstruct the matched sequence
            start = len(decompressed) - offset
            for _ in range(length):
                if start >= 0 and start < len(decompressed):
                    decompressed.append(decompressed[start])
                    start += 1
            
            i += 3
        else:
            # Literal byte
            decompressed.append(compressed_data[i])
            i += 1
    
    return decompressed