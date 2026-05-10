from utils import load_json, continue_prompt, session, save_json

def edit_permissions():
    session.header("Úprava práv uživatele")
    
    # EN: Using load_json with default value
    # CZ: Používáme náš nový load_json s defaultní hodnotou
    users = load_json("users.json", default_value=[])
    
    if not users:
        print("[!] Žádní uživatelé v systému.")
        continue_prompt()
        return

    print("Seznam uživatelů:")
    for idx, user in enumerate(users, start=1):
        print(f"{idx}. {user['name']:<15} (Role: {user['role']})")

    # EN: --- Handling user index input ---
    # CZ:--- Ošetření vstupu indexu ---
    volba = input("\nZadej číslo uživatele pro úpravu (nebo 'q' pro návrat): ").strip()
    
    if volba.lower() == 'q':
        return

    try:
        user_index = int(volba) - 1
        if user_index < 0 or user_index >= len(users):
            print("[!] Neplatné číslo uživatele.")
            continue_prompt()
            return
    except ValueError:
        print("[!] Chyba: Musíš zadat celé číslo.")
        continue_prompt()
        return

    selected_user = users[user_index]
    
    # EN: Security: Admin should not be able to edit themselves (optional, but recommended)
    # CZ: Zabezpečení: Admin by neměl upravovat sám sebe (volitelné, ale doporučené)
    if selected_user['name'] == session.current_user['name']:
        print("[!] Nemůžeš upravovat svou vlastní roli.")
        continue_prompt()
        return

    print(f"\nUživatel: {selected_user['name']} | Současná role: {selected_user['role']}")
    
    print("Dostupné role: Admin, Majitel, Spravce, Zamestnanec")
    print("Poznámka: Role jsou citlivé na velikost písmen, zadej přesně.")
    print("Doporučuji odstranit diakritiku z názvů rolí pro lepší stabilitu (např. Spravce místo Správce).")
    new_role = input("Zadej novou roli uživatele: ").strip().capitalize()

    valid_roles = ["Admin", "Majitel", "Spravce", "Zamestnanec"]
    
    if new_role not in valid_roles:
        print(f"[!] '{new_role}' není platná role.")
        continue_prompt()
        return

    # EN: --- Saving changes ---
    # CZ: --- Uložení změn ---
    old_role = selected_user["role"]
    selected_user["role"] = new_role
    save_json("users.json", users)
    
    # EN: Logging the change
    # CZ: Logování změny
    from utils import add_system_log
    add_system_log(f"Změna role: {selected_user['name']} ({old_role} -> {new_role})", 
                   session.current_user['name'])

    print(f"\n[OK] Role uživatele {selected_user['name']} byla změněna na {new_role}.")
    continue_prompt()