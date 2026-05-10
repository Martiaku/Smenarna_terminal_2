from permissions import ROLE_PERMISSIONS, Role
from utils import continue_prompt

def print_permission_matrix():
    # EN: Import the dictionary with labels here to avoid circular imports
    # CZ: Importujeme slovník s popisky až tady, abychom se vyhnuli circular importům
    from menu_config import PERM_LABELS
    
    print(f"\n{'FUNKCE SYSTÉMU (klíč)':<45} | {'ADMIN':<7} | {'MAJITEL':<7} | {'ZAMĚSTNANEC':<11}")
    print("-" * 90)

    all_perm_keys = set()
    for actions in ROLE_PERMISSIONS.values():
        all_perm_keys.update(actions)

    sorted_keys = sorted(all_perm_keys, key=lambda k: PERM_LABELS.get(k, k))

    for key in sorted_keys:
        # EN: Combine label and key into one text
        # CZ: Spojíme label a klíč do jednoho textu
        human_name = PERM_LABELS.get(key, key)
        display_label = f"{human_name} ({key})"
        
        has_admin = " [X] " if key in ROLE_PERMISSIONS.get(Role.ADMIN, []) else " [ ] "
        has_owner = " [X] " if key in ROLE_PERMISSIONS.get(Role.MAJITEL, []) else " [ ] "
        has_staff = " [X] " if key in ROLE_PERMISSIONS.get(Role.ZAMESTNANEC, []) else " [ ] "

        print(f"{display_label:<45} | {has_admin:<7} | {has_owner:<7} | {has_staff:<11}")
    
    print("\n[X] = Povolen přístup | [ ] = Zakázán přístup")
    continue_prompt()

