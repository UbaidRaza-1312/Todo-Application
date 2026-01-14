#!/usr/bin/env python3
"""
Direct bcrypt test to see if the issue is with passlib
"""

import bcrypt

def direct_bcrypt_test():
    """Test bcrypt directly"""
    
    # Create a password longer than 72 bytes
    long_password = "a" * 100  # 100 'a' characters
    print(f"Testing password of length: {len(long_password)} characters")
    print(f"Password byte length: {len(long_password.encode('utf-8'))} bytes")
    
    # Apply truncation
    encoded_password = long_password.encode('utf-8')
    if len(encoded_password) > 72:
        encoded_password = encoded_password[:72]
        safe_password = encoded_password.decode('utf-8', errors='ignore')
    else:
        safe_password = long_password
    
    print(f"Safe password length: {len(safe_password)} characters")
    print(f"Safe password byte length: {len(safe_password.encode('utf-8'))} bytes")
    
    # Hash using bcrypt directly
    try:
        hashed = bcrypt.hashpw(safe_password.encode('utf-8'), bcrypt.gensalt())
        print("SUCCESS: Direct bcrypt hashing worked!")
        print(f"Hash: {hashed[:50]}...")  # Print first 50 chars of hash
        
        # Verify the password
        is_valid = bcrypt.checkpw(safe_password.encode('utf-8'), hashed)
        print(f"Verification result: {is_valid}")
        
        return True
    except ValueError as e:
        print(f"FAILED: Direct bcrypt hashing failed: {e}")
        return False
    except Exception as e:
        print(f"OTHER ERROR: {e}")
        return False

if __name__ == "__main__":
    direct_bcrypt_test()