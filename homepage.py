from utils import clear_terminal, session, continue_prompt, add_system_log
from permissions import has_permissions


def homepage(current_user):
    from menu_config import MENU_DEFINITIONS
    
    role = current_user["role"]
    
    while True:
        clear_terminal()
        session.header("Hlavní menu")
        
        available_menu = [
            item for item in MENU_DEFINITIONS 
            if has_permissions(role, item["perm"])
        ]
        
        if not available_menu:
            print("[!] Vaše role nemá přiřazena žádná oprávnění.")
        else:
            for i, item in enumerate(available_menu, 1):
                print(f"{i} - {item['label']}")
        
        print("q - Odhlášení")
        
        volba = input("\nJaká je tvoje volba: ").strip().lower()
        
        if volba == 'q':
            add_system_log("Odhlášení uživatele", current_user['name'])
            session.current_user = None
            break
            
        try:
            index = int(volba) - 1
            if 0 <= index < len(available_menu):
                available_menu[index]["func"]()
            else:
                raise ValueError
        except (ValueError, IndexError):
            print("\n[!] Neplatná volba.")
            continue_prompt()