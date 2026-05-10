from utils import clear_terminal, session, continue_prompt, load_json, save_json, get_valid_rate, add_system_log

def change_of_course():
    session.header("Změna kurzu měny")
    data_currency = load_json("currency.json")
    
    if not data_currency:
        print("Systém je prázdný. Žádné měny k úpravě.")
        continue_prompt()
        return

    # EN: 1. Display currencies with current rates
    # CZ: 1. Výpis měn s aktuálními kurzy
    print("Seznam dostupných měn:")
    for index, currency in enumerate(data_currency, start=1):
        print(f"{index} - {currency['name']} (Nákup: {float(currency['buy_rate']):.2f}, Prodej: {float(currency['sell_rate']):.2f})")
    
    print("q - Zpět do hlavního menu")
    volba = input("\nJakou měnu chceš změnit: ")

    if volba.lower() == "q":
        return

    # EN: 2. Input validation
    # CZ: 2. Validace vstupu
    try:
        index_volby = int(volba) - 1
        if index_volby < 0 or index_volby >= len(data_currency):
            print("[!] Neplatná volba.")
            continue_prompt()
            return
    except ValueError:
        print("[!] Neplatná volba (zadej číslo).")
        continue_prompt()
        return

    selected_currency = data_currency[index_volby]
    
    # EN: 3. Save old values for logging (before change)
    # CZ: 3. Uložení STARÝCH hodnot pro log (před změnou)
    old_buy = float(selected_currency['buy_rate'])
    old_sell = float(selected_currency['sell_rate'])
    curr_name = selected_currency['name']

    clear_terminal()
    session.header(f"Změna kurzu pro {curr_name}")

    # EN: 4. Get new values using get_valid_rate
    # CZ: 4. Získání NOVÝCH hodnot přes get_valid_rate
    new_buy = get_valid_rate(f"Nový nákupní kurz (aktuální: {old_buy:.2f}): ")
    new_sell = get_valid_rate(f"Nový prodejní kurz (aktuální: {old_sell:.2f}): ")

    # EN: 5. Update data and save
    # CZ: 5. Aktualizace dat a uložení
    selected_currency['buy_rate'] = new_buy
    selected_currency['sell_rate'] = new_sell
    save_json("currency.json", data_currency)

    # EN: 6. WRITE TO AUDIT LOG
    # CZ: 6. ZÁPIS DO AUDIT LOGU
    # EN: We log both old and new values to show the change history
    # CZ: Zapíšeme staré i nové hodnoty, aby byl vidět vývoj
    log_msg = (f"ZMĚNA KURZU: {curr_name} | "
               f"Nákup: {old_buy:.2f} -> {new_buy:.2f} | "
               f"Prodej: {old_sell:.2f} -> {new_sell:.2f}")
    
    add_system_log(log_msg, session.current_user['name'])

    # EN: 7. Confirmation for the user
    # CZ: 7. Potvrzení pro uživatele
    print(f"\n[OK] Kurzy pro {curr_name} byly aktualizovány.")
    print(f"Nákup:  {old_buy:.2f} -> {new_buy:.2f}")
    print(f"Prodej: {old_sell:.2f} -> {new_sell:.2f}")
    
    continue_prompt()