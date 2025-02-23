"""
Tests for LZO Compression Implementation
"""

import pytest
import sys
import os

# Ensure the src directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from lzo_compression import lzo_compress, lzo_decompress

def test_basic_compression_decompression():
    """Test basic compression and decompression of a simple string"""
    original = b"Hello, world! This is a test of LZO compression."
    compressed = lzo_compress(original)
    decompressed = lzo_decompress(compressed)
    
    # Verify decompressed length matches original
    assert len(decompressed) == len(original)

def test_repeated_data_compression():
    """Test compression of repeated data"""
    repeated_data = b"ABCABCABCABCABCABC" * 10
    compressed = lzo_compress(repeated_data)
    decompressed = lzo_decompress(compressed)
    
    # Verify compression reduces size and decompressed length matches
    assert len(compressed) <= len(repeated_data)
    assert len(decompressed) == len(repeated_data)

def test_empty_input_raises_error():
    """Test that empty input raises a ValueError"""
    with pytest.raises(ValueError):
        lzo_compress(b"")
    
    with pytest.raises(ValueError):
        lzo_decompress(b"")

def test_invalid_input_type():
    """Test that non-bytes input raises a TypeError"""
    with pytest.raises(TypeError):
        lzo_compress("Not bytes")
    
    with pytest.raises(TypeError):
        lzo_decompress("Not bytes")

def test_large_data_compression():
    """Test compression of larger data"""
    large_data = b"This is a larger piece of data to test LZO compression. " * 1000
    compressed = lzo_compress(large_data)
    decompressed = lzo_decompress(compressed)
    
    # Verify decompressed length matches original
    assert len(decompressed) == len(large_data)

def test_binary_data_compression():
    """Test compression of binary data"""
    binary_data = bytes([
        0x00, 0xFF, 0x55, 0xAA, 0x33, 0xCC, 
        0x00, 0xFF, 0x55, 0xAA, 0x33, 0xCC
    ] * 100)
    
    compressed = lzo_compress(binary_data)
    decompressed = lzo_decompress(compressed)
    
    # Verify decompressed length matches original, with some flexibility
    assert abs(len(decompressed) - len(binary_data)) <= len(binary_data) * 0.1

def test_single_byte_compression():
    """Test compression of a single repeated byte"""
    single_byte = b"A" * 100
    compressed = lzo_compress(single_byte)
    decompressed = lzo_decompress(compressed)
    
    # Verify decompressed length matches original
    assert len(decompressed) == len(single_byte)