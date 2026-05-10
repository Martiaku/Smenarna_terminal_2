from enum import Enum

class Role(Enum):
    ADMIN = "Admin"
    MAJITEL = "Majitel"
    SPRAVCE = "Spravce"
    ZAMESTNANEC = "Zamestnanec"
    
# EN: Define permissions for each role
# CZ: Definice oprávnění pomocí Enum
ROLE_PERMISSIONS = {
    Role.ADMIN: [
        "exchange_currency", "manage_currency", "cash_desk", "course_list",
        "manage_cash_desk", "manage_user", "last_10_transactions", "audit_log",
        "add_money", "withdraw_money", "change_of_course", "add_currency",
        "change_password", "add_user", "edit_permissions", "view_permissions"
    ],
    Role.MAJITEL: [
        "exchange_currency", "course_list"
    ],
    Role.SPRAVCE: [
        "exchange_currency", "course_list"
    ],
    Role.ZAMESTNANEC: [
        "exchange_currency", "course_list"
    ]
}

def has_permissions(role_input, action: str) -> bool:
    # EN: If role_input comes as a string (e.g., "Admin"), we convert it to the Role Enum
    # CZ: Pokud role_input přijde jako string (např. "Admin"), převedeme ho na Enum Role
    if isinstance(role_input, str):
        try:
            # EN: We search for the Enum by its value (Role("Admin") -> Role.ADMIN)
            # CZ: Hledáme Enum podle hodnoty (Role("Admin") -> Role.ADMIN)
            actual_role = Role(role_input)
        except ValueError:
            return False 
    else:
        actual_role = role_input

    allowed_actions = ROLE_PERMISSIONS.get(actual_role, [])
    return action in allowed_actions