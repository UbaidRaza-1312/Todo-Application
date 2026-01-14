#!/usr/bin/env python3
"""
Fresh test script to check the password truncation logic
"""

import sys
import importlib

# Clear any cached modules
modules_to_clear = [k for k in sys.modules.keys() if k.startswith('src')]
for module in modules_to_clear:
    del sys.modules[module]

# Now import fresh
from src.utils.auth import get_password_hash

def fresh_test():
    """Fresh test of the password truncation logic"""
    
    # Create a password longer than 72 bytes
    long_password = "a" * 100  # 100 'a' characters
    print(f"Testing password of length: {len(long_password)} characters")
    print(f"Password byte length: {len(long_password.encode('utf-8'))} bytes")
    
    # Hash the long password - this should not raise an exception
    try:
        hashed = get_password_hash(long_password)
        print("SUCCESS: Password hashing succeeded")
        print(f"Hash: {hashed[:50]}...")  # Print first 50 chars of hash
        return True
    except ValueError as e:
        print(f"FAILED: Password hashing failed: {e}")
        return False
    except Exception as e:
        print(f"OTHER ERROR: {e}")
        return False

if __name__ == "__main__":
    fresh_test()