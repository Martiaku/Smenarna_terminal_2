from utils import continue_prompt, load_json, save_json, session
from auth import hash_password, check_password
from homepage import homepage
from utils import add_system_log
import getpass

def login():
    users = load_json("users.json") or []
    session.header("Přihlášení do systému")

    # EN: --- SAFE BOOTSTRAP ---
    # CZ:--- BEZPEČNÝ BOOTSTRAP ---
    if not users:
        print("Systém je prázdný. Je nutné vytvořit prvního administrátora.")
        
        while True:
            print("Uživalské jméno musí mít alespoň 3 znaky. Heslo musí být silné (alespoň 4 znaky).")
            new_name = input("Zadej jméno pro nového administrátora: ").strip()
            if len(new_name) < 3:
                print("[!] Jméno musí mít alespoň 3 znaky.")
                continue
                
            new_pwd = getpass.getpass("Zadej silné heslo: ")
            conf_pwd = getpass.getpass("Potvrď heslo znovu: ")
            
            if new_pwd != conf_pwd:
                print("[!] Hesla se neshodují, zkus to znovu.")
                continue
            if len(new_pwd) < 4:
                print("[!] Heslo je příliš krátké.")
                continue
                
            default_admin = {
                "name": new_name,
                "password": hash_password(new_pwd),
                "role": "Admin"
            }
            users.append(default_admin)
            save_json("users.json", users)
            print(f"\n[OK] Administrátor '{new_name}' byl vytvořen. Nyní se přihlas.")
            print("-" * 40)
            break
    # --- KONEC BOOTSTRAPU ---

    # EN: Standard login process
    # CZ: Standardní přihlašovací proces
    username = input("Zadej své uživatelské jméno: ").strip()
    password = getpass.getpass("Zadej své heslo: ")
    
    user_found = None
    for u in users:
        if u["name"] == username and check_password(password, u["password"]):
            user_found = u
            break
    
    if user_found:
        session.current_user = user_found
        add_system_log("Přihlášení uživatele", user_found['name'])
        print(f"\nVítejte, {user_found['name']}!")
        continue_prompt()
        homepage(user_found)
    else:
        print("\n[!] Nesprávné uživatelské jméno nebo heslo.")
        continue_prompt()

if __name__ == "__main__":
    login()