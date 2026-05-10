from utils import load_json, save_json, continue_prompt, session, add_system_log
from auth import hash_password
import getpass 

def add_user():
    session.header("Přidání uživatele")
    
    # EN: Using load_json
    # CZ: Použití load_json
    users = load_json("users.json", default_value=[])
    
    username = input("Zadej nové uživatelské jméno: ").strip()
    
    # EN: 1. Check if user already exists
    # CZ: 1. Kontrola existence uživatele
    if any(u["name"] == username for u in users):
        print(f"[!] Uživatel se jménem '{username}' již existuje.")
        continue_prompt()
        return

    if not username:
        print("[!] Uživatelské jméno nesmí být prázdné!")
        continue_prompt()
        return

    # EN: 2. Hidden password input and confirmation (Key change)
    # CZ: 2. Skryté zadání a potvrzení hesla (Klíčová změna)
    print("\nHeslo zadávejte skrytě (nebude vidět na obrazovce).")
    password = getpass.getpass("Zadej heslo pro nového uživatele: ").strip()
    confirm_password = getpass.getpass("Potvrď heslo pro kontrolu: ").strip()

    if password != confirm_password:
        print("[!] Hesla se neshodují! Uživatel nebyl přidán.")
        continue_prompt()
        return

    if len(password) < 12:
        print("[!] Heslo je příliš krátké (min. 12 znaků).")
        continue_prompt()
        return

    # EN: 3. Role selection
    # CZ: 3. Výběr role
    print("Dostupné role: Admin, Majitel, Spravce, Zamestnanec")
    print("Poznámka: Role jsou citlivé na velikost písmen, zadej přesně.")
    print("Doporučuji odstranit diakritiku z názvů rolí pro lepší stabilitu (např. Spravce místo Správce).")
    role = input("Zadej roli pro nového uživatele: ").strip().capitalize()
    
    valid_roles = ["Admin", "Majitel", "Spravce", "Zamestnanec"]
    if role not in valid_roles:
        print(f"[!] '{role}' není platná role. Uživatel nebyl přidán.")
        continue_prompt()
        return  

    # EN: 4. Saving
    # CZ: 4. Uložení
    new_user = {
        "name": username, 
        "password": hash_password(password), 
        "role": role
    }
    users.append(new_user)
    save_json("users.json", users)
    
    # EN: Logging the action
    # CZ: Logování akce
    add_system_log(f"Vytvořen nový uživatel: {username} ({role})", session.current_user['name'])
    
    print(f"\n[OK] Uživatel '{username}' s rolí '{role}' byl úspěšně přidán.")
    continue_prompt()