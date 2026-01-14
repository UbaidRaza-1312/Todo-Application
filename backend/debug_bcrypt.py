#!/usr/bin/env python3
"""
Debug script to check the password truncation logic
"""

from src.utils.auth import get_password_hash

def debug_password_truncation():
    """Debug the password truncation logic"""
    
    # Create a password longer than 72 bytes
    long_password = "a" * 100  # 100 'a' characters
    print(f"Original password length: {len(long_password)} characters")
    print(f"Original password byte length: {len(long_password.encode('utf-8'))} bytes")
    
    # Apply our truncation logic manually
    encoded_password = long_password.encode('utf-8')
    print(f"Encoded password length: {len(encoded_password)} bytes")
    
    if len(encoded_password) > 72:
        encoded_password = encoded_password[:72]
        safe_password = encoded_password.decode('utf-8', errors='ignore')
        print(f"Truncated password length: {len(safe_password)} characters")
        print(f"Truncated password byte length: {len(safe_password.encode('utf-8'))} bytes")
    else:
        safe_password = long_password
    
    print(f"Safe password: {repr(safe_password)}")
    
    # Now try to hash it
    try:
        hashed = get_password_hash(long_password)
        print("Password hashing succeeded!")
        print(f"Hash: {hashed[:50]}...")  # Print first 50 chars of hash
    except Exception as e:
        print(f"Password hashing failed: {e}")

if __name__ == "__main__":
    debug_password_truncation()