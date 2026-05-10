from utils import load_json, save_json, continue_prompt, session
from auth import hash_password, check_password 
import getpass 

def users_change_password():
    if not session.is_logged_in():
        return

    session.header("Změna hesla")
    users = load_json("users.json") or []
    
    print("--- OVĚŘENÍ IDENTITY ---")
    current_password = getpass.getpass("Zadej své současné heslo: ")
    
    # EN: 1. Check if the current password is correct
    # CZ: 1. Kontrola, zda uživatel zná své staré heslo
    if not check_password(current_password, session.current_user['password']):
        print("\n[!] Nesprávné heslo. Změna hesla selhala.")
        continue_prompt()
        return
    
    print("\n--- NOVÉ HESLO ---")
    
    # EN: 2. Hidden password input for confirmation (Important to prevent typos)
    # CZ: 2. Skryté zadání nového hesla pro potvrzení (Důležité pro prevenci překlepů)
    new_password = getpass.getpass("Zadej nové heslo: ")
    confirm_password = getpass.getpass("Potvrď nové heslo: ")
    
    if not new_password:
        print("\n[!] Heslo nemůže být prázdné.")
        continue_prompt(); return

    if new_password != confirm_password:
        print("\n[!] Hesla se neshodují. Změna hesla selhala.")
        continue_prompt()
        return
    
    # EN: 3. Update in database and running session
    # CZ: 3. Aktualizace v databázi i v běžící session
    success = False
    for u in users:
        if u['name'] == session.current_user['name']:
            new_hashed_pw = hash_password(new_password)
            u['password'] = new_hashed_pw
            session.current_user['password'] = new_hashed_pw
            success = True
            break
    
    if success:
        from utils import add_system_log
        add_system_log("Změna hesla", session.current_user['name'])
        save_json("users.json", users)
        print("\n[OK] Heslo bylo úspěšně změněno.")
    else:
        print("\n[!] Chyba: Uživatel nebyl v databázi nalezen.")
        
    continue_prompt()