"""
Lempel-Ziv-Oberhumer (LZO) Data Compression Implementation

This module provides a basic implementation of LZO compression algorithm.
Note: This is a simplified version and not a full cryptographically secure implementation.
"""

def lzo_compress(data):
    """
    Compress input data using a simplified LZO-like compression algorithm.
    
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
    
    # Compression logic
    compressed = bytearray()
    window = bytearray()
    
    for byte in data:
        # Try to find the longest match in the current window
        match_length = 0
        match_offset = 0
        
        for i in range(max(0, len(window) - 4096), len(window)):
            current_match_length = 0
            j = 0
            
            # Find longest match
            while (i + j < len(window) and 
                   j < len(data) and 
                   window[i + j] == byte):
                current_match_length += 1
                j += 1
            
            # Update best match if current match is longer
            if current_match_length > match_length:
                match_length = current_match_length
                match_offset = len(window) - i
        
        # Add byte or match to compressed output
        if match_length > 2:
            # Encode match as (offset, length)
            compressed.extend([
                (match_offset >> 8) & 0xFF,  # High byte of offset
                match_offset & 0xFF,         # Low byte of offset
                match_length - 3             # Length minus 3 (to save bits)
            ])
        else:
            # Literal byte
            compressed.append(byte)
        
        # Update sliding window
        window.append(byte)
        if len(window) > 4096:
            window = window[-4096:]
    
    return compressed

def lzo_decompress(compressed_data):
    """
    Decompress data that was compressed using the LZO-like algorithm.
    
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
    
    # Decompression logic
    decompressed = bytearray()
    i = 0
    
    while i < len(compressed_data):
        # Check if it's a match or literal
        if i + 2 < len(compressed_data):
            # Potential match encoding
            offset = (compressed_data[i] << 8) | compressed_data[i+1]
            length = compressed_data[i+2] + 3
            
            # Check if this looks like a valid match
            if offset < len(decompressed) and length > 0:
                # Reconstruct match
                start = len(decompressed) - offset
                for j in range(length):
                    if start + j < 0:
                        break
                    decompressed.append(decompressed[start + j])
                i += 3
            else:
                # Literal byte
                decompressed.append(compressed_data[i])
                i += 1
        else:
            # Remaining bytes are literals
            decompressed.append(compressed_data[i])
            i += 1
    
    return decompressed