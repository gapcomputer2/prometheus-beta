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
    i = 0
    
    while i < len(data):
        # Find longest match in the window
        best_length = 0
        best_offset = 0
        
        # Search back through the window
        for j in range(max(0, len(window) - 4096), len(window)):
            match_length = 0
            
            # Check how long the match continues
            while (i + match_length < len(data) and 
                   j + match_length < len(window) and 
                   data[i + match_length] == window[j + match_length] and 
                   match_length < 258):  # LZO match length limit
                match_length += 1
            
            # Update best match if needed
            if match_length > best_length:
                best_length = match_length
                best_offset = len(window) - j
        
        # Encode the match or literal
        if best_length >= 3:
            # Encode match (offset, length)
            compressed.extend([
                (best_offset >> 8) & 0xFF,  # High byte of offset
                best_offset & 0xFF,         # Low byte of offset
                best_length - 3             # Length minus 3
            ])
            # Move forward in input
            i += best_length
        else:
            # Literal byte
            compressed.append(data[i])
            i += 1
        
        # Update sliding window
        window.append(data[max(0, i-1)])
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
        # Check if there's a potential match
        if i + 2 < len(compressed_data):
            # Check if this is a match or a literal
            if compressed_data[i] < 224:  # Magic number for match detection
                # Decode match
                offset = (compressed_data[i] << 8) | compressed_data[i+1]
                length = compressed_data[i+2] + 3
                
                # Validate match
                start = len(decompressed) - offset
                
                # Protective check to prevent index errors
                if start >= 0:
                    for _ in range(length):
                        if start < len(decompressed):
                            decompressed.append(decompressed[start])
                            start += 1
                
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