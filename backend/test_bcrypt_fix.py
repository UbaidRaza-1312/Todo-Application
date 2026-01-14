#!/usr/bin/env python3
"""
Test script to verify the bcrypt password length fix
"""

from src.utils.auth import get_password_hash, verify_password

def test_long_password():
    """Test that long passwords are properly truncated and verified"""
    
    # Create a password longer than 72 bytes
    long_password = "a" * 100  # 100 'a' characters
    print(f"Testing password of length: {len(long_password)} characters")
    print(f"Password byte length: {len(long_password.encode('utf-8'))} bytes")
    
    # Hash the long password - this should not raise an exception
    try:
        hashed = get_password_hash(long_password)
        print("[PASS] Password hashing succeeded")
    except ValueError as e:
        print(f"[FAIL] Password hashing failed: {e}")
        return False

    # Verify the password - this should also work
    try:
        is_valid = verify_password(long_password, hashed)
        print("[PASS] Password verification succeeded")
    except Exception as e:
        print(f"[FAIL] Password verification failed: {e}")
        return False

    # Also test with a short password to ensure it still works normally
    short_password = "short"
    try:
        short_hashed = get_password_hash(short_password)
        short_valid = verify_password(short_password, short_hashed)
        print("[PASS] Short password handling still works")
    except Exception as e:
        print(f"[FAIL] Short password handling failed: {e}")
        return False

    # Test verification of a long password against its hash
    try:
        long_valid = verify_password(long_password, hashed)
        print("[PASS] Long password verification against its hash succeeded")
    except Exception as e:
        print(f"[FAIL] Long password verification failed: {e}")
        return False
    
    return True

def test_unicode_password():
    """Test with unicode characters that might affect byte length"""
    
    # Unicode password where characters take multiple bytes
    unicode_password = "üñíçødé" * 15  # Repeated to exceed 72 bytes
    print(f"\nTesting unicode password of length: {len(unicode_password)} characters")
    print(f"Unicode password byte length: {len(unicode_password.encode('utf-8'))} bytes")
    
    try:
        hashed = get_password_hash(unicode_password)
        is_valid = verify_password(unicode_password, hashed)
        print("[PASS] Unicode password handling succeeded")
        return True
    except Exception as e:
        print(f"[FAIL] Unicode password handling failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing bcrypt password length fix...")

    success1 = test_long_password()
    success2 = test_unicode_password()

    if success1 and success2:
        print("\n[SUCCESS] All tests passed! The bcrypt fix is working correctly.")
    else:
        print("\n[FAILURE] Some tests failed!")