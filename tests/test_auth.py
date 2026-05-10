import pytest
from auth import hash_password, check_password

def test_password_hashing_success():
    """
    EN: Tests that the correct password passes the check.
    CZ: Testuje, že správné heslo projde ověřením.
    """
    password = "MojeTajneHeslo123"
    hashed = hash_password(password)
    
    # EN: Verify that check_password returns True
    # CZ: Ověříme, že check_password vrátí True
    assert check_password(password, hashed) is True

def test_password_hashing_failure():
    """
    EN: Tests that an incorrect password fails the check.
    CZ: Testuje, že špatné heslo neprojde ověřením.
    """
    password = "MojeTajneHeslo123"
    hashed = hash_password(password)
    
    # EN: Verify that check_password returns False for an incorrect password
    # CZ: Ověříme, že check_password vrátí False pro špatné heslo
    assert check_password("SpatneHeslo", hashed) is False

def test_hashes_are_unique():
    """
    EN: Tests that two identical passwords have different hashes due to salt.
    CZ: Testuje, že dvě stejná hesla mají díky soli jiný hash.
    """
    password = "heslo"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    
    assert hash1 != hash2