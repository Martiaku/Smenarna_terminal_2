import pytest
from permissions import has_permissions, Role

def test_admin_permissions():
    # En: Admin should have access to all permissions
    # CZ: Admin musí mít přístup k citlivým věcem
    assert has_permissions("Admin", "manage_user") is True
    assert has_permissions("Admin", "audit_log") is True

def test_employee_restrictions():
    # En: Employee should not be able to manage users
    # CZ: Zaměstnanec nesmí spravovat uživatele
    assert has_permissions("Zamestnanec", "manage_user") is False

def test_invalid_role():
    # En: Invalid roles should have no permissions
    # CZ: Neexistující role nesmí mít žádná práva
    assert has_permissions("Hackerman", "exchange_currency") is False
    
def test_menu_filtering_for_employee():
    from menu_config import MENU_DEFINITIONS
    
    role = "Zamestnanec"
    available = [item for item in MENU_DEFINITIONS if has_permissions(role, item["perm"])]
    
    # En: Employee should only have access to certain menu items
    # CZ: Zaměstnanec má v tvém nastavení jen 2 práva v hlavním menu
    assert len(available) == 2
    assert available[0]["label"] == "Převod měn"
    
    
def test_permissions_for_owner():
    # En: Owner should have access to most features, but not all
    # CZ: Majitel by měl mít přístup k většině věcí, ale ne ke všemu
    assert has_permissions("Majitel", "manage_user") is False
    assert has_permissions("Majitel", "audit_log") is False    
    assert has_permissions("Admin", "exchange_currency") is True